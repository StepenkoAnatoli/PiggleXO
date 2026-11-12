"""Offline synthetic supplier CSV preflight. No network or catalog writes.

This is a deliberately small schema demonstration, not a Shopify/Google feed
validator. Prices use ASCII decimal notation; SKUs are trim-normalized and
case-sensitive. No input cells are echoed into reports or executed.
"""
from __future__ import annotations

import argparse
import csv
from contextlib import closing
import hashlib
import io
import json
from pathlib import Path
import re
import sqlite3
import sys
import unicodedata
from urllib.parse import urlsplit

RULES_VERSION = "synthetic-supplier-v1"
REQUIRED = ("sku", "title", "price", "currency", "link")
MAX_BYTES = 5_000_000
MAX_ROWS = 10_000
MAX_FIELD = 20_000
PRICE = re.compile(r"(?:0|[1-9][0-9]{0,8})(?:\.[0-9]{1,2})?\Z")
CURRENCY = re.compile(r"[A-Z]{3}\Z")


def digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, ensure_ascii=True,
                         separators=(",", ":")).encode("ascii")
    return hashlib.sha256(encoded).hexdigest()


def validate_csv(data: bytes) -> dict:
    """Return bounded, deterministic findings; throw on unreadable input.

    Row numbers count CSV records (including header), not physical lines.
    A field can contain a quoted newline. No URL is ever fetched.
    """
    if len(data) > MAX_BYTES:
        raise ValueError("file exceeds the 5 MB prototype limit")
    text = data.decode("utf-8-sig", errors="strict")
    if "\x00" in text:
        raise ValueError("NUL byte in CSV")
    old_limit = csv.field_size_limit(MAX_FIELD)
    issues: list[dict] = []
    rows = 0
    seen: dict[str, int] = {}

    def issue(row: int, field: str, code: str, **extra: object) -> None:
        issues.append({"row": row, "field": field, "code": code, **extra})

    try:
        reader = csv.reader(io.StringIO(text, newline=""), strict=True)
        header = next(reader, None)
        if header is None:
            issue(1, "", "empty_file")
        else:
            # Enforce exact schema to prevent guessing ambiguous customer mappings.
            if len(set(header)) != len(header):
                issue(1, "", "duplicate_header")
            for field in REQUIRED:
                if field not in header:
                    issue(1, field, "missing_header")
            if any(field not in REQUIRED for field in header):
                issue(1, "", "unknown_header")
            schema_ok = len(header) == len(REQUIRED) and set(header) == set(REQUIRED)
            for row_number, cells in enumerate(reader, start=2):
                rows += 1
                if rows > MAX_ROWS:
                    raise ValueError("file exceeds the 10000-row prototype limit")
                if len(cells) != len(header):
                    issue(row_number, "", "wrong_column_count")
                # Check every supplied cell, even with invalid/missing schema.
                for index, cell in enumerate(cells):
                    field = header[index] if schema_ok and index < len(header) else ""
                    # Strip Unicode whitespace and format controls before detection.
                    prefix = cell.lstrip()
                    while prefix and unicodedata.category(prefix[0]) == "Cf":
                        prefix = prefix[1:].lstrip()
                    if prefix.startswith(("=", "+", "-", "@")):
                        issue(row_number, field, "formula_like_cell")
                    if any(unicodedata.category(ch) == "Cf" for ch in cell):
                        issue(row_number, field, "unicode_format_control")
                if not schema_ok or len(cells) != len(header):
                    continue
                record = dict(zip(header, cells))
                for field, value in record.items():
                    if not value.strip():
                        issue(row_number, field, "missing_value")
                sku = record["sku"].strip()
                if sku:
                    if sku in seen:
                        issue(row_number, "sku", "duplicate_sku", first_row=seen[sku])
                    else:
                        seen[sku] = row_number
                if record["price"].strip() and not PRICE.fullmatch(record["price"].strip()):
                    issue(row_number, "price", "invalid_price")
                if record["currency"].strip() and not CURRENCY.fullmatch(record["currency"].strip()):
                    issue(row_number, "currency", "invalid_currency_shape")
                if record["link"].strip():
                    try:
                        url = urlsplit(record["link"].strip())
                        valid = (url.scheme in ("https", "http") and bool(url.hostname)
                                 and url.username is None and url.password is None
                                 and not any(ch.isspace() for ch in record["link"]))
                        # Force validation of port if one is present.
                        _ = url.port
                    except ValueError:
                        valid = False
                    if not valid:
                        issue(row_number, "link", "invalid_link_shape")
            if rows == 0:
                issue(1, "", "no_data_rows")
    finally:
        csv.field_size_limit(old_limit)
    return {"schema": RULES_VERSION, "input_sha256": hashlib.sha256(data).hexdigest(),
            "rows": rows, "valid": not issues, "issue_count": len(issues), "issues": issues,
            "estimated_external_cost_usd": 0, "external_actions": 0}


def record_run(report: dict, state_path: Path, feed_id: str) -> dict:
    """Persist deduplicated runs and decide whether a local digest is useful.

    No delivery occurs. The state remembers a decision, not delivery confirmation.
    A production sender needs an outbox + acknowledgment to prevent silent loss.
    """
    job_key = digest([feed_id, report["schema"], report["input_sha256"]])
    signature = digest([report["schema"], report["issues"]])
    with closing(sqlite3.connect(state_path, timeout=5)) as db, db:
        db.execute("CREATE TABLE IF NOT EXISTS runs (job_key TEXT PRIMARY KEY)")
        db.execute("CREATE TABLE IF NOT EXISTS feeds (feed_id TEXT PRIMARY KEY, signature TEXT NOT NULL, valid INTEGER NOT NULL)")
        db.execute("BEGIN IMMEDIATE")
        prior = db.execute("SELECT signature, valid FROM feeds WHERE feed_id=?", (feed_id,)).fetchone()
        prior_job = db.execute("SELECT 1 FROM runs WHERE job_key=?", (job_key,)).fetchone()
        # Reversion to an earlier bad file is actionable after a clean run.
        changed = prior is None or prior[0] != signature
        notify = changed and (not report["valid"] or (prior is not None and not prior[1]))
        reason = ("new_or_changed_findings" if notify and not report["valid"] else
                  "recovered" if notify else "unchanged_or_clean")
        db.execute("INSERT OR IGNORE INTO runs VALUES (?)", (job_key,))
        db.execute("INSERT INTO feeds VALUES (?, ?, ?) ON CONFLICT(feed_id) DO UPDATE SET signature=excluded.signature, valid=excluded.valid", (feed_id, signature, int(report["valid"])))
    return {**report, "job_key": job_key, "seen_input_before": prior_job is not None,
            "digest_actionable": bool(notify), "digest_reason": reason,
            "delivery_attempted": False}


def phone_digest(report: dict) -> str:
    if not report["digest_actionable"]:
        return ""
    codes: dict[str, int] = {}
    for item in report["issues"]:
        codes[item["code"]] = codes.get(item["code"], 0) + 1
    summary = ", ".join(f"{code}: {count}" for code, count in sorted(codes.items()))
    state = "REVIEW" if not report["valid"] else "RECOVERED"
    details = f"{report['rows']} rows; {report['issue_count']} findings."
    if summary:
        details += f" {summary}"
    return (f"Supplier preflight: {state}\n"
            f"{details}\n"
            "External actions: 0. External spend: $0 (local synthetic test).\n"
            "Revenue, margin, cash and owner minutes: not measured by this prototype.\n"
            "Next action: review report in weekly batch; no import or correction approved.\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--feed-id", default="synthetic-demo")
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--digest", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        # Bounded read also handles files that grow after a metadata check.
        with args.csv_path.open("rb") as stream:
            data = stream.read(MAX_BYTES + 1)
        report = validate_csv(data)
        # Do not let output paths overwrite input/state or each other.
        paths = [p.resolve() for p in (args.csv_path, args.state, args.report, args.digest)]
        if len(set(paths)) != len(paths):
            raise ValueError("input, state, report and digest paths must be different")
        # Validate writable output locations before changing digest state.
        for path in (args.report, args.digest):
            if not path.parent.is_dir():
                raise ValueError("output parent directory does not exist")
        report = record_run(report, args.state, args.feed_id)
        args.report.write_text(json.dumps(report, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
        args.digest.write_text(phone_digest(report), encoding="utf-8")
        print(f"rows={report['rows']} issues={report['issue_count']} actionable={report['digest_actionable']}")
        return 0 if report["valid"] else 1
    except (ValueError, UnicodeError, OSError, csv.Error, sqlite3.Error) as exc:
        # Do not echo potentially sensitive file data or OS messages.
        print(f"Preflight failed closed ({type(exc).__name__}); no external action taken.", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
