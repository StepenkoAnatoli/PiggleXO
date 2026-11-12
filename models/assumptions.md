# Model definitions, assumptions, and cash discipline

Research date: **12 November 2026**. All amounts USD. Read alongside [generated results](results.md), [inputs and formulas](economics.py), and [machine-readable results](results.json). These conditional cases are not demand forecasts, confidence intervals, or probabilities of success. No customer has been acquired and no income has been observed in this investigation.

## Formulas and accounting boundary

One month = 52/12 weeks. N is the SAME number of paying accounts (F1/F2/F4) or new orders (F3) used for both revenue and work. P is price before sales tax. Customer sales tax is not revenue. Monthly gross revenue = N × P. Fees = N × (P × fee rate + fixed transaction fee). Refund/chargeback allowance = gross revenue × allowance rate; conservatively no fee recovery. Variable delivery includes processing, storage, failed attempts and, for F4, contractor work. Contribution = revenue − fees − allowance − variable delivery. Contribution margin = contribution / revenue.

Monthly acquisition cash = N × churn × CAC for an existing stable subscriber book, or N × CAC for one-off products. Operating profit = contribution − acquisition cash − fixed costs, before owner compensation and income tax. Economic profit = operating profit − owner hours × $30. Substitute the owner's actual opportunity cost; at $15 and $60/hour F1 base economic profit becomes about $631 and $432 respectively. Break-even volume = ceiling(fixed / unit contribution after replacement acquisition). Target volume = ceiling((target profit + fixed)/same unit contribution).

Monthly owner minutes = scheduled weekly minutes × 52/12 + N × jobs/account × (review minutes/job + exception rate × minutes/exception) + N × support rate × minutes/ticket + new customers × onboarding/sales minutes. Work does not disappear because software fulfills an order. Fixed time includes acquisition management, notification reading, quality checks, maintenance, accounting, and planned reviews. Exceptions are additive. An incident month adds 180 minutes once, shown averaged over its weeks; in reality that time can arrive in one bad week.

Cash CAC excludes owner time because owner acquisition time is counted separately; if a channel demands more owner outreach, add minutes rather than pretending CAC bought that work. Subscription onboarding includes sales correspondence only at the assumed replacement volume. Initial acquisition is a separate launch project. The model DOES NOT claim that 15 acquisition minutes/week can recruit a book of 25 customers from zero.

## Base input register

| Input | F1 supplier-specific preflight | F2 weekly change watchlist | F3 craft-event template/content | F4 fixed monthly operational report |
|---|---:|---:|---:|---:|
| Price; volume | $39; 25 accounts | $79; 12 accounts | $29; 20 orders | $149; 5 accounts |
| Fee planning reserve | 10% + $0.50 | 10% + $0.50 | 12.9% + $0.80 | 10% + $0.50 |
| Refund/chargeback allowance | 3% | 4% | 4% | 3% |
| Delivery cost per unit/month | $1.20 | $8 | $0.10 | $15 |
| Fixed/month | $65 | $55 | $15 | $45 |
| CAC; monthly churn | $35; 5% | $70; 6% | $6/order; n/a | $90; 6% |
| Jobs/account/month | 4 | 52/12 | 1 download | 1 |
| Review per job | 0, plus fixed random-sample review | 2 min | 0, published version pre-reviewed | 12 min |
| Exception rate; handling | 4%; 8 min | 10%; 8 min | 4%; 8 min | 20%; 20 min |
| Support rate; handling | 8%/account-month; 12 min | 10%; 12 min | 10%/order; 8 min | 15%; 15 min |
| Acquisition/onboarding per new customer | 12 min | 15 min | 0, self-service | 20 min |
| Scheduled weekly time | 45 min | 40 min | 75 min | 45 min |
| Volume cap before redesign | 100 accounts | 25 accounts | 100 orders/month | 20 accounts |

All prices, CACs, conversions, volumes, churn, support frequencies, capacities and minutes in this table are **hypothesized**, not industry benchmarks. The capacities are chosen pilot safety limits, not measured server limits. F1's 4 files/month is an offer ceiling. Extra files are rejected/queued, not silently included. F2 includes only a bounded shared niche watchlist, not unlimited sites per customer. F4 covers one stable customer-owned source, no bookkeeping, financial advice, or executive consulting.

F1 fixed $65 = hosting/backups $20, monitoring/email $10, accounting/admin allocation $15, maintenance/tool contingency $20. F2 $55 = managed monitoring allocation $25, delivery $10, admin $15, contingency $5. F3 $15 = domain/tool/admin allocation; no paid video generation assumed. F4 $45 = reporting/hosting $15, delivery $5, admin $15, contingency $10. These are spending ceilings/estimates, not purchased vendor bundles. Fixed allocations may not cover local registration, mandatory insurance, or country-specific accounting. Those remain country-dependent launch gates, not assumed zero forever.

F1 variable $1.20 includes $0.80 processing/storage plus $0.40 failed-run/AI-explanation contingency; deterministic validation needs no inference. F2 $8 includes bounded source checks, extraction retries, and a small narration allowance. F4 $15 includes $10 contractor verification (20 min at $30/h), $3 processing and $2 failed-job reserve. Owner review and contractor supervision remain in the time model; the contractor is a hypothetical purchased service, not sourced or hired. No COGS/shipping/inventory is relevant to these digital finalists. Physical-commerce exposure is assessed separately in the landscape; its absence here is a business selection, not an omitted cost.

F1/F2/F4's 10%+$0.50 is a conservative planning placeholder including payment, FX/payout, and small indirect-tax-related fee effects, NOT a quoted universal processor rate. Lemon Squeezy's base rate is 5%+$0.50; extras include international/PayPal/subscription charges and payout costs. Fees can apply to tax-inclusive checkout totals. Model actual country/currency/tax mix before launch. Services cannot simply use Lemon Squeezy: its prohibited-products page excludes services. For the supervised report pilot use an eligible invoice/payment method after verifying owner eligibility. F3 uses Gumroad's detailed direct-card fee, not just its headline. See FIN01–FIN03 and FIN07–FIN10 in [finance sources](../research/finance-sources.json).

F3's 75 scheduled minutes/week comprise research/production 30, preview/scheduling 9, acquisition analytics 10, product quality/version checks 10, bookkeeping/refund-balance reconciliation 10, and two short checks totaling 6. Order-specific support/failed delivery is added by the formula. F2's two review minutes per recipient per issue are a conservative delivery/relevance check in addition to shared editorial work; it is not unlimited bespoke monitoring. F4 is one stable source contract with at most two agreed export files, not two arbitrary systems.

## Scenarios and demand needed

Conservative cases halve neither costs nor scheduled work: N=(5,3,2,1), CAC doubles, churn ×1.6, refunds and exceptions double, support ×1.5, variable costs ×1.5; fixed costs stay. Optimistic N=(75,25,80,12), CAC/churn ×0.7, exceptions ×0.6, variable costs ×0.85, fixed +$20; prices and scheduled editorial effort stay. These are deliberately conditional combinations, not statistical percentile outcomes. Zero revenue is plausible for the first 60–90 days; at N=0 the owner still pays fixed costs and spends scheduled minutes.

| Model | Base operating break-even | Acquisition needed at base volume | At $1,000 monthly operating target | At $5,000 target |
|---|---:|---|---|---|
| F1 | 3 accounts | 1.25 replacements/month; initial 25 acquisitions | 35 accounts, 1.75 replacements; initial cash CAC $1,225 | 167 accounts: exceeds capacity and 120 min/week |
| F2 | 1 account | 0.72 replacements/month; initial 12 | 20 accounts, 1.2 replacements; initial cash CAC $1,400 | 92 accounts: rejected at modeled workload |
| F3 | 1 order | 20 new orders every month | 60 new orders/month, assumed $360 cash acquisition | 292 orders: exceeds capacity/workload and unproven traffic |
| F4 | 1 account | 0.30 replacements/month; initial 5 | 10 accounts, 0.6 replacements; initial cash CAC $900 | 47 accounts: rejected at modeled workload |

At an assumed 2% qualified-visitor purchase rate, F3 needs 1,000 qualified landing visits/month for 20 orders, 3,000 for $1,000 profit, and 14,600 for $5,000. At 1% content-to-site click-through those require 100,000, 300,000, and 1.46 million relevant impressions. Those reach figures are NOT established from zero audience. F3 $6 blended cash CAC implies $0.12 per qualified visit if all acquisition is paid at 2% conversion; otherwise organic effort must create some visits. At $0.50/click and 2% conversion, cash CAC is $25 and unit contribution becomes negative before fixed costs. Price $19 at base F3 volume and same costs lowers operating profit from $329 to $163; at $9 it is negative. The $29 premium needs proof against cheaper/free alternatives.

For F1, assuming 10% of genuinely qualified agency conversations become paying accounts, 25 accounts require 250 conversations. At just 6 owner minutes each, that is 25 launch hours before setup/fulfillment. Even the $1,000 target's replacement acquisition needs ~18 conversations/month, approximately 25 min/week. That already exceeds the base acquisition allocation of 15 minutes/week. Thus at that target either self-service acquisition must prove itself or owner minutes must rise by at least 10/week; the displayed 68 minutes is not a demonstrated whole-business workload. At $5,000 the same channel adds roughly 116 min/week to acquisition alone. Similar sales constraints apply to F2/F4. Cash CAC and traffic assumptions need separate real measurements.

At F1 base, the same conversation assumptions require 17.3 acquisition minutes/week, about 2.3 more than the 15-minute allocation: channel-adjusted total ~64 minutes. At 35 accounts, ~78 minutes including the extra 9.2. At the optimistic scenario's 75 accounts and 3.5% churn, conversations require ~36.3 minutes/week, adding ~21.3 for a total ~103 minutes. These are sensitivity calculations, not evidence that those agencies can be reached.

## Cash, payout delays, and startup budgets

Accrued revenue is not a bank balance. A one-month-lag illustration at F1 base: $975 sales, $110 fees, $29.25 expected refunds, $30 delivery, $43.75 replacement acquisition and $65 fixed gives $697 operating profit. The processor receivable after fees/refund allowance is $835.75, not withdrawable cash. If no payout arrives this month, operating bank outflow is $138.75. If $835.75 settles next month, cash still must fund current obligations and reserves. A separate $100 liquidity floor is withheld from available cash; it is not deducted again as an expense. Initial CAC $875 and setup expense are separate; neither is hidden in steady-state margin. For an actual new cohort replace churn-based acquisition with actual new customers × CAC; do not charge full initial CAC AND replacements twice on the same customers.

Lemon Squeezy documents twice-monthly creation, a 13-day hold, 1–5 day bank arrival and $50 minimum. Its page also has a weekly rollover phrase inconsistent with twice-monthly scheduling; assume slower cash until account confirmation. Gumroad documents a minimum seven-day hold on weekly/monthly/quarterly schedules and country-dependent processing; do not assume new-account instant payouts. Account reviews/holds can be longer than normal. The pilot therefore budgets for 60 days without revenue and at least 30 days without payout, with no owner withdrawals. Minimum payouts can make tiny sales balances inaccessible longer. Cash export/reconciliation is a weekly task.

| Available startup capital | Setup cash cap | Demand-test cash cap | 60-day operating budget | Refund/payout liquidity reserve | Untouched | Maximum nonreserve pilot spend | Worst ring-fenced cash at risk |
|---|---:|---:|---:|---:|---:|---:|---:|
| $250 | $0 | $50 | $100 | $100 | $0 | $150 | $250 |
| $1,000 | $50 | $150 | $130 | $170 | $500 | $330 | $500 |
| $5,000 | $100 | $150 | $130 | $170 | $4,450 | $380 | $550 |

The $250 plan is **manual/local only**, operating cap $50/month; it does not buy the modeled $65/month hosted F1 stack. With $0 revenue and no demand/ad spend, operating runway from that $100 allocation is two months; once exhausted, stop, do not invade refund reserve. $1,000/$5,000 plans also fund two months, not an obligation to keep spending all capital. Larger capital does not cure weak demand. Do not buy contractors, annual subscriptions, or a hosted integration before the comparison test. Ring-fenced loss assumes bounded delivery and no production access; it is not a legal cap on all possible liability. Country-dependent setup costs can make the $250 plan infeasible. Owner setup time at $30/h is an additional economic investment, not cash: 12–20h validation = $360–600; hosted build 35–60h = $1,050–1,800.

These capital allocations apply to F1 comparisons. The selected F3 experiment has a separate, smaller allocation in [validation plan](../plans/validation.md); do not add both plans or run them concurrently. A bank reserve is not automatically an available processor refund balance: Gumroad specifically requires sufficient dashboard balance. Confirm the actual refund funding path before accepting payment.

## Stress and workload interpretation

Generated stress cases include lower volume, doubled CAC, doubled delivery cost, doubled churn, 12% refunds, combined downside and one 180-minute outage with 25% refunds. For F1 base, the combined case produces only ~$181 operating/$42 economic profit. It still assumes 12 customers already exist; it is NOT the worst possible launch result. A platform/payment restriction can reduce new sales to zero. At zero customers F1 loses $65/month before labor; a retained 25-customer book that must be fully refunded can lose more because fees, support and fixed costs remain. Pause checkout, retain records, stop new commitments, and fulfill/refund according to applicable obligations. No stable-margin scenario establishes protection from account loss.

Most base cases sit in the **60–120 minute tier**, not the preferred <=60. F1 approximately fits <=60 only below ~23 accounts with these assumptions and excludes initial growth. At 60 minutes cap, sacrifice acquisition speed or take fewer accounts; do not remove review from the model. The next tier buys useful editorial judgment, false-positive review and a weekly acquisition experiment. Test its marginal value by tracking preventable error cost, saved customer review minutes, conversion and repeat use—not by assuming all human work is waste.
