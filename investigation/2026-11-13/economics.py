"""Transparent scenario arithmetic, not a demand forecast. Standard library only."""
from dataclasses import dataclass, asdict, replace
from decimal import Decimal, ROUND_CEILING, ROUND_HALF_UP
from pathlib import Path
import json

D = Decimal
ROOT = Path(__file__).resolve().parent


@dataclass(frozen=True)
class Scenario:
    name: str
    orders: int
    price: D
    fee_rate: D
    fee_fixed: D
    refund_rate: D
    delivery_cash: D
    acquisition_cash: D
    fixed_cash: D
    delivery_hours_each: D
    sales_hours: D
    admin_hours: D
    setup_hours: D


def calculate(s):
    contribution = s.price * (1 - s.fee_rate - s.refund_rate) - s.fee_fixed - s.delivery_cash - s.acquisition_cash
    revenue = s.orders * s.price
    variable = s.orders * (s.price - contribution)
    surplus = s.orders * contribution - s.fixed_cash
    hours = s.orders * s.delivery_hours_each + s.sales_hours + s.admin_hours
    total_hours = hours + s.setup_hours
    return {
        "contribution_each": contribution,
        "revenue": revenue,
        "variable_costs_and_refund_allowance": variable,
        "operating_surplus_before_owner_pay_and_tax": surplus,
        "operating_hours": hours,
        "setup_hours": s.setup_hours,
        "all_hours": total_hours,
        "surplus_per_operating_hour": surplus / hours if hours else None,
        "surplus_per_all_hours": surplus / total_hours if total_hours else None,
        "economic_surplus_at_20_per_operating_hour": surplus - hours * 20,
        "economic_surplus_at_30_per_operating_hour": surplus - hours * 30,
    }


BASE = Scenario("Support: 2 first direct pilots", 2, D("149"), D(".10"), D(".50"), D(".05"), D("5"), D("10"), D("15"), D("4"), D("6"), D("1"), D("6"))
SCENARIOS = [
    BASE,
    replace(BASE, name="Support: zero sales", orders=0, sales_hours=D("12"), admin_hours=D("2")),
    replace(BASE, name="Support: 1 slow direct pilot", orders=1, delivery_hours_each=D("8"), sales_hours=D("12"), admin_hours=D("2")),
    replace(BASE, name="Support: 4 efficient direct orders", orders=4, delivery_hours_each=D("3"), sales_hours=D("4"), admin_hours=D("2"), setup_hours=D("0")),
    replace(BASE, name="Support: price reduced to $99", price=D("99")),
    replace(BASE, name="Support: 2 Fiverr pilots", fee_rate=D(".23"), fee_fixed=D("0"), acquisition_cash=D("0")),
    replace(BASE, name="Support: 15% refund stress", refund_rate=D(".15")),
    replace(BASE, name="CSV: 2 first direct jobs", price=D("99"), delivery_hours_each=D("3"), sales_hours=D("3"), admin_hours=D("1"), setup_hours=D("4")),
    Scenario("Template: 20 sales, acquisition works", 20, D("29"), D(".129"), D(".80"), D(".05"), D("1"), D("6"), D("15"), D(".15"), D("12"), D("1"), D("16")),
    Scenario("Template: same sales, slow acquisition", 20, D("29"), D(".129"), D(".80"), D(".05"), D("1"), D("6"), D("15"), D(".15"), D("40"), D("1"), D("16")),
    Scenario("POD: 10 orders", 10, D("35"), D(".12"), D(".50"), D(".08"), D("23"), D("5"), D("10"), D(".30"), D("8"), D("2"), D("15")),
    Scenario("Dropship: 10 orders, $12 cash CAC", 10, D("40"), D(".04"), D(".30"), D(".10"), D("20"), D("12"), D("39"), D(".50"), D("8"), D("2"), D("20")),
    Scenario("Dropship: 10 orders, $18 cash CAC", 10, D("40"), D(".04"), D(".30"), D(".10"), D("20"), D("18"), D("39"), D(".50"), D("8"), D("2"), D("20")),
    Scenario("Dropservice: 2 orders, $60 contractor", 2, D("149"), D(".10"), D(".50"), D(".05"), D("65"), D("10"), D("15"), D("3"), D("5"), D("1"), D("6")),
    Scenario("Dropservice: contractor + $40 rework", 2, D("149"), D(".10"), D(".50"), D(".05"), D("105"), D("10"), D("15"), D("4"), D("5"), D("1"), D("6")),
]


def money(x):
    return "n/a" if x is None else f"{x.quantize(D('.01'), rounding=ROUND_HALF_UP):,.2f}"


def validate():
    for s in SCENARIOS:
        assert isinstance(s.orders, int) and s.orders >= 0
        assert 0 <= s.fee_rate < 1 and 0 <= s.refund_rate <= 1
        for k, value in asdict(s).items():
            if isinstance(value, D):
                assert value >= 0, (s.name, k)
        r = calculate(s)
        assert r["revenue"] == r["variable_costs_and_refund_allowance"] + s.fixed_cash + r["operating_surplus_before_owner_pay_and_tax"]
        assert r["all_hours"] == r["operating_hours"] + s.setup_hours
    b = calculate(BASE)
    assert b["contribution_each"] == D("111.15")
    assert b["operating_surplus_before_owner_pay_and_tax"] == D("207.30")
    assert calculate(replace(BASE, orders=0))["operating_surplus_before_owner_pay_and_tax"] == -BASE.fixed_cash
    assert calculate(replace(BASE, refund_rate=D(".15")))["contribution_each"] < b["contribution_each"]
    assert calculate(replace(BASE, sales_hours=D("12")))["surplus_per_operating_hour"] < b["surplus_per_operating_hour"]
    assert sum([25, 25, 60, 40, 150, 50]) == 350


def main():
    validate()
    result = [{"inputs": asdict(s), "results": calculate(s)} for s in SCENARIOS]
    (ROOT / "economics.json").write_text(json.dumps(result, indent=2, default=str) + "\n", encoding="utf-8")
    lines = [
        "# Economics: conditional arithmetic, not forecasts", "",
        "Generated by `python investigation/2026-11-13/economics.py`. Decision date: 13 November 2026. All amounts USD. No scenario volume, conversion rate, efficiency improvement or price acceptance has been validated.", "",
        "Operating surplus = collected-price assumption minus modeled fees, refunds, delivery cash, acquisition cash and fixed cash; **before owner compensation, income tax and any output VAT liability**. If the customer price includes output VAT, reduce the net revenue first. Setup is shown separately and included in the all-hours return. Economic surplus subtracts an illustrative owner wage; it is not another cash payment.", "",
        "Expected refunds are a planning expense, not the full liquidity required for a refund. Gross revenue includes the orders later represented by that allowance. Processing is conservatively charged on all orders; any refundable fees are not credited. Cash acquisition and owner selling hours are both counted. If the same expense is in fixed costs, do not count it again as per-order delivery cash.", "",
        "| Scenario | Revenue | Contribution/order | Operating surplus | Operating h | Setup h | $/operating h | $/all h | Economic surplus @ $20/h* | @ $30/h* |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for s in SCENARIOS:
        r = calculate(s)
        vals = [r["revenue"], r["contribution_each"], r["operating_surplus_before_owner_pay_and_tax"], r["operating_hours"], s.setup_hours, r["surplus_per_operating_hour"], r["surplus_per_all_hours"], r["economic_surplus_at_20_per_operating_hour"], r["economic_surplus_at_30_per_operating_hour"]]
        lines.append("| " + s.name + " | " + " | ".join(money(v) for v in vals) + " |")
    lines += [
        "", "*Economic surplus columns value operating hours only. For a full project view, also subtract setup hours × the selected hourly value. The all-hours cash return already includes setup.", "",
        "## Assumptions and fee provenance", "",
        "- Direct support/CSV: 10% + $0.50 collection/FX allowance, 5% refunds, $5 variable delivery tools, $10 cash acquisition/order, $15 fixed. PayPal Israel publishes multiple components; this is a conservative scenario allowance, not its tariff or a guaranteed ceiling. Actual accounts, country/currency mix, disputes and VAT treatment need checking.",
        "- Fiverr: documented 20% seller deduction plus an **assumed 3%** withdrawal/FX allowance; 5% refunds, $5 delivery cash and $15 fixed. Zero paid acquisition spend does not remove the modeled six selling hours. No guarantee of impressions or orders. Clearing time creates a cash-flow delay.",
        "- Template: Gumroad direct card assumption 12.9% + $0.80; 5% refunds, $1 delivery/support cash allowance, $6 cash acquisition and $15 fixed. Price $29. Owner time adds 0.15h/order, 12h selling and 1h admin; stress uses 40h selling. The $6 acquisition rate is unverified. Discover's 30% pricing is a different channel and is not used here.",
        "- POD: $35 price; $17 production + $6 shipping; assumed composite 12% + $0.50 platform/payment fees, 8% refund allowance, $5 acquisition and $10 fixed. These are illustrative quotes **not obtained from a supplier** and are not a universal Etsy fee schedule.",
        "- Dropshipping: $40 price; $14 goods + $6 shipping; assumed 4% + $0.30 collection, 10% refunds, $12 or $18 cash CAC, $39 fixed. These are assumptions, not Shopify/processor quotes. Advertising tests can lose money before any ten-order batch exists.",
        "- Dropservicing: $149 price, same direct collection/refund allowances, $60 assumed contractor + $5 delivery tools; stress adds $40 rework/order. Founder briefing/review/communications and selling hours remain. No contractor quote or hire exists.", "",
        "Source details: [S19–S21, S27–S33 in the evidence ledger](sources.md). Exact inputs are in [economics.json](economics.json). Every scenario is reproducible from the source script.", "",
        "## Income targets are illustrations, not the owner's stated goal", "",
        "Using $111.15 direct contribution/order and $15 fixed cash, with **unproven** recurring efficiency of 3 delivery hours/order, 1 sales hour/order and 2 admin hours/month:", "",
        "| Desired monthly operating surplus | Required orders | Resulting surplus | Owner hours/month, excluding setup | Approx. hours/week (4.33 weeks) |",
        "|---|---:|---:|---:|---:|",
    ]
    c = calculate(BASE)["contribution_each"]
    for goal in [D("300"), D("1000")]:
        n = int(((goal + BASE.fixed_cash) / c).to_integral_value(rounding=ROUND_CEILING))
        h = D(n * 4 + 2)
        lines.append(f"| ${money(goal)} | {n} | ${money(n*c-BASE.fixed_cash)} | {money(h)} | {money(h/D('4.33'))} |")
    lines += [
        "", "Acquisition could take much longer than one hour/order; refunds or pricing pressure increase the requirement. Two extra selling hours/order add 20 hours/month at ten orders. Repeat buying is not assumed, and no recurring subscription revenue is implied.", "",
        "## Other sensitivity checks", "",
        "- At $149 and 10% + $0.50 collection, 5% refunds and $5 delivery cash, contribution before cash acquisition is $121.15. To retain $20/hour across five operating hours, the remaining cash acquisition ceiling is $21.15 before allocating fixed costs. This is a break-even constraint, not evidence that customers can be acquired at that price.",
        "- Content ad sensitivity: $1,000 at a hypothetical $2/$5/$10 net RPM needs 500,000/200,000/100,000 monetized views. Eligibility and actual RPM are unknown; zero ad income is the starting case.",
        "- Service funnel sensitivity: 10,000 relevant video views × 1% clicks × 2% click-to-purchase yields two orders. At 0.2% clicks and 1% purchase it yields 0.2 expected orders, not a guaranteed fractional sale. Neither rate is measured.",
        "- Hosted chatbot illustration: $49 revenue − $15 usage/hosting − $5 collection allowance = $29 before acquisition/refunds/support/tax. One hour valued at $30 makes this negative even before setup. This is not a project-specific operating quote.",
        "- POD working cash: ten orders at $23 supplier production/shipping need $230 before considering payout timing, acquisition or returns. Dropshipping at $20 fulfillment plus $12 acquisition needs $320 for ten orders, before fixed fees/returns. With a $350 loss ceiling, holds and one incident can consume the reserve.", "",
        "## Checks performed", "",
        "The generator checks cost/revenue reconciliation for every scenario, nonnegative inputs, hour reconciliation, the independently calculated first-pilot result, zero-sale fixed loss, the direction of refund/time sensitivity and the $350 budget sum. These checks validate arithmetic and bookkeeping only, not the assumptions or future business performance.", "",
    ]
    (ROOT / "economics.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Validated and generated {len(SCENARIOS)} scenarios: economics.md and economics.json")


if __name__ == "__main__":
    main()
