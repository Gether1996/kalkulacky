"""
Test sending actual notifications with past dates.

This script creates a notification with a past date and tests the email sending.
"""

import os
import sys
import django
from datetime import datetime, timedelta, date

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_calculators.settings')
django.setup()

from calculators.models import SavedCalculation, ScheduledNotification
from django.core.management import call_command
from io import StringIO


def create_test_notification():
    """Create a test notification with past date"""
    print("\n" + "=" * 70)
    print("CREATING TEST NOTIFICATION WITH PAST DATE")
    print("=" * 70)
    
    # Create a simple calculation
    calculation = SavedCalculation.objects.create(
        session_key='test_email_session',
        email='test@example.com',
        calculator_type='pregnancy',
        name='Test Email Notification',
        params={'test': 'data'},
        result={'test': 'result'},
        is_tracking=True,
        notification_enabled=True,
    )
    
    print(f"✓ Created SavedCalculation ID: {calculation.id}")
    
    # Create notification with yesterday's date
    yesterday = date.today() - timedelta(days=1)
    
    notification = ScheduledNotification.objects.create(
        calculation=calculation,
        notification_type='pregnancy_week',
        priority='medium',
        scheduled_date=yesterday,
        scheduled_time='09:00:00',
        title='Test Email - Týždeň 12 tehotenstva',
        message='Toto je testovacia notifikácia.',
        action_url='/calculator/pregnancy?id=1',
        sent=False,
    )
    
    print(f"✓ Created ScheduledNotification ID: {notification.id}")
    print(f"  Scheduled for: {notification.scheduled_date} {notification.scheduled_time}")
    print(f"  Email: {calculation.email}")
    
    return calculation, notification


def test_send_command():
    """Test the send_notifications command (real send, but to console)"""
    print("\n" + "=" * 70)
    print("TESTING SEND_NOTIFICATIONS COMMAND (CONSOLE OUTPUT)")
    print("=" * 70)
    
    print("\nRunning: python manage.py send_notifications")
    print("(Check console for email output)\n")
    
    out = StringIO()
    call_command('send_notifications', stdout=out)
    
    output = out.getvalue()
    print(output)


def verify_sent():
    """Verify that notification was marked as sent"""
    print("\n" + "=" * 70)
    print("VERIFICATION")
    print("=" * 70)
    
    sent_notifs = ScheduledNotification.objects.filter(sent=True).count()
    unsent_notifs = ScheduledNotification.objects.filter(sent=False).count()
    
    print(f"\nSent notifications: {sent_notifs}")
    print(f"Unsent notifications: {unsent_notifs}")
    
    if sent_notifs > 0:
        print("\n✅ Notification(s) were successfully sent!")
    else:
        print("\n⚠️  No notifications were sent.")


def main():
    """Run email test"""
    print("\n" + "=" * 70)
    print("EMAIL NOTIFICATION TEST")
    print("=" * 70)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("EMAIL_BACKEND: django.core.mail.backends.console.EmailBackend")
    print("(Emails will be printed to console)")
    
    try:
        # Clean up previous test data
        SavedCalculation.objects.filter(session_key='test_email_session').delete()
        
        # Create test notification
        calc, notif = create_test_notification()
        
        # Send notifications
        test_send_command()
        
        # Verify
        verify_sent()
        
        print("\n" + "=" * 70)
        print("✅ EMAIL TEST COMPLETED!")
        print("=" * 70)
        print("\nCheck the console output above for the email content.")
        print("If you see email output, the notification system is working correctly!")
        
    except Exception as e:
        print("\n" + "=" * 70)
        print("❌ TEST FAILED!")
        print("=" * 70)
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
