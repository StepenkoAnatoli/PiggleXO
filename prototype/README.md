# Offline supplier CSV preflight demonstration

This original Python-standard-library example checks a **synthetic** five-column supplier schema. It demonstrates exception reporting and quiet repeat decisions. It is not a hosted service, Shopify importer, Google Merchant feed validator, spreadsheet sanitizer or proof of a profitable business. No URLs are fetched, no data leaves the computer, no cell is evaluated, and no catalog or payment action exists.

Run from this directory with Python 3.10+ (actually tested with Python 3.14.7 on Windows):

```powershell
python -m unittest -v test_feed_preflight.py
python feed_preflight.py samples/supplier.csv --state demo-state.sqlite --report sample-report.json --digest sample-digest.txt
python run_demo.py
```

The deliberate bad sample returns exit **1** for findings; this is expected. Exit **0** means no findings under this limited schema; exit **2** means processing failed. State/output parent directories must already exist. Run the same command again to see an empty digest and `digest_actionable: false`. Run `samples/clean.csv` with the same state to produce a recovery digest. State is local SQLite; use a fresh filename to repeat the first-run scenario. Do not place real customer files in this repository or commit generated customer reports.

Required headers are exactly `sku,title,price,currency,link`, in any order, each once; no extra columns. Duplicate detection uses trimmed case-sensitive SKU, not product title or URL handle. Price syntax is nonnegative ASCII decimal with at most nine integer and two fractional digits. Currency checking validates only the shape of three uppercase ASCII letters. Link checking validates only an HTTP(S) URL shape with a host and without embedded credentials. A syntactically valid URL can be unreachable; a syntactically valid currency can be nonexistent. Formula-like prefixes and Unicode format controls are warnings represented as findings; no automatic correction occurs. HTML remains inert and is not copied into output. Input cells are not echoed into JSON or digest text.

Limits: 5 MB input, 10,000 CSV records and 20,000 characters per field. Row numbers count logical CSV records, including the header, not physical lines. Strict UTF-8 (with optional BOM) and strict CSV parsing apply. This narrower schema intentionally rejects inputs that require ambiguous mapping; legitimate product variants and multiple image rows in other formats require different rules.

State identifies inputs by feed ID, rules version and SHA-256. Repeated findings are quiet; recovery and reversion to a previously bad input are actionable. A different bad value at the same row/field/code remains quiet. State isolation is a label convention in this local prototype, not tenant authentication. No delivery occurs, so `digest_actionable` means useful local content exists, not that a notification was sent. The state transaction and output files are not one atomic operation; an output failure after state commit can suppress a later digest. A production version requires a durable outbox, acknowledgment/replay, authenticated controls, backups, scheduling, transport retries, retention rules, concurrency testing and a customer-approved schema. None of those are claimed implemented.

The regression suite covers CSV edge cases, formula/Unicode inputs, nonfinite prices, safe reporting, malformed URLs, input/row limits, deduplication/recovery/reversion, independent feed labels, corrupt state, and output/input path equality. Initial test execution exposed SQLite connections remaining open on Windows; the implementation and tests now close connections explicitly. Fourteen tests passed after that correction. See `samples/test-results.txt` and `samples/run-summary.json` for actual run artifacts. The checked-in sample reports contain synthetic data only.

The demonstration intentionally uses no LLM. AI could explain already validated findings later, but should not invent rules or write to a merchant system. Build a paid service only after the demand experiment in the main report meets its gates.
