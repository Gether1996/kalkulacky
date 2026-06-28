"""
Security / defense-against-attackers audit.

Covers: authentication gates, per-user ownership isolation (IDOR), rate-limit
throttling, injection / stored-XSS safety, input hardening (oversized, malformed,
wrong-method), field immutability, JWT tampering, bot filtering and admin-only
analytics.
"""

from unittest import mock
from django.test import override_settings
from django.core import mail
from rest_framework.throttling import SimpleRateThrottle
from .base import BaseAPITestCase, NO_THROTTLE_RF

C = '/api/calculators'
A = '/api/auth'


# ---------------------------------------------------------------------------
# Authentication gates
# ---------------------------------------------------------------------------
@override_settings(REST_FRAMEWORK=NO_THROTTLE_RF)
class AuthRequiredTests(BaseAPITestCase):
    """Protected endpoints reject anonymous callers."""

    PROTECTED_GET = [
        f'{C}/my/dashboard/',
        f'{C}/my/reminders/',
        f'{C}/my/savings-goals/',
        f'{A}/profile/',
    ]

    def test_anonymous_get_blocked(self):
        for url in self.PROTECTED_GET:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 401)

    def test_anonymous_mutations_blocked(self):
        self.assertEqual(self.client.post(f'{A}/logout/', {}, format='json').status_code, 401)
        self.assertEqual(self.client.post(f'{A}/change-password/', {}, format='json').status_code, 401)
        self.assertEqual(self.client.delete(f'{A}/delete-account/').status_code, 401)

    def test_analytics_stats_admin_only(self):
        # anonymous
        self.assertIn(self.client.get(f'{C}/analytics/stats/').status_code, (401, 403))
        # normal user -> forbidden
        self.login_as(self.make_user('normal@example.com'))
        self.assertEqual(self.client.get(f'{C}/analytics/stats/').status_code, 403)
        # admin -> ok
        self.logout()
        self.login_as(self.make_admin())
        self.assertEqual(self.client.get(f'{C}/analytics/stats/').status_code, 200)

    def test_tampered_jwt_rejected(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer not.a.real.token')
        self.assertEqual(self.client.get(f'{C}/my/dashboard/').status_code, 401)


# ---------------------------------------------------------------------------
# Ownership isolation (IDOR) on saved calculations + reminders
# ---------------------------------------------------------------------------
@override_settings(REST_FRAMEWORK=NO_THROTTLE_RF)
class OwnershipIsolationTests(BaseAPITestCase):

    def setUp(self):
        super().setUp()
        self.alice = self.make_user('alice@example.com')
        self.bob = self.make_user('bob@example.com')
        # Alice saves a calculation
        self.login_as(self.alice)
        self.calc_id = self.client.post(f'{C}/saved-calculations/', {
            'calculator_type': 'salary', 'name': 'Alice salary',
            'params': {'gross_salary': 1500}, 'is_tracking': False,
        }, format='json').json()['data']['id']
        # Alice creates a reminder
        self.rem_id = self.client.post(f'{C}/my/reminders/', {
            'title': 'Alice reminder', 'remind_date': '2027-01-01',
        }, format='json').json()['data']['id']
        # Become Bob (attacker)
        self.login_as(self.bob)

    def test_bob_cannot_read_alice_calc(self):
        resp = self.client.get(f'{C}/saved-calculations/{self.calc_id}/')
        self.assertEqual(resp.status_code, 403)

    def test_bob_cannot_modify_alice_calc(self):
        resp = self.client.put(f'{C}/saved-calculations/{self.calc_id}/',
                               {'name': 'hacked'}, format='json')
        self.assertEqual(resp.status_code, 403)

    def test_bob_cannot_delete_alice_calc(self):
        resp = self.client.delete(f'{C}/saved-calculations/{self.calc_id}/')
        self.assertEqual(resp.status_code, 403)

    def test_bob_dashboard_excludes_alice_data(self):
        body = self.client.get(f'{C}/my/dashboard/').json()
        self.assertEqual(body['calculations'], [])
        self.assertEqual(body['stats']['totalCalculations'], 0)

    def test_bob_cannot_touch_alice_reminder(self):
        self.assertEqual(self.client.patch(f'{C}/my/reminders/{self.rem_id}/',
                                           {'title': 'x'}, format='json').status_code, 404)
        self.assertEqual(self.client.delete(f'{C}/my/reminders/{self.rem_id}/').status_code, 404)


# ---------------------------------------------------------------------------
# Rate-limit throttling
#
# DRF binds THROTTLE_RATES as a class attribute at import time, so
# override_settings(REST_FRAMEWORK=...) does NOT reach it. We patch the shared
# rate dict in place (restored automatically) to assert the throttle fires.
# ---------------------------------------------------------------------------
class ThrottlingTests(BaseAPITestCase):

    def _rate(self, **scopes):
        return mock.patch.dict(SimpleRateThrottle.THROTTLE_RATES, scopes)

    def test_leads_throttled(self):
        payload = {'vertical': 'insurance_car', 'calculator_type': 'car-insurance',
                   'email': 'lead@example.com', 'consent': True}
        with self._rate(leads='2/min'):
            codes = [self.client.post(f'{C}/leads/', payload, format='json').status_code for _ in range(4)]
        self.assertIn(429, codes, f'expected a 429 within {codes}')

    def test_login_bruteforce_throttled(self):
        payload = {'email': 'nobody@example.com', 'password': 'wrong'}
        with self._rate(login='2/min'):
            codes = [self.client.post(f'{A}/login/', payload, format='json').status_code for _ in range(4)]
        self.assertIn(429, codes, f'expected a 429 within {codes}')

    def test_data_report_throttled(self):
        payload = {'calculator_type': 'salary', 'message': 'wrong number here',
                   'page_url': 'https://x/y'}
        with self._rate(data_report='2/min'):
            codes = [self.client.post(f'{C}/data-report/', payload, format='json').status_code for _ in range(4)]
        self.assertIn(429, codes)


# ---------------------------------------------------------------------------
# Injection / stored-XSS safety + input hardening
# ---------------------------------------------------------------------------
@override_settings(REST_FRAMEWORK=NO_THROTTLE_RF)
class InjectionAndHardeningTests(BaseAPITestCase):

    def test_sql_injection_string_stored_literally(self):
        from calculators.models import Lead
        evil = "Robert'); DROP TABLE calculators_lead;--"
        resp = self.client.post(f'{C}/leads/', {
            'vertical': 'insurance_car', 'calculator_type': 'car-insurance',
            'name': evil, 'email': 'x@example.com', 'consent': True,
        }, format='json')
        self.assertEqual(resp.status_code, 201)
        # Table intact + value stored as an inert literal (ORM parameterizes).
        lead = Lead.objects.latest('id')
        self.assertEqual(lead.name, evil)

    def test_xss_payload_stored_verbatim_not_executed(self):
        from calculators.models import DataReport
        xss = '<script>alert(document.cookie)</script>'
        resp = self.client.post(f'{C}/data-report/', {
            'calculator_type': 'salary', 'message': f'bad value {xss}',
            'page_url': 'https://x/y', 'locale': 'sk',
        }, format='json')
        self.assertEqual(resp.status_code, 201)
        report = DataReport.objects.latest('id')
        # Stored as data, never interpreted; escaping is the render layer's job.
        self.assertIn(xss, report.message)

    def test_oversized_number_rejected(self):
        resp = self.client.post(f'{C}/salary/', {'gross_salary': 10 ** 15}, format='json')
        self.assertEqual(resp.status_code, 400)

    def test_malformed_json_rejected(self):
        resp = self.client.post(f'{C}/salary/', data='{not valid json',
                                content_type='application/json')
        self.assertEqual(resp.status_code, 400)

    def test_lead_requires_consent(self):
        resp = self.client.post(f'{C}/leads/', {
            'vertical': 'insurance_car', 'calculator_type': 'car-insurance',
            'email': 'x@example.com', 'consent': False,
        }, format='json')
        self.assertEqual(resp.status_code, 400)

    def test_lead_requires_contact(self):
        resp = self.client.post(f'{C}/leads/', {
            'vertical': 'insurance_car', 'calculator_type': 'car-insurance',
            'consent': True,
        }, format='json')
        self.assertEqual(resp.status_code, 400)


# ---------------------------------------------------------------------------
# Analytics: bot filtering + privacy
# ---------------------------------------------------------------------------
@override_settings(REST_FRAMEWORK=NO_THROTTLE_RF)
class AnalyticsCollectionTests(BaseAPITestCase):

    def test_human_pageview_stored(self):
        from calculators.models import PageView
        resp = self.client.post(f'{C}/analytics/collect/', {'path': '/calculator/salary', 'locale': 'sk'},
                                format='json', HTTP_USER_AGENT='Mozilla/5.0 (Windows NT 10.0)')
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(PageView.objects.filter(path='/calculator/salary').count(), 1)

    def test_bot_pageview_ignored(self):
        from calculators.models import PageView
        before = PageView.objects.count()
        resp = self.client.post(f'{C}/analytics/collect/', {'path': '/calculator/salary'},
                                format='json', HTTP_USER_AGENT='Googlebot/2.1')
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(PageView.objects.count(), before)  # nothing stored

    def test_collect_never_stores_raw_ip(self):
        from calculators.models import PageView
        self.client.post(f'{C}/analytics/collect/', {'path': '/x'}, format='json',
                         HTTP_USER_AGENT='Mozilla/5.0')
        pv = PageView.objects.latest('id')
        self.assertFalse(hasattr(pv, 'ip_address') and getattr(pv, 'ip_address', None))


# ---------------------------------------------------------------------------
# Field immutability + open endpoints
# ---------------------------------------------------------------------------
@override_settings(REST_FRAMEWORK=NO_THROTTLE_RF)
class ImmutabilityTests(BaseAPITestCase):

    def test_email_cannot_be_changed_via_profile(self):
        user = self.make_user('fixed@example.com')
        self.login_as(user)
        resp = self.client.patch(f'{A}/profile/',
                                 {'email': 'attacker@evil.com', 'first_name': 'New'}, format='json')
        self.assertEqual(resp.status_code, 200)
        user.refresh_from_db()
        self.assertEqual(user.email, 'fixed@example.com')   # unchanged (read-only)
        self.assertEqual(user.first_name, 'New')            # other fields editable

    def test_health_check_is_public(self):
        self.assertEqual(self.client.get(f'{C}/health/').status_code, 200)
