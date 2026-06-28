"""
Audit tests for the Savings Goal feature: the public projection calculator, the
logged-in goal/contribution tracker, and strict per-user ownership isolation.
"""

from django.test import override_settings
from .base import BaseAPITestCase, NO_THROTTLE_RF

CALC = '/api/calculators/savings-goal/'
GOALS = '/api/calculators/my/savings-goals/'


@override_settings(REST_FRAMEWORK=NO_THROTTLE_RF)
class SavingsGoalCalculatorTests(BaseAPITestCase):
    """Public compound-interest projection (no auth)."""

    def test_time_mode_reaches_goal(self):
        resp = self.client.post(CALC, {
            'mode': 'time', 'target_amount': 10000, 'initial_amount': 1000,
            'monthly_contribution': 250, 'annual_rate': 3, 'currency': 'EUR',
        }, format='json')
        self.assertEqual(resp.status_code, 200)
        r = resp.json()['result']
        self.assertTrue(r['reached'])
        self.assertGreater(r['months'], 0)
        self.assertGreaterEqual(r['projected_balance'], 10000)
        # Interest earned must be positive with a 3% rate.
        self.assertGreater(r['interest_earned'], 0)

    def test_monthly_mode_solves_contribution(self):
        resp = self.client.post(CALC, {
            'mode': 'monthly', 'target_amount': 10000, 'initial_amount': 1000,
            'months': 24, 'annual_rate': 3, 'currency': 'CZK',
        }, format='json')
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertEqual(body['currency'], 'CZK')
        # Saving the required monthly for 24 months must land on/above target.
        self.assertGreaterEqual(body['result']['projected_balance'], 9999)

    def test_zero_rate_is_linear(self):
        resp = self.client.post(CALC, {
            'mode': 'time', 'target_amount': 1200, 'initial_amount': 0,
            'monthly_contribution': 100, 'annual_rate': 0,
        }, format='json')
        r = resp.json()['result']
        self.assertEqual(r['months'], 12)
        self.assertEqual(r['interest_earned'], 0)

    def test_unreachable_goal_reported(self):
        # No contribution and no interest can never reach a positive target.
        resp = self.client.post(CALC, {
            'mode': 'time', 'target_amount': 5000, 'initial_amount': 0,
            'monthly_contribution': 0, 'annual_rate': 5,  # rate present so request validates
        }, format='json')
        self.assertEqual(resp.status_code, 200)
        # With only interest on a 0 balance it stays 0 -> unreachable.
        self.assertFalse(resp.json()['result']['reached'])

    def test_time_mode_requires_contribution_or_rate(self):
        resp = self.client.post(CALC, {
            'mode': 'time', 'target_amount': 5000, 'initial_amount': 0,
            'monthly_contribution': 0, 'annual_rate': 0,
        }, format='json')
        self.assertEqual(resp.status_code, 400)

    def test_monthly_mode_requires_months(self):
        resp = self.client.post(CALC, {'mode': 'monthly', 'target_amount': 5000}, format='json')
        self.assertEqual(resp.status_code, 400)

    def test_target_must_be_positive(self):
        resp = self.client.post(CALC, {'mode': 'time', 'target_amount': 0,
                                       'monthly_contribution': 100}, format='json')
        self.assertEqual(resp.status_code, 400)

    def test_rate_above_cap_rejected(self):
        resp = self.client.post(CALC, {'mode': 'time', 'target_amount': 5000,
                                       'monthly_contribution': 100, 'annual_rate': 99}, format='json')
        self.assertEqual(resp.status_code, 400)


@override_settings(REST_FRAMEWORK=NO_THROTTLE_RF)
class SavingsGoalTrackerTests(BaseAPITestCase):
    """Logged-in goal CRUD + contributions + progress."""

    def setUp(self):
        super().setUp()
        self.user = self.make_user('owner@example.com')
        self.login_as(self.user)

    def _create_goal(self, **over):
        payload = {'name': 'Rezerva', 'target_amount': 5000, 'initial_amount': 500,
                   'monthly_contribution': 200, 'annual_rate': 2,
                   'target_date': '2027-06-01', 'currency': 'EUR'}
        payload.update(over)
        return self.client.post(GOALS, payload, format='json')

    def test_create_goal(self):
        resp = self._create_goal()
        self.assertEqual(resp.status_code, 201)
        data = resp.json()['data']
        self.assertEqual(data['current_balance'], 500)
        self.assertIn(data['progress']['status'], ('on_track', 'behind', 'reached', 'no_deadline'))

    def test_create_requires_name(self):
        resp = self._create_goal(name='')
        self.assertEqual(resp.status_code, 400)

    def test_add_contribution_advances_balance(self):
        gid = self._create_goal().json()['data']['id']
        resp = self.client.post(f'{GOALS}{gid}/contributions/',
                                {'amount': 1500, 'date': '2026-07-01', 'note': 'first'}, format='json')
        self.assertEqual(resp.status_code, 201)
        data = resp.json()['data']
        self.assertEqual(data['current_balance'], 2000)   # 500 initial + 1500
        self.assertEqual(data['progress']['progress_pct'], 40.0)
        self.assertEqual(len(data['contributions']), 1)

    def test_zero_contribution_rejected(self):
        gid = self._create_goal().json()['data']['id']
        resp = self.client.post(f'{GOALS}{gid}/contributions/',
                                {'amount': 0, 'date': '2026-07-01'}, format='json')
        self.assertEqual(resp.status_code, 400)

    def test_delete_goal(self):
        gid = self._create_goal().json()['data']['id']
        resp = self.client.delete(f'{GOALS}{gid}/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.client.get(GOALS).json()['data'], [])

    def test_goal_appears_in_dashboard(self):
        self._create_goal()
        resp = self.client.get('/api/calculators/my/dashboard/')
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertEqual(len(body['savingsGoals']), 1)
        self.assertEqual(body['stats']['activeSavingsGoals'], 1)


@override_settings(REST_FRAMEWORK=NO_THROTTLE_RF)
class SavingsGoalOwnershipTests(BaseAPITestCase):
    """User B must never see or mutate user A's goals (IDOR defense)."""

    def setUp(self):
        super().setUp()
        self.alice = self.make_user('alice@example.com')
        self.bob = self.make_user('bob@example.com')
        self.login_as(self.alice)
        self.gid = self.client.post(GOALS, {'name': 'Alice goal', 'target_amount': 9000}, format='json').json()['data']['id']
        self.login_as(self.bob)  # switch to attacker

    def test_b_cannot_list_a_goals(self):
        self.assertEqual(self.client.get(GOALS).json()['data'], [])

    def test_b_cannot_patch_a_goal(self):
        resp = self.client.patch(f'{GOALS}{self.gid}/', {'name': 'hacked'}, format='json')
        self.assertEqual(resp.status_code, 404)

    def test_b_cannot_delete_a_goal(self):
        resp = self.client.delete(f'{GOALS}{self.gid}/')
        self.assertEqual(resp.status_code, 404)

    def test_b_cannot_add_contribution_to_a_goal(self):
        resp = self.client.post(f'{GOALS}{self.gid}/contributions/',
                                {'amount': 100, 'date': '2026-07-01'}, format='json')
        self.assertEqual(resp.status_code, 404)

    def test_anonymous_cannot_list_goals(self):
        self.logout()
        self.assertEqual(self.client.get(GOALS).status_code, 401)
