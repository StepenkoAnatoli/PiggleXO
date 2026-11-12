# Invention and adaptation portfolio

Research date: **12 November 2026**. These eight hypotheses were designed from observed tasks, then challenged with substitute searches. They are not eight businesses to launch. “Original” here describes the design exercise, not worldwide novelty, patentability or demonstrated willingness to pay. Several apparently original concepts had very close existing equivalents. Those findings are preserved instead of inventing differentiation.

The source ledger is [market-sources.json](market-sources.json); broader buyer/task screening is [landscape.md](landscape.md). Proposed prices, budgets, conversion thresholds and owner times below are **hypotheses or predeclared experiment limits**, not observed market statistics. Tests requiring outreach, payment or publishing are future plans outside this research-only authorization.

## Portfolio decisions at a glance

| ID | Hypothesis and paid outcome | Closest observed substitute | Status after search |
|---|---|---|---|
| I01 | Agency catalog-change decision receipt | Preflight Kit, CSV SafeCheck, LocalCSV, MerchantUtil | Generic novelty rejected; only buyer substitution test remains |
| I02 | Weekly commercial-change brief with explicit monitoring coverage | Visualping summaries, selectors and monitoring health alerts | Conditional adaptation; editorial value and payment unresolved |
| I03 | Translation API acceptance check before saving | Localazy built-in QA and existing localization workflows | Conditional technical gap; strongest overlooked integration test |
| I04 | Replay fixtures for duplicate AI tool actions after timeouts | Promptfoo, Langfuse, existing deterministic tests | Conditional artifact, technical expertise required |
| I05 | Agency missing-decision packet | Content Snare, Drive checklist, approval portals | Conditional workflow packaging; likely setup service |
| I06 | Tender amendment-only evidence digest | Generic monitoring; BidVeritas discovery lead | Downgraded; urgent deadlines conflict with owner schedule |
| I07 | Export-schema compatibility pack for one licensed spreadsheet | SheetBrain, Innovvo saved import contracts, Sheetgo | Conditional product maintenance; generic schema checker rejected |
| I08 | Non-regulated PDF extraction evidence packet | Docparser; EviTrace provenance design | Insufficient buyer/payment evidence; bounded technical test only |

No hypothesis is promoted to “market-proven.” I03 is interesting because an official API limitation is specific and falsifiable, but a technical omission may be easy for the platform or customer to fix. The final cross-category decision selects F3/S05, described in [the validation plan](../plans/validation.md), as the single first experiment. I01 and the tests below are conditional alternatives only. I01 tests an objection, not a recommendation to build another validator.

## I01 — Catalog-change decision receipt for agencies

**Observed problem / buyer / trigger.** Agencies preparing repeated product imports must decide whether proposed changes are intentional. CSV complaints and manual validation discussions support the task only weakly; one superficially relevant thread was admitted builder research and was excluded. Trigger: an already planned import, not an imagined future problem. Sources MKT04–06.

**Proposed outcome.** A review-only document listing changed fields, unexplained removals, explicit assumptions, source-file hashes and agency-approved decisions. No store write, guarantee of importability or inferred missing product values. Hypothetical price: $29 per scheduled report, with recurring pricing considered only after repeated paid use.

**Substitutes and search.** Exact query “CSV preflight Shopify GitHub validator” found Preflight Kit, CSV SafeCheck and several local tools. Opened LocalCSV documents supplier-cost comparison too; simply adding supplier reconciliation does not restore novelty. MerchantUtil gives a free checklist. [Preflight Kit](https://github.com/q00tar00/preflight-kit) [LocalCSV](https://github.com/livastic-vm3-primary-tmp-260920/localcsv-shopify-supplier-audit) [MerchantUtil](https://merchantutil.com/en/errors/shopify-blank-overwrite)

**Why now / what's new.** Cheap deterministic parsing and AI-assisted explanations reduce prototype cost, but the plausible adaptation is an agency's documented acceptance workflow, not new technology. Required access: authorized product-only exports and a buyer willing to define acceptance criteria. Acquisition: one permitted agency placement.

**Switching reason and durable advantage.** A buyer might pay for a clear, supported decision record that reduces their own review time. Only accumulated reliable test cases, trust and distribution could survive copying; a report layout or AI explanation is easy to copy.

**Failure / cheapest test.** If revisited after the selected experiment, show five qualified agencies the free substitutes and one synthetic report before requesting payment. Budget $100 cash and six hours; stop if four say their existing tools are sufficient. Require paid completion and repeated jobs before subscription development. The landscape describes this fallback test; the main validation plan controls the selected experiment. Do not run eight pilots.

## I02 — Commercial change brief that also says what could not be checked

**Observed problem / buyer / trigger.** A small SaaS commercial team checks competitor offers manually and may ignore noisy alerts. A competitor price or packaging change before a sales review is the trigger. A forum account supplies anecdotal pain; current product documentation supplies a strong substitute. MKT03, MKT09–10.

**Proposed outcome.** One weekly shared-market brief with a short evidence-linked change list, explicit “no material changes observed” only for successfully checked sources, and a separate degraded-coverage list. Price hypothesis $79/month per team. Never equate an unchanged or failed fetch with absence of change.

**Substitutes and search.** Queries for “Visualping false alerts competitor pricing” surfaced existing semantic monitors and vendor-led comparison discussions. Opened Visualping already includes AI summaries and health/error notifications. [Visualping documentation](https://help.visualping.io/en/articles/10154433) The contribution cannot be merely “AI summarizes a diff.”

**Why now / what's new.** Transfer an analyst's short commercial review to one narrow market, retain a human decision on significance, and make uncertainty visible. Required access: permitted public pages and rights to summarize their facts. Acquisition: a precise sample via one allowed industry partner.

**Switching / defense.** Switching would require materially less customer reading and a useful decision, not more alerts. A consistently useful niche taxonomy and customer trust are plausible defenses; neither exists yet.

**Failure / test.** Prepare two historical sample briefs and ask five buyer teams to identify an action each would change. Later test $20 for a single brief, cap cash at $50 and preparation at four hours. Kill if no buyer names a decision or if broad individualized monitoring is required. No-response emergencies should exist; publication can wait, but lateness reduces paid value. Assume 100 minutes/week only for one shared brief, not bespoke coverage for every subscriber.

## I03 — An acceptance check for machine-written localization values

**Observed problem / buyer / trigger.** A developer or localization agency submits AI-generated translations through an API. Localazy's official submit endpoint documentation says it stores supplied values without running project QA and warns that HTTP 200 can still contain result:false. Separately, a historical placeholder false-positive report shows why naive validators also need review. MKT32–34. [API contract](https://localazy.com/docs/api/submit-translation) [user-reported edge case](https://discuss.localazy.com/t/bug-in-web-editor-parsing-d-placeholder/2255)

**Proposed outcome.** A narrow pre-submit adapter that checks placeholder sets, numeric literals, plural completeness and length, then records API acknowledgement. It blocks or queues uncertainty; it does not judge whether the translation is linguistically correct. Hypothetical $49 downloadable adapter plus fixtures for one stack.

**Substitutes and search.** Searched Localazy placeholder issues, QA and pricing; opened its built-in checks and API contract. Existing translation platforms and plain unit tests are direct substitutes. No claim that localization validation is new. A cross-path acceptance check is an adaptation of existing QA.

**Why now / access.** More automated generation creates more values submitted outside the UI, but prevalence and payment remain unknown. Need customer-approved source/target strings, an API contract and a test project; production write credentials are unnecessary for the first test. Acquisition: a precise documentation example or permitted integration marketplace entry.

**Switching / defense.** Less engineering effort to keep one path reliable; compatibility fixtures and version maintenance may retain value. The vendor could remove the gap quickly.

**Failure / cheapest falsifiable test.** In a local mocked endpoint, test 30 synthetic string cases including escaped percent signs and missing plurals; require every deliberate mismatch caught, no false pass on missing acknowledgements, and fewer than two false alarms. Then, only with authorization, seek two buyers who use that API path and one $49 purchase. Budget $50 and six hours. Kill if native QA already covers the customer's route or setup exceeds one hour per account. Technical success is not payment evidence.

## I04 — A replay pack for AI actions that may have succeeded before a timeout

**Observed problem / buyer / trigger.** AI agencies change models/prompts and fear repeated or malformed tool actions. The opened regression discussion is builder-led, so customer pain confidence is low; an independent issue demonstrates historical tooling maintenance rather than demand. MKT26, MKT35.

**Proposed outcome.** Synthetic fixtures for a specific noncritical workflow: a mock tool records a successful action, returns a timeout, and detects whether the agent retries with the same idempotency key or causes a duplicate. Include assertions for unauthorized actions and approval-state handling. Price hypothesis $49 per reusable pack.

**Substitutes/search.** “AI regression test pack agency,” Promptfoo issue searches and official pricing found free evaluation tooling. Langfuse provides tracing; ordinary code assertions remain sufficient for exact argument checks. [Promptfoo](https://www.promptfoo.dev/pricing/) [Langfuse](https://langfuse.com/pricing) We are not inventing replay or idempotency testing.

**Why now / access / distribution.** Agent tool use makes failure semantics consequential. Need a declared tool schema and synthetic data, not customer secrets. Sell a precisely documented workflow fixture via developer search and a permitted technical listing.

**Switching / defense.** A maintained library of realistic edge cases might save implementation time. Domain-specific correctness is the only meaningful advantage; a generic wrapper has none.

**Failure / test.** Build a tiny mock with ten seeded errors; require deterministic detection of all ten and no network side effects, then request one paid adaptation from a qualified agency. Cash cap $30, six-hour technical cap. Stop if every buyer needs custom orchestration or urgent CI support. A $49 artifact cannot support unlimited model upgrades. Model a 4–8-hour laptop incident week until observed otherwise.

## I05 — A missing-decision packet instead of another upload portal

**Observed problem / buyer / trigger.** Agencies may have files but lack decisions: which logo, who approves copy, which offer is current. The original webdesign discussion shows that some teams are perfectly served by Drive; other comments are product promotion. MKT11.

**Proposed outcome.** A packet that turns an approved scope into a short table of unresolved decisions, named approvers, permitted options and consequences of deferral. Silence retains “awaiting decision”; it never approves work. Offer an illustrative $99 setup of one packet and handoff checklist.

**Substitutes/search.** Searched client approval, locked content and agency portals. Content Snare and an opened Utin workflow guide already describe structured request/approval states. The guide is vendor evidence, not measured time savings. [Content Snare](https://contentsnare.com/pricing/) [approval workflow](https://utin.no/en/social-media/agency-client-content-portal/)

**Why now / new element.** AI can draft missing-decision questions from source material; the bounded product focuses on decisions, not collecting more files. Required access: client-approved scope and identified approver, with permission to process the information. Acquisition: one agency partner.

**Switching / defense.** A short packet might reduce meetings without replacing the agency's tools. Tested decision taxonomies for a specific project type could help; templates alone copy easily.

**Failure / cheapest test.** With permission, compare two similar past project briefs: count unanswered decisions and ask the agency to resolve them using the packet. Later sell one setup. Cap $25 and three preparation hours. Kill if it merely moves the same conversation elsewhere or requires owner participation in client calls. A setup service may be viable but is not automatically a 60-minute/week recurring business.

## I06 — Amendment-only tender digest for one permitted portal

**Observed problem / buyer / trigger.** Small suppliers report noisy notices and fragmented tender portals; a bidder already following a tender wants material amendments identified. This is a different buyer moment from broad lead discovery. MKT30.

**Proposed outcome.** Compare successive public documents for one portal and supply source-linked changed sections, timestamps, deadline fields and an explicit retrieval-health statement. No completeness or legal interpretation guarantee. Hypothetical $19 per tender.

**Substitutes/search.** Searched “tender amendment diff software” and “tender amendment compare alert software.” BidVeritas appeared as a close discovery lead; its underlying page returned only a JavaScript requirement, so its features and pricing were **not verified**. Generic website monitors and manual document comparison are confirmed adjacent substitutes. [unresolved competitor lead](https://www.bidveritas.com/)

**Why now / access.** Document comparison and summary drafting are cheaper; official feeds and portal terms still determine lawful/reliable access. Require public or explicitly authorized documents; no bypassing login or anti-bot barriers. Acquisition: an industry association listing after portal verification.

**Switching / defense.** A clear amendment-specific record might beat a noisy whole-page alert; the durable advantage would be portal reliability and bidder trust. Both are hard to earn.

**Failure / test.** Test ten historical document pairs locally, including altered deadlines and meaningless formatting changes. Cash cap $25, six hours; require all seeded deadline changes found and no claimed completeness. Before commercial work, ask whether customers tolerate 48-hour gaps. Reject for this owner's schedule if they need rapid notification or bid-deadline support. This urgency flaw makes I06 lower priority even if technical detection works.

## I07 — A compatibility pack for one operational spreadsheet's changing exports

**Observed problem / buyer / trigger.** Users repeatedly copy and refresh chained workbooks; a renamed or reformatted export can break an otherwise useful template. Buyer: a template vendor or business using the same export every month. Trigger: the source system changes its headers or types. MKT31.

**Proposed outcome.** A versioned input specification, fixture samples and a local “this export matches version X” check sold with one original template. Offer a one-time $29 pack; renewals only if actual valuable updates occur. Never silently rewrite formulas on unreviewed data.

**Substitutes/search.** “Spreadsheet schema drift validation tool” found SheetBrain's documented schema repair and Innovvo's browser-local saved import contracts. Both were opened. [SheetBrain](https://sheetbrain.app/docs/) [Innovvo](https://tools.innovvohq.online/tools/csv-cleanup-schema-repair) Generic schema detection is not new.

**Why now / adaptation.** AI-assisted support can explain failures, but deterministic checks should decide compatibility. The adaptation is packaging tested compatibility maintenance with a narrowly useful licensed artifact. Need rights to the template and synthetic examples of the export schema. Acquisition: the existing template's marketplace; no existing buyer base is assumed.

**Switching / defense.** A buyer might prefer reliable use over a prettier template. Test fixtures, clear migration notes and trustworthy support can accumulate value; a generic AI formula generator cannot be the moat.

**Failure / cheapest test.** Use 20 synthetic export variants and three permitted historical schemas; measure whether users understand failures without help. Later ask a vendor for one $29 purchase. Cash cap $25, six hours. Kill if ten-minute support per buyer recurs or upstream changes require constant rework. This could improve N03; it does not justify building both businesses at once.

## I08 — A source-evidence packet for non-regulated PDF extraction

**Observed problem / buyer / trigger.** Teams need structured fields from recurring documents and must verify them. Docparser establishes an existing paid extraction offer, not demand for a new provenance layer. Buyer: a small non-regulated operations team; trigger: a batch of supplier specification PDFs, excluding medical, legal or safety-critical interpretation.

**Proposed outcome.** A CSV plus field-to-page references and cropped evidence links for a fixed schema, with “not found” and “ambiguous” kept separate. Deliver a review packet, not a claim that extraction is correct. Hypothetical $49 per 20-document batch.

**Substitutes/search.** “PDF extraction source evidence coordinates” found the EviTrace developer's provenance design in clinical research; opened it as an adjacent technical example only. Its guarantees, benchmark numbers and license claim were not independently validated. [Docparser](https://docparser.com/pricing) [adjacent design](https://soroushdianaty.com/projects/evitrace/)

**Why now / access.** Cheap OCR and multimodal extraction make draft fields affordable, but source citations can still point to the wrong evidence. Need documents the customer may share, a fixed schema, readable files and a retention policy. Acquisition: one industry-specific operations partner.

**Switching / defense.** Faster human verification could justify an add-on where existing extraction requires opening every PDF. Domain templates and a corrected error corpus might help; generation technology is readily copied.

**Failure / cheapest test.** On 20 synthetic/nonconfidential PDFs, compare manual review time with and without the packet. Require every extracted field to have a valid source reference, zero fabricated values and at least 30% reviewer-time reduction. Those are gates, not predicted results. Budget $50 and six hours. Stop if evidence verification erases the savings or customers need confidentiality commitments beyond the owner's capacity. No paid test was run.

## What the invention exercise changed

1. It removed the claim that local/private product CSV preflight is an overlooked empty market. Multiple near-exact tools exist, including free two/three-file supplier analysis.
2. It exposed a specific localization API acceptance gap that deserves a small technical test, without confusing that gap with commercial demand.
3. It showed that spreadsheet health checks, approval states and provenance extraction already have close substitutes. Combining them differently may be useful, but combination alone is not evidence customers will switch.
4. It rejected urgency as a hidden cost: tender amendment monitoring can be technically attractive and still wrong for someone unavailable during work.
5. It preserved human judgment where it could earn its time: commercial relevance, acceptance criteria and exception review. Each retained decision needs an owner-minute measurement.

Cheapest remaining commercial check: a buyer comparing the proposed outcome with their current process and a free substitute, then making a real bounded purchase. Cheapest remaining technical check: one specific capability with synthetic fixtures and explicit failure criteria. Neither should be inflated into proof of sustainable, unattended profit.
