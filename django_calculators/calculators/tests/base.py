"""
Shared test base + throttle helpers for the audit suite.

Throttling is the trickiest part to test: DRF throttles accumulate counts in the
default cache, keyed by client IP. The whole suite runs from one IP (testserver),
so the global anon rate (600/min) could trip mid-suite and cause flaky 429s.

Strategy:
  * Functional tests run with throttling DISABLED (`NO_THROTTLE_RF`) — they assert
    business logic, not rate limits.
  * Throttle behaviour is tested explicitly in test_security.py with a tiny rate
    override (`throttle_rf`), and `cache.clear()` between tests so counts reset.

We preserve the rest of REST_FRAMEWORK (auth/permission/renderer/parser) by
copying the live config and only swapping throttle keys — replacing the whole
dict would drop JWT auth.
"""

from django.conf import settings as dj_settings
from django.core.cache import cache
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

_RF = dict(getattr(dj_settings, 'REST_FRAMEWORK', {}))

# REST_FRAMEWORK with throttling switched off (functional tests).
NO_THROTTLE_RF = {
    **_RF,
    'DEFAULT_THROTTLE_CLASSES': [],
    'DEFAULT_THROTTLE_RATES': {},
}


def throttle_rf(**rates):
    """REST_FRAMEWORK copy with specific scope rates overridden (throttle tests)."""
    base_rates = dict(_RF.get('DEFAULT_THROTTLE_RATES', {}))
    base_rates.update(rates)
    return {**_RF, 'DEFAULT_THROTTLE_RATES': base_rates}


User = get_user_model()


class BaseAPITestCase(APITestCase):
    """APITestCase with a clean cache per test + auth helpers."""

    def setUp(self):
        super().setUp()
        cache.clear()  # reset throttle counters between tests

    # ---- user / auth helpers ----
    def make_user(self, email='user@example.com', password='Str0ng-Pass!23', **extra):
        return User.objects.create_user(email=email, password=password, **extra)

    def make_admin(self, email='admin@example.com', password='Str0ng-Pass!23'):
        return User.objects.create_superuser(email=email, password=password)

    def login_as(self, user):
        """Attach a Bearer access token for `user` to the test client."""
        token = str(RefreshToken.for_user(user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        return token

    def logout(self):
        self.client.credentials()
