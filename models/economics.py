"""Conditional business arithmetic, not forecasts. Python standard library only.

Run from repo root: python models/economics.py
All dollar values USD; revenue excludes sales tax. See assumptions.md.
"""
from dataclasses import dataclass, asdict, replace
from pathlib import Path
import json
import math

WEEKS = 52 / 12
OWNER_HOURLY = 30


@dataclass(frozen=True)
class Case:
    business: str
    scenario: str
    units: int
    price: float
    fee_rate: float
    fee_flat: float
    refund_rate: float
    variable: float
    fixed: float
    cac: float
    churn: float  # monthly; zero for one-time sales
    recurring: bool
    scheduled_weekly: float
    jobs_per_unit: float
    review_minutes: float  # per job, including previews
    exception_rate: float  # per job
    exception_minutes: float
    support_rate: float  # tickets/unit/month
    support_minutes: float
    onboarding_minutes: float  # per new customer incl sales correspondence
    capacity_units: int


def calculate(c: Case):
    if c.units < 0 or any(not 0 <= x <= 1 for x in
        (c.fee_rate, c.refund_rate, c.churn, c.exception_rate, c.support_rate)):
        raise ValueError("Invalid units or rate")
    revenue = c.units * c.price
    fees = c.units * (c.price * c.fee_rate + c.fee_flat)
    refunds = revenue * c.refund_rate  # no recovered fee credit assumed
    delivery = c.units * c.variable
    new_customers = c.units * c.churn if c.recurring else c.units
    acquisition = new_customers * c.cac  # steady-state replacements only
    contribution = revenue - fees - refunds - delivery
    operating = contribution - acquisition - c.fixed
    jobs = c.units * c.jobs_per_unit
    variable_minutes = (jobs * (c.review_minutes + c.exception_rate * c.exception_minutes)
        + c.units * c.support_rate * c.support_minutes
        + new_customers * c.onboarding_minutes)
    weekly = c.scheduled_weekly + variable_minutes / WEEKS
    labor = weekly * WEEKS / 60 * OWNER_HOURLY
    net_unit = c.price * (1-c.fee_rate-c.refund_rate) - c.fee_flat - c.variable
    retained_unit = net_unit - c.cac * (c.churn if c.recurring else 1)
    return {"business": c.business, "scenario": c.scenario, "units": c.units,
        "gross_revenue": revenue, "fees": fees, "refund_allowance": refunds,
        "variable_delivery": delivery, "contribution": contribution,
        "contribution_margin": contribution/revenue if revenue else None,
        "new_customers_per_month": new_customers, "acquisition": acquisition,
        "fixed": c.fixed, "operating_profit": operating,
        "weekly_owner_minutes": weekly, "owner_labor": labor,
        "economic_profit": operating-labor, "jobs_monthly": jobs,
        "unit_after_replacement_acquisition": retained_unit,
        "break_even_units": math.ceil(c.fixed/retained_unit) if retained_unit>0 else None,
        "within_volume_capacity": c.units <= c.capacity_units,
        "initial_acquisition_cash": c.units * c.cac if c.recurring else 0}


BASE = [
    Case("F1 Supplier preflight", "base", 25, 39, .10, .5, .03, 1.2, 65,
         35, .05, True, 45, 4, 0, .04, 8, .08, 12, 12, 100),
    Case("F2 Weekly watchlist", "base", 12, 79, .10, .5, .04, 8, 55,
         70, .06, True, 40, WEEKS, 2, .10, 8, .10, 12, 15, 25),
    Case("F3 Template + content", "base", 20, 29, .129, .8, .04, .1, 15,
         6, 0, False, 75, 1, 0, .04, 8, .10, 8, 0, 100),
    Case("F4 Monthly report", "base", 5, 149, .10, .5, .03, 15, 45,
         90, .06, True, 45, 1, 12, .20, 20, .15, 15, 20, 20),
]


def scenarios():
    for b, low_n, high_n in zip(BASE, (5,3,2,1), (75,25,80,12)):
        yield replace(b, scenario="conservative", units=low_n, cac=b.cac*2,
            churn=b.churn*1.6, refund_rate=b.refund_rate*2,
            exception_rate=min(1,b.exception_rate*2), support_rate=b.support_rate*1.5,
            variable=b.variable*1.5)
        yield b
        yield replace(b, scenario="optimistic", units=high_n, cac=b.cac*.7,
            churn=b.churn*.7, exception_rate=b.exception_rate*.6,
            variable=b.variable*.85, fixed=b.fixed+20)


def targets(b):
    out = []
    for profit in (1000, 5000):
        retained = calculate(b)["unit_after_replacement_acquisition"]
        n = math.ceil((profit+b.fixed)/retained)
        r = calculate(replace(b, units=n))
        r["target"] = profit
        r["warning"] = "Algebra at base costs; not a scalable promise. Capacity/traffic/hosting revalidation required."
        out.append(r)
    return out


def stress(b):
    variants = [
        replace(b, scenario="half volume", units=b.units//2),
        replace(b, scenario="double CAC", cac=b.cac*2),
        replace(b, scenario="double delivery cost", variable=b.variable*2),
        replace(b, scenario="double churn", churn=b.churn*2),
        replace(b, scenario="12% refunds", refund_rate=.12),
        replace(b, scenario="compound downside", units=b.units//2, cac=b.cac*2,
            churn=b.churn*2, variable=b.variable*2, refund_rate=.12,
            exception_rate=min(1,b.exception_rate*3), support_rate=min(1,b.support_rate*2)),
        replace(b, scenario="one outage month", refund_rate=.25,
            scheduled_weekly=b.scheduled_weekly+180/WEEKS),
    ]
    return [calculate(v) for v in variants]


def main():
    folder = Path(__file__).resolve().parent
    data = {"label":"Illustrative conditional scenarios; no measured conversions or revenue",
        "weeks_per_month":WEEKS, "owner_usd_per_hour":OWNER_HOURLY,
        "inputs":[asdict(c) for c in scenarios()],
        "scenarios":[calculate(c) for c in scenarios()],
        "targets":[t for b in BASE for t in targets(b)],
        "stress":[s for b in BASE for s in stress(b)]}
    (folder/"results.json").write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
    lines=["# Reproducible conditional economics", "", "Generated by `python models/economics.py`. USD/month except owner minutes/week. These are assumptions, not forecasts. Revenue excludes tax. Owner labor is $30/hour. Steady-state subscriptions include replacement acquisition; initial growth cash is separate.","",
        "| Business/scenario | Units | Revenue | Contribution | Acquisition | Fixed | Operating profit | Minutes/week | Economic profit |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for r in data["scenarios"]:
        lines.append(f'| {r["business"]} / {r["scenario"]} | {r["units"]} | ${r["gross_revenue"]:,.0f} | ${r["contribution"]:,.0f} | ${r["acquisition"]:,.0f} | ${r["fixed"]:,.0f} | ${r["operating_profit"]:,.0f} | {r["weekly_owner_minutes"]:.0f} | ${r["economic_profit"]:,.0f} |')
    lines += ["", "## Profit targets at base unit costs", "", "Targets include replacement acquisition; no growth or scale-cost uplift. Capacity violations invalidate this plan until redesigned.", "", "| Business | Target | Units | Minutes/week | Within stated volume cap? | Initial acquisition cash |", "|---|---:|---:|---:|---|---:|"]
    for r in data["targets"]:
        lines.append(f'| {r["business"]} | ${r["target"]:,} | {r["units"]} | {r["weekly_owner_minutes"]:.0f} | {r["within_volume_capacity"]} | ${r["initial_acquisition_cash"]:,.0f} |')
    lines += ["", "## Stress tests", "", "| Business | Change | Operating profit | Minutes/week | Economic profit |", "|---|---|---:|---:|---:|"]
    for r in data["stress"]:
        lines.append(f'| {r["business"]} | {r["scenario"]} | ${r["operating_profit"]:,.0f} | {r["weekly_owner_minutes"]:.0f} | ${r["economic_profit"]:,.0f} |')
    (folder/"results.md").write_text("\n".join(lines)+"\n",encoding="utf-8")


if __name__ == "__main__":
    main()
