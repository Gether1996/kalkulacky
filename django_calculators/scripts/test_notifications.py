"""
Test script for notification and tracking system.

This script:
1. Creates sample SavedCalculation entries for pregnancy, vacation, and mortgage
2. Generates notifications for each
3. Tests the notification sending command
4. Displays results
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
from calculators.services.notification_generator import NotificationGenerator


def clear_test_data():
    """Clear all test data"""
    print("\n" + "=" * 70)
    print("CLEARING TEST DATA")
    print("=" * 70)
    
    deleted_calc = SavedCalculation.objects.all().delete()
    deleted_notif = ScheduledNotification.objects.all().delete()
    
    print(f"✓ Deleted {deleted_calc[0]} SavedCalculation records")
    print(f"✓ Deleted {deleted_notif[0]} ScheduledNotification records")


def create_pregnancy_test():
    """Create pregnancy calculation with tracking"""
    print("\n" + "=" * 70)
    print("TEST 1: PREGNANCY TRACKING")
    print("=" * 70)
    
    # Calculate LMP date (12 weeks ago)
    today = date.today()
    lmp_date = today - timedelta(days=12 * 7)
    due_date = lmp_date + timedelta(days=280)
    
    print(f"\nCreating pregnancy calculation:")
    print(f"  LMP date: {lmp_date}")
    print(f"  Due date: {due_date}")
    print(f"  Current week: 12")
    
    calculation = SavedCalculation.objects.create(
        session_key='test_session_pregnancy',
        email='test_pregnancy@example.com',
        calculator_type='pregnancy',
        name='Test Tehotenstvo - termín júl 2026',
        params={
            'calculation_method': 'lmp',
            'lmp_date': lmp_date.strftime('%Y-%m-%d'),
            'current_date': today.strftime('%Y-%m-%d'),
        },
        result={
            'due_date': due_date.strftime('%Y-%m-%d'),
            'conception_date': (lmp_date + timedelta(days=14)).strftime('%Y-%m-%d'),
            'current_week': 12,
            'current_day': 0,
            'total_days_pregnant': 84,
            'days_remaining': (due_date - today).days,
            'trimester': 1,
            'trimester_progress': 92.3,
        },
        is_tracking=True,
        notification_enabled=True,
    )
    
    print(f"✓ Created SavedCalculation ID: {calculation.id}")
    
    # Generate notifications
    print("\nGenerating notifications...")
    count = NotificationGenerator.generate_for_calculation(calculation)
    print(f"✓ Generated {count} notifications")
    
    # Show sample notifications
    notifications = ScheduledNotification.objects.filter(
        calculation=calculation
    ).order_by('scheduled_date')[:5]
    
    print("\nFirst 5 notifications:")
    for notif in notifications:
        print(f"  - {notif.scheduled_date} | {notif.notification_type} | {notif.title}")
    
    return calculation


def create_vacation_test():
    """Create vacation calculation with tracking"""
    print("\n" + "=" * 70)
    print("TEST 2: VACATION TRACKING")
    print("=" * 70)
    
    print(f"\nCreating vacation calculation:")
    print(f"  Total days: 25")
    print(f"  Used days: 5")
    print(f"  Remaining: 20")
    
    calculation = SavedCalculation.objects.create(
        session_key='test_session_vacation',
        email='test_vacation@example.com',
        calculator_type='vacation',
        name='Test Dovolenka 2026',
        params={
            'total_days': 25,
            'used_days': 5,
            'birth_date': '1993-08-15',
            'expiry_date': '2026-12-31',
        },
        result={
            'remaining_days': 20,
            'used_days': 5,
            'total_days': 25,
            'percentage_used': 20.0,
        },
        is_tracking=True,
        notification_enabled=True,
    )
    
    print(f"✓ Created SavedCalculation ID: {calculation.id}")
    
    # Generate notifications
    print("\nGenerating notifications...")
    count = NotificationGenerator.generate_for_calculation(calculation)
    print(f"✓ Generated {count} notifications")
    
    # Show all notifications
    notifications = ScheduledNotification.objects.filter(
        calculation=calculation
    ).order_by('scheduled_date')
    
    print(f"\nAll {notifications.count()} notifications:")
    for notif in notifications:
        print(f"  - {notif.scheduled_date} | {notif.notification_type} | {notif.title}")
    
    return calculation


def create_mortgage_test():
    """Create mortgage calculation with tracking"""
    print("\n" + "=" * 70)
    print("TEST 3: MORTGAGE TRACKING")
    print("=" * 70)
    
    print(f"\nCreating mortgage calculation:")
    print(f"  Principal: €150,000")
    print(f"  Interest rate: 4.5%")
    print(f"  Term: 30 years (360 months)")
    print(f"  Payment day: 15th of month")
    
    calculation = SavedCalculation.objects.create(
        session_key='test_session_mortgage',
        email='test_mortgage@example.com',
        calculator_type='mortgage',
        name='Test Hypotéka VUB',
        params={
            'principal': 150000,
            'interest_rate': 4.5,
            'months': 360,
            'payment_day': 15,
        },
        result={
            'monthly_payment': 760.03,
            'total_payment': 273610.80,
            'total_interest': 123610.80,
        },
        is_tracking=True,
        notification_enabled=True,
    )
    
    print(f"✓ Created SavedCalculation ID: {calculation.id}")
    
    # Generate notifications
    print("\nGenerating notifications...")
    count = NotificationGenerator.generate_for_calculation(calculation)
    print(f"✓ Generated {count} notifications")
    
    # Show sample notifications
    notifications = ScheduledNotification.objects.filter(
        calculation=calculation
    ).order_by('scheduled_date')[:10]
    
    print(f"\nFirst 10 notifications:")
    for notif in notifications:
        print(f"  - {notif.scheduled_date} | {notif.notification_type} | {notif.title}")
    
    return calculation


def show_summary():
    """Show summary of all data"""
    print("\n" + "=" * 70)
    print("DATABASE SUMMARY")
    print("=" * 70)
    
    total_calcs = SavedCalculation.objects.count()
    total_notifs = ScheduledNotification.objects.count()
    
    print(f"\nTotal SavedCalculations: {total_calcs}")
    print(f"Total ScheduledNotifications: {total_notifs}")
    
    # Breakdown by calculator type
    print("\nBreakdown by calculator type:")
    for calc_type, calc_name in SavedCalculation.CALCULATOR_TYPES:
        count = SavedCalculation.objects.filter(calculator_type=calc_type).count()
        if count > 0:
            notif_count = ScheduledNotification.objects.filter(
                calculation__calculator_type=calc_type
            ).count()
            print(f"  {calc_name}: {count} calculation(s), {notif_count} notifications")
    
    # Breakdown by notification type
    print("\nBreakdown by notification type:")
    notif_types = ScheduledNotification.objects.values_list(
        'notification_type', flat=True
    ).distinct()
    
    for notif_type in notif_types:
        count = ScheduledNotification.objects.filter(notification_type=notif_type).count()
        print(f"  {notif_type}: {count}")
    
    # Upcoming notifications (next 30 days)
    today = date.today()
    upcoming = ScheduledNotification.objects.filter(
        scheduled_date__gte=today,
        scheduled_date__lte=today + timedelta(days=30),
        sent=False
    ).count()
    
    print(f"\nUpcoming notifications (next 30 days): {upcoming}")


def test_notification_command():
    """Test the send_notifications management command"""
    print("\n" + "=" * 70)
    print("TEST: NOTIFICATION COMMAND (DRY RUN)")
    print("=" * 70)
    
    from django.core.management import call_command
    from io import StringIO
    
    out = StringIO()
    call_command('send_notifications', '--dry-run', stdout=out)
    
    output = out.getvalue()
    print(output)


def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("NOTIFICATION & TRACKING SYSTEM - TEST SUITE")
    print("=" * 70)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Clear existing test data
    clear_test_data()
    
    # Run tests
    try:
        preg_calc = create_pregnancy_test()
        vac_calc = create_vacation_test()
        mort_calc = create_mortgage_test()
        
        # Show summary
        show_summary()
        
        # Test command
        test_notification_command()
        
        print("\n" + "=" * 70)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        
        print("\nNext steps:")
        print("1. Check the generated notifications in the database")
        print("2. Run: python manage.py send_notifications --dry-run")
        print("3. Check email output in console (or configure SMTP for real emails)")
        print("4. Set up cron job to run send_notifications daily")
        
    except Exception as e:
        print("\n" + "=" * 70)
        print("❌ TEST FAILED!")
        print("=" * 70)
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
