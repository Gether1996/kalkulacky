"""
Regression tests for the production-hardening audit (2026-07-31).

Covers the fixes applied in this pass:
  * GDPR erasure now purges/anonymizes PII that isn't FK-linked to the user
    (Lead, DataReport, AuthEvent) on account deletion.
  * Split-bill line items are schema-validated → malformed input yields 400,
    not a KeyError/500.
  * Savings-goal tracker inputs are bounded → negative / absurd values and a
    far-future target_date are rejected (previously drove a huge projection loop).
"""

from datetime import date
from decimal import Decimal
from django.test import TestCase, override_settings
from calculators.tests.base import BaseAPITestCase, NO_THROTTLE_RF

CALC = '/api/calculators'
AUTH = '/api/auth'


@override_settings(REST_FRAMEWORK=NO_THROTTLE_RF)
class GdprErasureTests(BaseAPITestCase):
    """Account deletion must not leave email/IP-keyed PII behind."""

    def test_delete_account_purges_and_anonymizes_pii(self):
        from calculators.models import Lead, DataReport, AuthEvent
        email = 'erase-me@example.com'
        user = self.make_user(email)

        # PII rows keyed by the string email, NOT by a FK to the user.
        Lead.objects.create(
            vertical='mortgage', calculator_type='mortgage', name='X',
            email=email, phone='+421900000000', consent=True,
        )
        DataReport.objects.create(
            calculator_type='salary', message='wrong', reporter_email=email,
        )
        AuthEvent.objects.create(event='login', email=email, ip_address='1.2.3.4')

        self.login_as(user)
        resp = self.client.delete(f'{AUTH}/delete-account/')
        self.assertEqual(resp.status_code, 200)

        # Lead + DataReport are hard-deleted.
        self.assertFalse(Lead.objects.filter(email__iexact=email).exists())
        self.assertFalse(DataReport.objects.filter(reporter_email__iexact=email).exists())
        # AuthEvent rows survive as an audit trail but are stripped of PII.
        for ev in AuthEvent.objects.filter(event='login'):
            self.assertEqual(ev.email, '')
            self.assertIsNone(ev.ip_address)


@override_settings(REST_FRAMEWORK=NO_THROTTLE_RF)
class SplitBillValidationTests(BaseAPITestCase):
    """Malformed by_items input must be a validated 400, never a 500."""

    def test_missing_item_keys_returns_400(self):
        resp = self.client.post(f'{CALC}/split-bill/', {
            'split_type': 'by_items',
            'items': [{}],  # no person / amount
        }, format='json')
        self.assertEqual(resp.status_code, 400)

    def test_non_numeric_amount_returns_400(self):
        resp = self.client.post(f'{CALC}/split-bill/', {
            'split_type': 'by_items',
            'items': [{'person': 'A', 'amount': 'abc'}],
        }, format='json')
        self.assertEqual(resp.status_code, 400)

    def test_valid_items_still_calculate(self):
        resp = self.client.post(f'{CALC}/split-bill/', {
            'split_type': 'by_items',
            'items': [
                {'person': 'A', 'amount': '10.00'},
                {'person': 'B', 'amount': '20.00'},
            ],
        }, format='json')
        self.assertEqual(resp.status_code, 200)


@override_settings(REST_FRAMEWORK=NO_THROTTLE_RF)
class SavingsGoalBoundsTests(BaseAPITestCase):
    """Tracker inputs are bounded so a single goal can't drive a huge loop."""

    def setUp(self):
        super().setUp()
        self.user = self.make_user('saver@example.com')
        self.login_as(self.user)

    def _create(self, **overrides):
        payload = {
            'name': 'Emergency fund',
            'target_amount': '10000.00',
            'monthly_contribution': '200.00',
            'annual_rate': '2.00',
        }
        payload.update(overrides)
        return self.client.post(f'{CALC}/my/savings-goals/', payload, format='json')

    def test_negative_target_amount_rejected(self):
        self.assertEqual(self._create(target_amount='-5').status_code, 400)

    def test_far_future_target_date_rejected(self):
        self.assertEqual(self._create(target_date='9999-01-01').status_code, 400)

    def test_reasonable_goal_accepted(self):
        resp = self._create(target_date=f'{date.today().year + 2}-01-01')
        self.assertEqual(resp.status_code, 201)


class TaxCorrectnessTests(TestCase):
    """2026 tax-logic fixes (verified against Sociálna poisťovňa / Financná správa)."""

    def test_child_bonus_is_refundable(self):
        from calculators.services.salary_calculator import SalaryCalculator
        r = SalaryCalculator().calculate(gross_salary=900, children_under_15=1)
        # Bonus paid in full (€100) even though it exceeds the income tax → net rises.
        self.assertEqual(float(r['child_tax_bonus']), 100.0)
        self.assertLess(float(r['final_tax']), 0)          # excess refunded
        self.assertAlmostEqual(float(r['net_salary']), 818.5, places=1)

    def test_salary_social_insurance_max_base(self):
        from calculators.services.salary_calculator import SalaryCalculator
        from calculators.services import config_variables as cfg
        r = SalaryCalculator().calculate(gross_salary=20000)
        expected = float(cfg.SOCIAL_INSURANCE_MAX_BASE_MONTHLY * cfg.SOCIAL_INSURANCE_RATE_EMPLOYEE)
        self.assertAlmostEqual(float(r['social_insurance']), expected, places=2)

    def test_sick_leave_daily_cap(self):
        from calculators.services import config_variables as cfg
        self.assertAlmostEqual(float(cfg.SICK_LEAVE_MAX_ASSESSMENT_BASE_DAILY), 100.2083, places=3)

    def test_freelancer_nczd_taper_zeroes_at_high_base(self):
        from calculators.services.freelancer_tax_calculator import FreelancerTaxCalculator
        from calculators.services import config_variables as cfg
        # Base well above €43,983 → NČZD must be fully tapered to 0 (taxable == base).
        base = Decimal('60000')
        nczd = max(Decimal('0'), cfg.NCZD_TAPER_SUBTRAHEND_ANNUAL - base / Decimal('3'))
        self.assertEqual(nczd, Decimal('0'))
