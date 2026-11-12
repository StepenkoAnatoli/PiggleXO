"""Reproduce the synthetic sample artifacts without leaving a state database."""
import json
from pathlib import Path
import platform
import subprocess
import sys
import tempfile


def main():
    root = Path(__file__).resolve().parent
    samples = root / "samples"
    tests = subprocess.run([sys.executable, "-m", "unittest", "-v", "test_feed_preflight.py"],
                           cwd=root, capture_output=True, text=True, encoding="utf-8")
    (samples / "test-results.txt").write_text(
        f"Python {platform.python_version()} on {platform.system()}\n" + tests.stdout + tests.stderr,
        encoding="utf-8")
    if tests.returncode:
        print("Tests failed; inspect samples/test-results.txt")
        return tests.returncode
    runs = []
    with tempfile.TemporaryDirectory() as temp:
        for label, source, expected in [("first", "supplier.csv", 1),
                                        ("repeat", "supplier.csv", 1),
                                        ("recovered", "clean.csv", 0)]:
            report = samples / f"{label}-report.json"
            output = subprocess.run(
                [sys.executable, "feed_preflight.py", str(samples / source),
                 "--state", str(Path(temp) / "state.sqlite"),
                 "--report", str(report), "--digest", str(samples / f"{label}-digest.txt")],
                cwd=root, capture_output=True, text=True, encoding="utf-8")
            if output.returncode != expected:
                print(f"Unexpected demo result: {label}: {output.returncode}")
                return 2
            data = json.loads(report.read_text(encoding="utf-8"))
            runs.append({"label": label, "input": source, "exit_code": output.returncode,
                         "rows": data["rows"], "issues": data["issue_count"],
                         "digest_actionable": data["digest_actionable"],
                         "digest_reason": data["digest_reason"], "stdout": output.stdout.strip()})
    summary = {"research_date": "2026-11-12", "python": platform.python_version(),
               "platform": platform.system(), "tests": 14, "test_exit_code": tests.returncode,
               "data": "synthetic only", "network_calls": 0, "external_spend_usd": 0,
               "hosted_or_mobile_tested": False, "runs": runs}
    (samples / "run-summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
