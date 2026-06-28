"""
Audit tests for the authentication / account lifecycle:
register, login, logout (JWT blacklist), profile, change-password, password reset,
and GDPR account deletion — with edge cases and anti-enumeration checks.

Reuses the throttle-free REST_FRAMEWORK override from the calculators test base so
the auth flows aren't tripped by rate limits.
"""

from django.test import override_settings
from django.core import mail
from django.contrib.auth import get_user_model
from calculators.tests.base import BaseAPITestCase, NO_THROTTLE_RF

A = '/api/auth'
User = get_user_model()


@override_settings(REST_FRAMEWORK=NO_THROTTLE_RF)
class RegisterTests(BaseAPITestCase):

    def test_register_success_returns_tokens(self):
        resp = self.client.post(f'{A}/register/', {
            'email': 'new@example.com', 'password': 'Str0ng-Pass!23',
            'password_confirm': 'Str0ng-Pass!23', 'first_name': 'New',
        }, format='json')
        self.assertEqual(resp.status_code, 201)
        body = resp.json()
        self.assertIn('access', body)
        self.assertIn('refresh', body)
        self.assertEqual(body['user']['email'], 'new@example.com')

    def test_password_mismatch_rejected(self):
        resp = self.client.post(f'{A}/register/', {
            'email': 'm@example.com', 'password': 'Str0ng-Pass!23',
            'password_confirm': 'different!23',
        }, format='json')
        self.assertEqual(resp.status_code, 400)

    def test_short_password_rejected(self):
        resp = self.client.post(f'{A}/register/', {
            'email': 's@example.com', 'password': 'short', 'password_confirm': 'short',
        }, format='json')
        self.assertEqual(resp.status_code, 400)

    def test_duplicate_email_rejected(self):
        self.make_user('dup@example.com')
        resp = self.client.post(f'{A}/register/', {
            'email': 'dup@example.com', 'password': 'Str0ng-Pass!23',
            'password_confirm': 'Str0ng-Pass!23',
        }, format='json')
        self.assertEqual(resp.status_code, 400)

    def test_invalid_email_rejected(self):
        resp = self.client.post(f'{A}/register/', {
            'email': 'not-an-email', 'password': 'Str0ng-Pass!23',
            'password_confirm': 'Str0ng-Pass!23',
        }, format='json')
        self.assertEqual(resp.status_code, 400)


@override_settings(REST_FRAMEWORK=NO_THROTTLE_RF)
class LoginLogoutTests(BaseAPITestCase):

    def setUp(self):
        super().setUp()
        self.user = self.make_user('login@example.com', password='Str0ng-Pass!23')

    def test_login_success(self):
        resp = self.client.post(f'{A}/login/', {
            'email': 'login@example.com', 'password': 'Str0ng-Pass!23',
        }, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('access', resp.json())

    def test_login_wrong_password(self):
        resp = self.client.post(f'{A}/login/', {
            'email': 'login@example.com', 'password': 'nope',
        }, format='json')
        self.assertEqual(resp.status_code, 400)

    def test_login_unknown_user(self):
        resp = self.client.post(f'{A}/login/', {
            'email': 'ghost@example.com', 'password': 'whatever',
        }, format='json')
        self.assertEqual(resp.status_code, 400)

    def test_inactive_user_cannot_login(self):
        self.user.is_active = False
        self.user.save()
        resp = self.client.post(f'{A}/login/', {
            'email': 'login@example.com', 'password': 'Str0ng-Pass!23',
        }, format='json')
        self.assertEqual(resp.status_code, 400)

    def test_logout_blacklists_refresh_token(self):
        login = self.client.post(f'{A}/login/', {
            'email': 'login@example.com', 'password': 'Str0ng-Pass!23',
        }, format='json').json()
        self.login_as(self.user)
        resp = self.client.post(f'{A}/logout/', {'refresh': login['refresh']}, format='json')
        self.assertEqual(resp.status_code, 200)
        # The blacklisted refresh token can no longer mint a new access token.
        self.logout()
        again = self.client.post(f'{A}/token/refresh/', {'refresh': login['refresh']}, format='json')
        self.assertEqual(again.status_code, 401)

    def test_login_failed_logs_auth_event(self):
        from calculators.models import AuthEvent
        self.client.post(f'{A}/login/', {'email': 'login@example.com', 'password': 'bad'}, format='json')
        self.assertTrue(AuthEvent.objects.filter(event='login_failed').exists())


@override_settings(REST_FRAMEWORK=NO_THROTTLE_RF)
class ProfileAndPasswordTests(BaseAPITestCase):

    def setUp(self):
        super().setUp()
        self.user = self.make_user('p@example.com', password='Str0ng-Pass!23')
        self.login_as(self.user)

    def test_get_profile(self):
        resp = self.client.get(f'{A}/profile/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['email'], 'p@example.com')

    def test_change_password_success(self):
        resp = self.client.post(f'{A}/change-password/', {
            'old_password': 'Str0ng-Pass!23',
            'new_password': 'Even-Str0nger!45',
            'new_password_confirm': 'Even-Str0nger!45',
        }, format='json')
        self.assertEqual(resp.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('Even-Str0nger!45'))

    def test_change_password_wrong_old(self):
        resp = self.client.post(f'{A}/change-password/', {
            'old_password': 'WRONG',
            'new_password': 'Even-Str0nger!45',
            'new_password_confirm': 'Even-Str0nger!45',
        }, format='json')
        self.assertEqual(resp.status_code, 400)

    def test_change_password_mismatch(self):
        resp = self.client.post(f'{A}/change-password/', {
            'old_password': 'Str0ng-Pass!23',
            'new_password': 'Even-Str0nger!45',
            'new_password_confirm': 'different!45',
        }, format='json')
        self.assertEqual(resp.status_code, 400)


@override_settings(REST_FRAMEWORK=NO_THROTTLE_RF)
class PasswordResetTests(BaseAPITestCase):

    def setUp(self):
        super().setUp()
        self.user = self.make_user('reset@example.com', password='Str0ng-Pass!23')

    def test_forgot_password_does_not_enumerate(self):
        # Same generic 200 whether or not the email exists.
        r1 = self.client.post(f'{A}/forgot-password/', {'email': 'reset@example.com'}, format='json')
        r2 = self.client.post(f'{A}/forgot-password/', {'email': 'ghost@example.com'}, format='json')
        self.assertEqual(r1.status_code, 200)
        self.assertEqual(r2.status_code, 200)
        self.assertEqual(r1.json()['message'], r2.json()['message'])

    def test_forgot_password_sends_email_to_existing_user(self):
        mail.outbox.clear()
        self.client.post(f'{A}/forgot-password/', {'email': 'reset@example.com'}, format='json')
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('reset@example.com', mail.outbox[0].to)

    def test_reset_with_valid_token(self):
        from django.contrib.auth.tokens import default_token_generator
        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        resp = self.client.post(f'{A}/reset-password/', {
            'uid': uid, 'token': token,
            'new_password': 'Brand-New!99', 'new_password_confirm': 'Brand-New!99',
        }, format='json')
        self.assertEqual(resp.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('Brand-New!99'))

    def test_reset_with_invalid_token(self):
        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        resp = self.client.post(f'{A}/reset-password/', {
            'uid': uid, 'token': 'bogus-token',
            'new_password': 'Brand-New!99', 'new_password_confirm': 'Brand-New!99',
        }, format='json')
        self.assertEqual(resp.status_code, 400)


@override_settings(REST_FRAMEWORK=NO_THROTTLE_RF)
class AccountDeletionTests(BaseAPITestCase):

    def test_delete_account_removes_user_and_data(self):
        from calculators.models import SavedCalculation
        user = self.make_user('gone@example.com')
        self.login_as(user)
        # Create owned data that must cascade-delete.
        self.client.post('/api/calculators/saved-calculations/', {
            'calculator_type': 'salary', 'name': 'x', 'params': {'gross_salary': 1500},
        }, format='json')
        self.assertEqual(SavedCalculation.objects.filter(user=user).count(), 1)

        uid = user.pk  # this model's PK is the email; capture before deletion
        resp = self.client.delete(f'{A}/delete-account/')
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(User.objects.filter(email='gone@example.com').exists())
        self.assertEqual(SavedCalculation.objects.filter(user_id=uid).count(), 0)
