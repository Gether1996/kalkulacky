"""
Management command to send scheduled notifications.

Run this command via cron job:
- Every day at 9:00 AM: python manage.py send_notifications
- Or use Django-cron / celery beat for scheduling
"""

from django.core.management.base import BaseCommand
from datetime import datetime, time
from calculators.models import ScheduledNotification, UserReminder
from calculators.services.notification_service import NotificationService
import logging


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Send scheduled notifications that are due'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show notifications that would be sent without actually sending them',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force resend notifications even if already sent (for testing)',
        )
    
    def handle(self, *args, **options):
        dry_run = options['dry_run']
        force = options['force']
        
        now = datetime.now()
        today = now.date()
        current_time = now.time()
        
        self.stdout.write(f"Running send_notifications at {now}")
        
        # Get notifications scheduled for today that haven't been sent yet
        query = ScheduledNotification.objects.filter(
            scheduled_date__lte=today,
            scheduled_time__lte=current_time,
        ).select_related('calculation')
        
        if not force:
            query = query.filter(sent=False)
        
        notifications = query.order_by('scheduled_date', 'scheduled_time', '-priority')
        
        total_count = notifications.count()
        
        if total_count == 0:
            self.stdout.write(self.style.WARNING('No notifications to send'))
            return
        
        self.stdout.write(f"Found {total_count} notification(s) to send")
        
        sent_count = 0
        failed_count = 0
        skipped_count = 0
        
        for notification in notifications:
            calculation = notification.calculation
            
            # Check if calculation still has tracking enabled
            if not calculation.is_tracking or not calculation.notification_enabled:
                self.stdout.write(
                    self.style.WARNING(
                        f"Skipping notification {notification.id} - tracking disabled for calculation {calculation.id}"
                    )
                )
                skipped_count += 1
                continue
            
            # Respect the owner's master email-notifications preference.
            owner = getattr(calculation, 'user', None)
            if owner is not None and not getattr(owner, 'email_notifications', True):
                skipped_count += 1
                continue

            # Effective recipient: the calculation's email, else the account email.
            recipient_email = calculation.email or (owner.email if owner else None)
            if not recipient_email:
                self.stdout.write(
                    self.style.WARNING(
                        f"Skipping notification {notification.id} - no email for calculation {calculation.id}"
                    )
                )
                skipped_count += 1
                notification.mark_failed("No email address provided")
                continue
            
            if dry_run:
                self.stdout.write(
                    self.style.NOTICE(
                        f"[DRY RUN] Would send: {notification.title} to {recipient_email}"
                    )
                )
                sent_count += 1
            else:
                # Prepare context for email template
                context = self._prepare_context(notification, calculation)

                # Send notification
                success = NotificationService.send_notification_email(
                    to_email=recipient_email,
                    notification_type=notification.notification_type,
                    context=context,
                    calculator_type=calculation.calculator_type
                )

                if success:
                    notification.mark_sent()
                    sent_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Sent notification {notification.id}: {notification.title} to {recipient_email}"
                        )
                    )
                else:
                    notification.mark_failed("Email sending failed")
                    failed_count += 1
                    self.stdout.write(
                        self.style.ERROR(
                            f"Failed to send notification {notification.id}: {notification.title}"
                        )
                    )
        
        # User-created custom reminders due today
        self._send_user_reminders(today, current_time, dry_run, force)

        # Summary
        self.stdout.write("\n" + "=" * 50)
        self.stdout.write(self.style.SUCCESS(f"Successfully sent: {sent_count}"))
        if failed_count > 0:
            self.stdout.write(self.style.ERROR(f"Failed: {failed_count}"))
        if skipped_count > 0:
            self.stdout.write(self.style.WARNING(f"Skipped: {skipped_count}"))
        self.stdout.write("=" * 50)
    
    def _send_user_reminders(self, today, current_time, dry_run, force):
        """Email custom user-created reminders that are due."""
        from django.conf import settings
        from django.core.mail import send_mail
        from django.utils import timezone

        query = UserReminder.objects.filter(
            remind_date__lte=today, email_enabled=True
        ).select_related('user')
        if not force:
            query = query.filter(sent=False)

        reminders = query.filter(remind_date__lt=today) | query.filter(
            remind_date=today, remind_time__lte=current_time
        )
        count = reminders.count()
        if count == 0:
            return
        self.stdout.write(f"Found {count} user reminder(s) to send")

        base = getattr(settings, 'FRONTEND_URL', 'https://kalkulacky.sk')
        for r in reminders:
            if not getattr(r.user, 'email_notifications', True):
                continue
            email = getattr(r.user, 'email', None)
            if not email:
                continue
            if dry_run:
                self.stdout.write(self.style.NOTICE(f"[DRY RUN] reminder '{r.title}' -> {email}"))
                continue
            body = (
                f"Pripomienka: {r.title}\n\n"
                f"{r.note or ''}\n\n"
                f"Termín: {r.remind_date:%d.%m.%Y}\n\n"
                f"— Kalkulačky.sk · {base}/dashboard"
            )
            try:
                send_mail(f"Pripomienka: {r.title}",
                          body, getattr(settings, 'DEFAULT_FROM_EMAIL', None),
                          [email], fail_silently=False)
                r.sent = True
                r.sent_at = timezone.now()
                r.save(update_fields=['sent', 'sent_at'])
                self.stdout.write(self.style.SUCCESS(f"Sent reminder '{r.title}' to {email}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Reminder '{r.title}' failed: {e}"))

    def _prepare_context(self, notification, calculation):
        """
        Prepare template context from notification and calculation data.
        """
        context = {
            'calculator_name': calculation.name,
            'title': notification.title,
            'message': notification.message,
            'action_url': f'https://kalkulacky.sk{notification.action_url}' if notification.action_url else '',
        }
        
        # Add calculator-specific data
        params = calculation.params
        result = calculation.result
        
        if calculation.calculator_type == 'pregnancy':
            context.update({
                'week': result.get('current_week', 0),
                'day': result.get('current_day', 0),
                'trimester': result.get('trimester', 1),
                'due_date': result.get('due_date', ''),
                'days_remaining': result.get('days_remaining', 0),
                'baby_size': self._get_baby_size(result.get('current_week', 0)),
                'week_description': result.get('weeks_description', ''),
                'milestone_message': '',
                'milestone_name': notification.title,
                'milestone_description': notification.message,
                'trimester_description': notification.message,
                'visit_type': notification.message,
                'visit_description': notification.message,
                'preparation_tips': notification.message,
            })
        
        elif calculation.calculator_type == 'vacation':
            context.update({
                'remaining_days': result.get('remaining_days', 0),
                'used_days': result.get('used_days', 0),
                'total_days': result.get('total_days', 0),
                'days_until': notification.message,
                'expiry_date': params.get('expiry_date', ''),
                'recommendation': notification.message,
                'months_until': 0,
                'birthday': params.get('birth_date', ''),
                'effective_date': '',
                'new_total_days': 0,
            })
        
        elif calculation.calculator_type in ['mortgage', 'loan']:
            context.update({
                'payment_amount': result.get('monthly_payment', 0),
                'due_date': notification.message,
                'days_until': 5,
                'loan_type': calculation.get_calculator_type_display(),
                'old_rate': 0,
                'new_rate': 0,
                'rate_change': 0,
                'old_payment': result.get('monthly_payment', 0),
                'new_payment': result.get('monthly_payment', 0),
                'recommendation': notification.message,
                'percentage': 0,
                'paid_amount': 0,
                'remaining_amount': params.get('principal', 0),
                'total_amount': params.get('principal', 0),
                'interest_saved': 0,
                'annual_payment': result.get('monthly_payment', 0) * 12,
                'interest_portion': 0,
                'interest_percentage': 0,
                'principal_portion': 0,
                'principal_percentage': 0,
                'extra_amount': 0,
                'savings': 0,
                'months_saved': 0,
                'remaining_balance': params.get('principal', 0),
                'monthly_payment': result.get('monthly_payment', 0),
            })
        
        return context
    
    def _get_baby_size(self, week):
        """Get baby size comparison for given week"""
        sizes = {
            4: 'semienko maku', 5: 'sezamové semeno', 6: 'hrášok',
            7: 'čučoriedka', 8: 'malina', 9: 'čerešňa', 10: 'jahoda',
            11: 'figovník', 12: 'slivka', 13: 'broskyňa', 14: 'citrón',
            15: 'jablko', 16: 'avokádo', 17: 'hruška', 18: 'paprika',
            19: 'mangold', 20: 'banán', 21: 'mrkva', 22: 'kokosový orech',
            23: 'veľký grapefruit', 24: 'kukurica', 25: 'karfiol',
            26: 'kapusta', 27: 'brokolica', 28: 'baklažán',
            29: 'tekvica butternut', 30: 'veľká kapusta', 31: 'kokosový orech',
            32: 'jicama', 33: 'ananás', 34: 'melón kantalup',
            35: 'veľká papája', 36: 'hlávkový šalát rímsky',
            37: 'mangold švajčiarsky', 38: 'rebarborové stonky',
            39: 'mini vodný melón', 40: 'malá tekvica',
        }
        return sizes.get(week, 'veľké bábätko')
