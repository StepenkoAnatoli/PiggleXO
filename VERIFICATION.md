# Verification record

Research and local verification date: **12 November 2026**. Environment actually used: **Python 3.14.7, Windows**. No external runtime dependencies were installed for the included code.

| Check actually executed | Result | Scope limit |
|---|---|---|
| `python models/economics.py` | Generated 12 conditional scenarios, 8 target-volume rows and 28 stress rows into JSON/Markdown | Inputs are hypotheses, not measured sales/CAC/workload |
| `python -m unittest discover -s models -p "test_*.py" -v` | **5 tests passed** | Tests cover cost identity, zero-sales cost/time, replacement versus initial acquisition, smallest target volume, and volume-consistent workload/labor |
| `python prototype/run_demo.py` | **14 tests passed**, followed by three expected CLI results | Original local code and synthetic schema only; upstream/hosted/platform behavior not tested |
| First flawed synthetic file | 5 rows, 6 findings, actionable local digest; expected exit 1 | No notification delivered; no external call or spend |
| Identical repeat | Same findings, quiet local digest; expected exit 1 | Local decision deduplication, not exactly-once network delivery |
| Clean recovery file | 3 rows, 0 findings, recovery digest; exit 0 | No findings under this narrow schema is not proof real business data is correct |
| `python scripts/build_evidence_index.py` | **134 source-ledger records**, 126 distinct URL strings after trailing-slash normalization | Includes repeated sources/access failures; count is not an evidence-quality score |

Actual prototype run outputs are in [run-summary.json](prototype/samples/run-summary.json) and [test-results.txt](prototype/samples/test-results.txt). Financial inputs and raw calculations are in [results.json](models/results.json). Evidence JSON files preserve dates, inspection classes and uncertainties; the generated ledger is navigational.

Code inspection found and corrected SQLite connection lifecycle handling during the initial prototype run. Subsequent tests passed. Source/output state is still not one atomic transaction: an output write failure after state commit can suppress a later digest. This is documented in the prototype; production requires a durable outbox and replay/acknowledgement. No scheduler, transport retry mechanism, email sender, authenticated multi-tenant upload, mobile control, payment route or production import exists.

Financial cross-review recomputed the 12 scenario results and identified additional conversation-acquisition time and a sample time-budget mismatch, now explained/corrected. Exact source rechecks changed the business ranking and fee/platform assumptions. See [coverage and corrections](research/coverage-and-checks.md). A review is not independent customer evidence.

Before the repository push, local Markdown links and evidence-ID references were checked, JSON files parsed, and Git whitespace/content inventory inspected. No credential/private-customer files were included. External links were not all re-fetched in a separate link-crawler pass; source access statuses reflect the research inspections. No claims are made about future availability.

The selected template product has **not** been built, usability-tested, purchased or used by a customer. Its seven-day/30-day plan and longer paid pilot are future conditional work. No business was deployed, third-party account created, money spent, content posted or outreach sent. GitHub publication of this research/code package was explicitly requested by the user.
