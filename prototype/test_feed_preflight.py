import csv
from contextlib import closing
import io
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

import feed_preflight as feed


def make_csv(rows, header=feed.REQUIRED):
    output = io.StringIO(newline="")
    writer = csv.writer(output)
    writer.writerow(header)
    writer.writerows(rows)
    return output.getvalue().encode("utf-8")


GOOD = ["SKU-1", "Plain tea cup", "12.50", "USD", "https://example.com/cup"]


class PreflightTests(unittest.TestCase):
    def codes(self, report):
        return [issue["code"] for issue in report["issues"]]

    def test_clean_and_quoted_unicode(self):
        row = GOOD.copy()
        row[1] = 'כוס, cup "quoted"\nsecond line'
        self.assertTrue(feed.validate_csv(make_csv([row]))["valid"])

    def test_duplicate_sku_not_duplicate_titles(self):
        second = GOOD.copy()
        second[0] = " SKU-1 "
        report = feed.validate_csv(make_csv([GOOD, second]))
        self.assertEqual(report["issues"], [{"row": 3, "field": "sku", "code": "duplicate_sku", "first_row": 2}])
        second[0] = "sku-1"  # Explicitly case sensitive.
        self.assertTrue(feed.validate_csv(make_csv([GOOD, second]))["valid"])

    def test_missing_and_duplicate_headers_fail(self):
        report = feed.validate_csv(make_csv([GOOD], ["sku", "title", "price", "link", "link"]))
        self.assertIn("duplicate_header", self.codes(report))
        self.assertIn("missing_header", self.codes(report))

    def test_missing_cells_and_extra_columns(self):
        empty = GOOD.copy()
        empty[1] = "   "
        self.assertIn("missing_value", self.codes(feed.validate_csv(make_csv([empty]))))
        self.assertIn("wrong_column_count", self.codes(feed.validate_csv(make_csv([GOOD + ["x"]]))))

    def test_price_shapes_and_nonfinite_numbers(self):
        for value in ["NaN", "Infinity", "1e3", "-1", "1,50", "$2", "1.234", "1_000", "１２"]:
            with self.subTest(value=value):
                row = GOOD.copy()
                row[2] = value
                self.assertIn("invalid_price", self.codes(feed.validate_csv(make_csv([row]))))
        for value in ["0", "0.00", "999999999.99", "12.5"]:
            row = GOOD.copy()
            row[2] = value
            self.assertTrue(feed.validate_csv(make_csv([row]))["valid"])

    def test_formula_and_unicode_controls_not_echoed(self):
        for value in ["=1+1", " +SUM(A1)", "\t@command", "\u200b=1", "\u202e=1"]:
            row = GOOD.copy()
            row[1] = value
            report = feed.validate_csv(make_csv([row]))
            self.assertIn("formula_like_cell", self.codes(report))
            self.assertNotIn(value, json.dumps(report))

    def test_html_is_data_and_never_echoed(self):
        row = GOOD.copy()
        row[1] = '<script>alert("x")</script>'
        report = feed.validate_csv(make_csv([row]))
        self.assertTrue(report["valid"])
        self.assertNotIn("<script>", json.dumps(report))

    def test_urls_are_shape_checks_only(self):
        for value in ["javascript:alert(1)", "https://user:pass@example.com", "https://example.com:bad", "https://exa mple.com"]:
            row = GOOD.copy()
            row[4] = value
            self.assertIn("invalid_link_shape", self.codes(feed.validate_csv(make_csv([row]))))
        row = GOOD.copy()
        row[4] = "https://unresolvable.invalid/item"
        self.assertTrue(feed.validate_csv(make_csv([row]))["valid"])

    def test_empty_invalid_encoding_nul_and_unclosed_quote(self):
        self.assertIn("empty_file", self.codes(feed.validate_csv(b"")))
        self.assertIn("no_data_rows", self.codes(feed.validate_csv(make_csv([]))))
        for data in [b"\xff", b"\x00"]:
            with self.assertRaises((ValueError, UnicodeError)):
                feed.validate_csv(data)
        with self.assertRaises(csv.Error):
            feed.validate_csv(b'sku,title,price,currency,link\nx,"unclosed')

    def test_limits(self):
        with patch.object(feed, "MAX_BYTES", 5):
            with self.assertRaises(ValueError):
                feed.validate_csv(b"123456")
        with patch.object(feed, "MAX_ROWS", 1):
            with self.assertRaises(ValueError):
                feed.validate_csv(make_csv([GOOD, GOOD]))

    def test_digest_dedup_recovery_and_reversion(self):
        with tempfile.TemporaryDirectory() as temp:
            state = Path(temp) / "state.sqlite"
            bad = feed.validate_csv(make_csv([GOOD, GOOD]))
            first = feed.record_run(bad, state, "customer-a")
            repeated = feed.record_run(bad, state, "customer-a")
            self.assertTrue(first["digest_actionable"])
            self.assertFalse(repeated["digest_actionable"])
            self.assertTrue(repeated["seen_input_before"])
            self.assertEqual(feed.phone_digest(repeated), "")
            clean = feed.validate_csv(make_csv([GOOD]))
            recovered = feed.record_run(clean, state, "customer-a")
            self.assertEqual(recovered["digest_reason"], "recovered")
            reverted = feed.record_run(bad, state, "customer-a")
            self.assertTrue(reverted["digest_actionable"])
            with closing(sqlite3.connect(state)) as db:
                self.assertEqual(db.execute("SELECT count(*) FROM runs").fetchone()[0], 2)

    def test_clean_change_quiet_and_customer_isolation(self):
        with tempfile.TemporaryDirectory() as temp:
            state = Path(temp) / "state.sqlite"
            clean = feed.validate_csv(make_csv([GOOD]))
            self.assertFalse(feed.record_run(clean, state, "a")["digest_actionable"])
            row = GOOD.copy()
            row[1] = "New title"
            self.assertFalse(feed.record_run(feed.validate_csv(make_csv([row])), state, "a")["digest_actionable"])
            bad = feed.validate_csv(make_csv([GOOD, GOOD]))
            self.assertTrue(feed.record_run(bad, state, "a")["digest_actionable"])
            self.assertTrue(feed.record_run(bad, state, "b")["digest_actionable"])

    def test_corrupt_state_is_error(self):
        with tempfile.TemporaryDirectory() as temp:
            state = Path(temp) / "state.sqlite"
            state.write_bytes(b"not a database")
            with self.assertRaises(sqlite3.DatabaseError):
                feed.record_run(feed.validate_csv(make_csv([GOOD])), state, "a")

    def test_cli_cannot_overwrite_input(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            csv_path = root / "source.csv"
            original = make_csv([GOOD])
            csv_path.write_bytes(original)
            code = feed.main([str(csv_path), "--state", str(root / "state.sqlite"),
                              "--report", str(csv_path), "--digest", str(root / "digest.txt")])
            self.assertEqual(code, 2)
            self.assertEqual(csv_path.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
