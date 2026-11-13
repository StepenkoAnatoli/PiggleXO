# Fallback: one bounded CSV cleanup job

Prepared 13 November 2026. Launch only if the support-pack test fails or the owner's readiness assessment clearly favors this service. This is a draft offer and verified portfolio assessment, not a live job or a production-readiness certification.

## Existing public asset

[automation-samples at the reviewed commit](https://github.com/StepenkoAnatoli/automation-samples/tree/fccf9007055764fcc4ec6a41b177643d2b71b5b7) contains a Python CSV cleanup example and a Node API export example, with reports and before/after data. The samples are more credible than a claim that “AI can automate anything.” They are not evidence of a paying customer.

An ignored local clone was inspected without changing the original repository. Python 3.14.7: `python -m pytest csv-cleanup -q` passed **49 tests**. Node 24.20.0, from `api-to-csv`: `node --test "test/*.test.mjs"` passed **18 tests**. The API tests use fixtures; no live API export or customer integration was run. No new packages were installed. These are recorded results, not an independent security audit.

The sample cleanup report reconciles 20 nonblank input rows into 11 output rows, 4 rejected rows and 5 merged duplicate rows. The rule set assumes day-first dates, defaults missing currency to ILS, and keeps the newest dated row for each SKU. Those rules are appropriate only when explicitly agreed. Rows from different suppliers or currencies may not be interchangeable even when the SKU matches. The public portfolio should explain these decisions rather than obscure them.

## Reviewable offer

**Title:** I will clean one small product CSV and document every rule

**Price hypothesis:** $99, five business days, one consolidated correction round within scope. Direct quote; actual marketplace price controls may require review before publication.

**Included:** one CSV file, up to 1,000 rows and 20 columns, one agreed output schema, explicit normalization rules, rejected/duplicate row report, before/after counts and a short rule summary. The buyer approves the rules on a small sanitized sample before the full batch is transformed. Keep the original unchanged.

**Excluded:** customer/payment/patient data, scraping, live API connections, database repairs, store imports, accounting/tax decisions, fuzzy identity matching, multiple suppliers without agreed identifiers, guessing currency or date ambiguity, macros and arbitrary executable files. XLSX can be considered later after separately reviewing spreadsheet-specific security and formatting needs; the pilot is CSV only.

**Buyer-facing draft:**

> I will normalize one small product CSV using rules we agree in advance and return both the cleaned file and a report of rows that need your decision. The $99 pilot includes up to 1,000 rows and 20 columns, one output schema, and one correction round. I will not guess ambiguous currencies, dates or duplicate matches. Please send only a sanitized sample first; no customer or payment data. You review the output before using it in another system. My public portfolio shows synthetic before/after examples and the rules behind them. Delivery is five business days after complete inputs and rule approval.

## Owner readiness exercise

Using only the existing synthetic sample, explain:

1. Why 20 input rows do not become 20 output rows, and where each missing row is accounted for.
2. Why `03/04/2026` is ambiguous without an agreed date convention.
3. Why missing currency cannot safely be assumed from the owner's country.
4. Why a later USD row and an earlier ILS row cannot automatically be treated as a price update; likewise the same SKU from two suppliers.
5. How to preserve leading zeros and prevent a spreadsheet viewer from interpreting dangerous formula-like input when exporting a file that someone will open.
6. How to stop and ask the buyer when a file is outside the agreed schema, rather than patching a customer's production system.

Then rerun the sample and locate one rejected row and its reason. If the owner cannot explain these without relying on unexamined AI output, do not accept a paid job yet. Passing the current unit tests does not answer the spreadsheet-formula/export safety question; that remains a pre-delivery control to inspect for the actual output workflow.

## Test and economics

Seek one explicitly posted matching task or qualified inbound buyer after publication/contact authorization. Do not apply to a broad software-development job just because its title says cleaning. Compare against the buyer's current free tool and cheap service alternatives. Show the auditability, not an invented claim of superior accuracy.

The $99 direct-sale model leaves **$68.65 contribution** after the stated collection, refund, tools and acquisition allowances. At five hours including selling, that is $13.73/hour before fixed costs and tax. If delivery can fall to two hours and acquisition/admin to one, the same contribution supports $22.88/hour; that efficiency is unproven. One extra two-hour correction can erase the improvement. Do not buy ads for this margin.

Continue only if rules are understandable, no rows disappear without explanation, delivery fits <=3 hours, and the buyer accepts and safely uses the output. Repeat-client batches may later improve acquisition efficiency, but a subscription cannot be inferred from a single cleanup job. Hosted automation, live writes and API connections require a new scope and risk review.
