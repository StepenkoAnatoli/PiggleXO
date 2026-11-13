# PiggleXO — business investigation and validation package

**Start with the [current decision and experiment](investigation/2026-11-13/README.md), updated 13 November 2026.** The owner's confirmed experience, languages, time and $350 loss ceiling change the ranking: test a **$149 bilingual customer-support reply pack**, with a bounded CSV cleanup service as the fallback. Paid demand is unvalidated. The [offer](investigation/2026-11-13/offer.md), [multilingual sample](investigation/2026-11-13/sample.md), [experiment](investigation/2026-11-13/experiment.md), [economics](investigation/2026-11-13/economics.md) and [sources](investigation/2026-11-13/sources.md) are prepared for review. No marketing or customer contact has been executed.

**Historical investigation below, dated 12 November 2026.** Its craft-market template recommendation and time assumptions are superseded by the update above. Its approximately 34 candidates, eight invention hypotheses, source records, code and contrary evidence remain useful background; they are preserved rather than silently rewritten. The new update adds a broad rescreen, five deeper candidates, a reviewed public portfolio and fifteen conditional financial scenarios.

| Read / run | Purpose |
|---|---|
| [Main report](REPORT.md) | Recommendation, ranking, confidence, economics and limits |
| [Selected experiment and 7/30-day plans](plans/validation.md) | One audience/channel/offer; budgets, payment and quality gates, stopping criteria |
| [Phone operations](plans/phone-operations.md) | Actions, digest, queue, quiet notifications and 10h/48h/week absence behavior |
| [Financial assumptions](models/assumptions.md) and [generated results](models/results.md) | Consistent volume/workload, cash flow, labor, scenarios and stress tests |
| [Non-social landscape](research/landscape.md) | 26 screening entries and six deeper dossiers |
| [Social investigation](research/social-media.md) | 12 entries, routes A–F, platform checks, six-operator sample and three dossiers |
| [Inventions](research/inventions.md) | Eight hypotheses and nearest substitutes; no worldwide novelty claims |
| [Technical audit](research/technical-audit.md) | Exact upstream commits/licenses/code inspections and build/buy tradeoffs |
| [Evidence ledger](research/evidence-ledger.md) | Source IDs, dates, claim limits and decisions |
| [Coverage/corrections](research/coverage-and-checks.md) | Checks actually completed, changes to conclusions and unresolved claims |
| [Offline prototype](prototype/README.md) | Original synthetic CSV validation demonstration; not the selected product or production service |
| [Verification record](VERIFICATION.md) | Executed local checks and limitations |

The historical 38 screening rows include four overlaps, documented in the old report. The social template is one business analyzed twice, not two opportunities. The **current** experiment is controlled by `investigation/2026-11-13/experiment.md`; historical F3 and `plans/validation.md` no longer control the selection. Alternatives are not concurrent launch instructions.

## Reproduce the local checks

Python standard library only. Tested with Python 3.14.7 on Windows. From the repository root:

```powershell
python investigation/2026-11-13/economics.py
python models/economics.py
python -m unittest discover -s models -p "test_*.py" -v
python prototype/run_demo.py
python scripts/build_evidence_index.py
```

The deliberately flawed prototype sample exits 1 for findings; its demo runner checks that this is expected. It makes no network calls or external changes, uses synthetic data and records actual sample outputs. It is not Shopify-compatible and has no payment, hosting, email or phone integration. The original local tests do not validate upstream dependencies, a real business or future reliability.

No customers were contacted, funds spent, third-party accounts created or business launched. The requested repository push shares the investigation and local artifacts. Do not commit real customer files, credentials, payment exports or private notes; `private/`, local databases and environment files are ignored where appropriate. Private asset notes and the uncontacted prospect shortlist remain local. The historical workbook was not built; the current reply-pack sample is synthetic and has not been used by a buyer.
