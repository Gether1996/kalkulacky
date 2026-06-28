"""
Audit tests for periodic / recurring notifications:
the send_notifications recurrence logic and the run_notifications_worker loop.
"""

from datetime import date, timedelta, time

from django.core import mail
from django.core.management import call_command
from django.test import override_settings
from django.utils import timezone

from calculators.models import UserReminder
from .base import BaseAPITestCase, NO_THROTTLE_RF


@override_settings(REST_FRAMEWORK=NO_THROTTLE_RF)
class RecurringReminderTests(BaseAPITestCase):

    def setUp(self):
        super().setUp()
        self.user = self.make_user('rem@example.com')

    def _reminder(self, **over):
        defaults = dict(
            user=self.user, title='Test', remind_date=date.today() - timedelta(days=1),
            remind_time=time(0, 0), frequency='once', is_active=True, email_enabled=True,
        )
        defaults.update(over)
        return UserReminder.objects.create(**defaults)

    def test_once_reminder_fires_then_stops(self):
        r = self._reminder(frequency='once')
        mail.outbox.clear()
        call_command('send_notifications')
        self.assertEqual(len(mail.outbox), 1)
        r.refresh_from_db()
        self.assertTrue(r.sent)
        self.assertFalse(r.is_active)
        # A second run sends nothing.
        mail.outbox.clear()
        call_command('send_notifications')
        self.assertEqual(len(mail.outbox), 0)

    def test_daily_reminder_rearms_to_future(self):
        r = self._reminder(frequency='daily')
        mail.outbox.clear()
        call_command('send_notifications')
        self.assertEqual(len(mail.outbox), 1)
        r.refresh_from_db()
        self.assertFalse(r.sent)             # stays armed
        self.assertTrue(r.is_active)
        self.assertGreater(r.remind_date, date.today())  # advanced into the future

    def test_weekly_reminder_advances_seven_days(self):
        start = date.today() - timedelta(days=1)
        r = self._reminder(frequency='weekly', remind_date=start)
        call_command('send_notifications')
        r.refresh_from_db()
        # Next occurrence is the first start+7k that is in the future.
        self.assertEqual((r.remind_date - start).days % 7, 0)
        self.assertGreater(r.remind_date, date.today())

    def test_recurring_catches_up_without_backlog(self):
        # Due 100 days ago, daily — must send ONCE and jump to the future,
        # not send 100 emails.
        r = self._reminder(frequency='daily', remind_date=date.today() - timedelta(days=100))
        mail.outbox.clear()
        call_command('send_notifications')
        self.assertEqual(len(mail.outbox), 1)
        r.refresh_from_db()
        self.assertGreater(r.remind_date, date.today())

    def test_inactive_reminder_not_sent(self):
        self._reminder(frequency='daily', is_active=False)
        mail.outbox.clear()
        call_command('send_notifications')
        self.assertEqual(len(mail.outbox), 0)

    def test_future_reminder_not_sent_yet(self):
        self._reminder(frequency='once', remind_date=date.today() + timedelta(days=5))
        mail.outbox.clear()
        call_command('send_notifications')
        self.assertEqual(len(mail.outbox), 0)

    def test_respects_master_email_pref(self):
        self.user.email_notifications = False
        self.user.save()
        self._reminder(frequency='daily')
        mail.outbox.clear()
        call_command('send_notifications')
        self.assertEqual(len(mail.outbox), 0)

    def test_next_occurrence_monthly_handles_month_end(self):
        # Use a Jan-31 base in the future so the catch-up loop does a single bump
        # and we can assert the month-end clamp (Jan 31 -> Feb 28/29).
        import calendar
        year = date.today().year + 1
        base = date(year, 1, 31)
        r = self._reminder(frequency='monthly', remind_date=base)
        nxt = r.next_occurrence(after=base)
        expected_day = min(31, calendar.monthrange(year, 2)[1])
        self.assertEqual(nxt, date(year, 2, expected_day))


class WorkerCommandTests(BaseAPITestCase):

    def test_worker_once_runs_a_single_pass(self):
        user = self.make_user('w@example.com')
        UserReminder.objects.create(
            user=user, title='Daily ping', remind_date=date.today() - timedelta(days=1),
            remind_time=time(0, 0), frequency='daily', is_active=True, email_enabled=True,
        )
        mail.outbox.clear()
        # --once must execute one send pass and return (no infinite loop).
        call_command('run_notifications_worker', once=True)
        self.assertEqual(len(mail.outbox), 1)

    def test_worker_once_dry_run_sends_nothing(self):
        user = self.make_user('w2@example.com')
        UserReminder.objects.create(
            user=user, title='Daily ping', remind_date=date.today() - timedelta(days=1),
            remind_time=time(0, 0), frequency='daily', is_active=True, email_enabled=True,
        )
        mail.outbox.clear()
        call_command('run_notifications_worker', once=True, dry_run=True)
        self.assertEqual(len(mail.outbox), 0)
