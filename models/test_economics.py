import unittest
from dataclasses import replace
from economics import BASE, calculate, targets, WEEKS, OWNER_HOURLY


class EconomicsTests(unittest.TestCase):
    def test_cash_cost_identity(self):
        for b in BASE:
            r=calculate(b)
            self.assertAlmostEqual(r['operating_profit'], r['gross_revenue']-
                r['fees']-r['refund_allowance']-r['variable_delivery']-
                r['acquisition']-r['fixed'])

    def test_zero_sales_still_has_time_and_cost(self):
        r=calculate(replace(BASE[0],units=0))
        self.assertEqual(r['operating_profit'],-BASE[0].fixed)
        self.assertGreater(r['owner_labor'],0)

    def test_subscription_replacements_not_full_book_acquired_each_month(self):
        b=BASE[0]
        r=calculate(b)
        self.assertEqual(r['acquisition'], b.units*b.churn*b.cac)
        self.assertEqual(r['initial_acquisition_cash'], b.units*b.cac)

    def test_targets_reached_at_smallest_integer(self):
        for b in BASE:
            for t in targets(b):
                self.assertGreaterEqual(t['operating_profit'],t['target'])
                self.assertLess(calculate(replace(b,units=t['units']-1))['operating_profit'],t['target'])

    def test_same_volume_drives_work(self):
        b=BASE[1]
        r=calculate(b)
        doubled=calculate(replace(b,units=b.units*2))
        self.assertAlmostEqual(doubled['weekly_owner_minutes']-b.scheduled_weekly,
                               2*(r['weekly_owner_minutes']-b.scheduled_weekly))
        self.assertAlmostEqual(r['economic_profit'],r['operating_profit']-
            r['weekly_owner_minutes']*WEEKS/60*OWNER_HOURLY)


if __name__=='__main__':
    unittest.main()
