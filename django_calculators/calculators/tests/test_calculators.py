"""
Audit tests for the calculator API endpoints.

Covers the HTTP contract for every public calculator: happy-path requests return
200 with a result body, and malformed/invalid input is rejected with 400 (never a
500 or a silently-wrong 200). Exact numeric output is asserted where the formula
is stable; otherwise we assert the response shape so the suite is not brittle to
copy changes.
"""

from django.test import override_settings
from .base import BaseAPITestCase, NO_THROTTLE_RF

PREFIX = '/api/calculators'


@override_settings(REST_FRAMEWORK=NO_THROTTLE_RF)
class CalculatorHappyPathTests(BaseAPITestCase):
    """Each calculator returns 200 + a non-error body for valid input."""

    HAPPY = {
        'salary/': {'gross_salary': 1500},
        'mortgage/': {'loan_amount': 150000, 'annual_interest_rate': 3.5, 'loan_term_years': 25},
        'vat/': {'amount': 100, 'vat_rate': 20, 'calculation_type': 'add_vat'},
        'loan/': {'loan_amount': 10000, 'interest_rate': 6, 'loan_years': 5},
        'fuel-cost/': {'distance': 100, 'consumption': 6.5, 'fuel_price': 1.6},
        'bmi/': {'weight': 75, 'height': 180},
        'pension/': {'current_age': 35, 'gross_salary': 1500, 'years_worked': 10},
        'vacation/': {'age': 30, 'employment_start_date': '2020-01-01'},
        'energy/': {'electricity_consumption': 300},
        'bmr/': {'weight': 75, 'height': 180, 'age': 30, 'gender': 'male'},
        'payment/': {'loan_amount': 10000, 'annual_interest_rate': 5, 'loan_term_years': 3},
        'freelancer-tax/': {'annual_revenue': 30000},
        'inflation/': {'present_value': 1000, 'years': 10},
        'roi/': {'initial_investment': 1000, 'final_value': 1500},
        'hours-worked/': {'hours_worked': 40, 'hourly_rate': 10},
        'sick-leave/': {'gross_salary': 1500, 'days_sick': 14},
        'car-leasing/': {'car_price': 25000, 'down_payment': 5000, 'term_months': 48},
        'parental-benefit/': {'birth_date': '2025-01-01', 'gross_salary': 1500},
        'solar/': {'annual_consumption_kwh': 4000},
    }

    def test_happy_paths(self):
        for path, payload in self.HAPPY.items():
            with self.subTest(calculator=path):
                resp = self.client.post(f'{PREFIX}/{path}', payload, format='json')
                self.assertEqual(resp.status_code, 200, f'{path} -> {resp.status_code}: {resp.content[:300]}')
                body = resp.json()
                self.assertNotIn('errors', body, f'{path} returned validation errors')
                self.assertFalse(body.get('success') is False, f'{path} returned success=false: {body}')

    def test_salary_cz_country_dispatch(self):
        resp = self.client.post(f'{PREFIX}/salary/', {'gross_salary': 40000, 'country': 'CZ'}, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json().get('country'), 'CZ')

    def test_vat_add_and_remove_consistent(self):
        add = self.client.post(f'{PREFIX}/vat/', {'amount': 100, 'vat_rate': 20, 'calculation_type': 'add_vat'}, format='json')
        rem = self.client.post(f'{PREFIX}/vat/', {'amount': 120, 'vat_rate': 20, 'calculation_type': 'remove_vat'}, format='json')
        self.assertEqual(add.status_code, 200)
        self.assertEqual(rem.status_code, 200)


@override_settings(REST_FRAMEWORK=NO_THROTTLE_RF)
class CalculatorValidationTests(BaseAPITestCase):
    """Invalid / malformed input is rejected with 400, not 200 or 500."""

    BAD = {
        'salary-missing':       ('salary/', {}),
        'salary-negative':      ('salary/', {'gross_salary': -100}),
        'salary-bad-country':   ('salary/', {'gross_salary': 1500, 'country': 'XX'}),
        'mortgage-too-small':   ('mortgage/', {'loan_amount': 500, 'annual_interest_rate': 3, 'loan_term_years': 20}),
        'mortgage-bad-term':    ('mortgage/', {'loan_amount': 150000, 'annual_interest_rate': 3, 'loan_term_years': 0}),
        'vat-bad-type':         ('vat/', {'amount': 100, 'vat_rate': 20, 'calculation_type': 'frobnicate'}),
        'bmi-weight-low':       ('bmi/', {'weight': 0.2, 'height': 180}),
        'bmi-height-low':       ('bmi/', {'weight': 75, 'height': 10}),
        'loan-too-small':       ('loan/', {'loan_amount': 50, 'interest_rate': 5, 'loan_years': 3}),
        'sick-leave-zero-days': ('sick-leave/', {'gross_salary': 1500, 'days_sick': 0}),
        'pension-underage':     ('pension/', {'current_age': 10, 'gross_salary': 1500, 'years_worked': 1}),
    }

    def test_invalid_inputs_rejected(self):
        for name, (path, payload) in self.BAD.items():
            with self.subTest(case=name):
                resp = self.client.post(f'{PREFIX}/{path}', payload, format='json')
                self.assertEqual(resp.status_code, 400, f'{name} -> {resp.status_code}: {resp.content[:300]}')

    def test_wrong_type_rejected(self):
        resp = self.client.post(f'{PREFIX}/salary/', {'gross_salary': 'abc'}, format='json')
        self.assertEqual(resp.status_code, 400)

    def test_get_not_allowed_on_post_endpoint(self):
        resp = self.client.get(f'{PREFIX}/salary/')
        self.assertEqual(resp.status_code, 405)

    def test_calculator_list_is_public(self):
        resp = self.client.get(f'{PREFIX}/')
        self.assertEqual(resp.status_code, 200)
