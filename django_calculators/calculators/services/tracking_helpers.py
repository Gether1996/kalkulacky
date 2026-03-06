"""
Tracking Helpers for Calculator Notifications

These helpers create scheduled notifications for different calculator types
based on the input parameters and tracking preferences.
"""

from datetime import datetime, timedelta, date
from typing import List, Dict, Any
from calculators.models import ScheduledNotification, SavedCalculation


class PregnancyTrackingHelper:
    """
    Helper for creating pregnancy-related notifications.
    
    Creates:
    - Weekly pregnancy updates
    - Trimester transition notifications
    - Milestone notifications (weeks 8, 12, 20, 28, 36, 38, 40)
    - Prenatal visit reminders
    - Due date approaching notifications
    """
    
    # Pregnancy milestones
    MILESTONES = {
        8: {
            'name': 'Koniec embryonálneho obdobia',
            'description': 'Bábätko je teraz oficiálne plod! Všetky hlavné orgány sú založené.'
        },
        12: {
            'name': 'Koniec 1. trimestra',
            'description': 'Riziko potratu výrazne klesá. Väčšina tiel bábätka je už vytvorená.'
        },
        20: {
            'name': 'Polovica cesty!',
            'description': 'Ste v polovici tehotenstva! Bábätko aktívne kope a pohybuje sa.'
        },
        28: {
            'name': 'Začiatok 3. trimestra',
            'description': 'Bábätko by už malo reálnu šancu na prežitie pri predčasnom pôrode.'
        },
        36: {
            'name': 'Skorý termín',
            'description': 'Bábätko je už považované za skorý termín. Pľúca sú takmer zrelé.'
        },
        38: {
            'name': 'Bábätko je plne vyvinuté',
            'description': 'Bábätko je teraz plne vyvinuté a pripravené na narodenie.'
        },
        40: {
            'name': 'Termín pôrodu!',
            'description': 'Gratulujeme! Dnes je váš predpokladaný termín pôrodu. Každú chvíľu môže prísť! 🎉'
        },
    }
    
    # Prenatal visits schedule (in weeks)
    PRENATAL_VISITS = {
        8: 'Prvá prenatálna kontrola + ultrazvuk',
        12: 'Kontrola + odber krvi (screeningové testy)',
        20: 'Detailný ultrazvuk (morfológia)',
        28: 'Glukózový tolerančný test (cukrovka)',
        32: 'Štandardná kontrola',
        36: 'Kontrola + GBS test',
        38: 'Týždenné kontroly začínajú',
        39: 'Týždenná kontrola',
        40: 'Týždenná kontrola',
    }
    
    # Baby size comparisons by week
    BABY_SIZES = {
        4: 'semienko maku',
        5: 'sezamové semeno',
        6: 'hrášok',
        7: 'čučoriedka',
        8: 'malina',
        9: 'čerešňa',
        10: 'jahoda',
        11: 'figovník',
        12: 'slivka',
        13: 'broskyňa',
        14: 'citrón',
        15: 'jablko',
        16: 'avokádo',
        17: 'hruška',
        18: 'paprika',
        19: 'mangold',
        20: 'banán',
        21: 'mrkva',
        22: 'kokosový orech',
        23: 'veľký grapefruit',
        24: 'kukurica',
        25: 'karfiol',
        26: 'kapusta',
        27: 'brokolica',
        28: 'baklažán',
        29: 'tekvica butternut',
        30: 'veľká kapusta',
        31: 'kokosový orech',
        32: 'jicama',
        33: 'ananás',
        34: 'melón kantalup',
        35: 'veľká papája',
        36: 'hlávkový šalát rímsky',
        37: 'mangold švajčiarsky',
        38: 'rebarborové stonky',
        39: 'mini vodný melón',
        40: 'malá tekvica',
    }
    
    @staticmethod
    def create_notifications(calculation: SavedCalculation) -> int:
        """
        Create all pregnancy-related notifications for a saved calculation.
        
        Args:
            calculation: SavedCalculation instance with pregnancy data
        
        Returns:
            Number of notifications created
        """
        params = calculation.params
        result = calculation.result
        
        if not result:
            return 0
        
        # Extract key dates
        due_date_str = result.get('due_date')
        if not due_date_str:
            return 0
        
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        current_week = result.get('current_week', 0)
        
        notifications_created = 0
        
        # 1. Create weekly notifications (from current week to week 40)
        notifications_created += PregnancyTrackingHelper._create_weekly_notifications(
            calculation, current_week, due_date
        )
        
        # 2. Create trimester transition notifications
        notifications_created += PregnancyTrackingHelper._create_trimester_notifications(
            calculation, current_week, due_date
        )
        
        # 3. Create milestone notifications
        notifications_created += PregnancyTrackingHelper._create_milestone_notifications(
            calculation, current_week, due_date
        )
        
        # 4. Create prenatal visit reminders
        notifications_created += PregnancyTrackingHelper._create_prenatal_reminders(
            calculation, current_week, due_date
        )
        
        # 5. Create due date approaching notifications
        notifications_created += PregnancyTrackingHelper._create_due_date_reminders(
            calculation, due_date
        )
        
        return notifications_created
    
    @staticmethod
    def _create_weekly_notifications(
        calculation: SavedCalculation,
        current_week: int,
        due_date: date
    ) -> int:
        """Create weekly pregnancy update notifications"""
        notifications_created = 0
        
        # Start from next week
        start_week = current_week + 1
        
        # Create notifications for weeks until week 40
        for week in range(start_week, 41):
            # Calculate notification date (Monday of that week)
            days_from_now = (week - current_week) * 7
            scheduled_date = date.today() + timedelta(days=days_from_now)
            
            # Skip if date is in the past or after due date
            if scheduled_date < date.today() or scheduled_date > due_date + timedelta(days=7):
                continue
            
            # Get baby size for this week
            baby_size = PregnancyTrackingHelper.BABY_SIZES.get(
                week, 'veľké bábätko'
            )
            
            # Calculate trimester
            if week < 13:
                trimester = 1
            elif week < 27:
                trimester = 2
            else:
                trimester = 3
            
            # Calculate days remaining
            days_remaining = (due_date - scheduled_date).days
            
            # Week description
            week_description = f"Vaše bábätko sa neustále vyvíja a rastie."
            if week >= 20:
                week_description = "Bábätko je aktívne a možno už cítite jeho pohyby."
            if week >= 28:
                week_description = "Bábätko pribúda na váhe a pripravuje sa na narodenie."
            if week >= 36:
                week_description = "Bábätko je už plne vyvinuté a pripravené na svet!"
            
            milestone_message = ""
            if week in PregnancyTrackingHelper.MILESTONES:
                milestone_message = f"⭐ MÍĽNIK: {PregnancyTrackingHelper.MILESTONES[week]['name']}"
            
            # Create notification
            ScheduledNotification.objects.create(
                calculation=calculation,
                notification_type='pregnancy_week',
                priority='medium',
                scheduled_date=scheduled_date,
                scheduled_time='09:00:00',
                title=f'Týždeň {week} tehotenstva',
                message=f'Vitaj v týždni {week}! Bábätko je teraz veľké ako {baby_size}.',
                action_url=f'/calculator/pregnancy?id={calculation.id}'
            )
            
            notifications_created += 1
        
        return notifications_created
    
    @staticmethod
    def _create_trimester_notifications(
        calculation: SavedCalculation,
        current_week: int,
        due_date: date
    ) -> int:
        """Create trimester transition notifications"""
        notifications_created = 0
        
        # Trimester transitions: week 13 (2nd trimester), week 27 (3rd trimester)
        trimester_transitions = {
            13: {
                'trimester': 2,
                'description': 'Vitajte v 2. trimestri! Väčšina nepríjemných symptómov 1. trimestra by mala pominúť.'
            },
            27: {
                'trimester': 3,
                'description': 'Vitajte v 3. trimestri! Posledné mesiace pred pôrodom. Bábätko rastie a pripravuje sa na svet.'
            },
        }
        
        for week, data in trimester_transitions.items():
            if week > current_week:
                # Calculate notification date
                days_from_now = (week - current_week) * 7
                scheduled_date = date.today() + timedelta(days=days_from_now)
                
                if scheduled_date < date.today() or scheduled_date > due_date:
                    continue
                
                days_remaining = (due_date - scheduled_date).days
                
                ScheduledNotification.objects.create(
                    calculation=calculation,
                    notification_type='trimester_change',
                    priority='high',
                    scheduled_date=scheduled_date,
                    scheduled_time='09:00:00',
                    title=f'Vitajte v {data["trimester"]}. trimestri!',
                    message=data['description'],
                    action_url=f'/calculator/pregnancy?id={calculation.id}'
                )
                
                notifications_created += 1
        
        return notifications_created
    
    @staticmethod
    def _create_milestone_notifications(
        calculation: SavedCalculation,
        current_week: int,
        due_date: date
    ) -> int:
        """Create milestone notifications for important weeks"""
        notifications_created = 0
        
        for week, milestone_data in PregnancyTrackingHelper.MILESTONES.items():
            if week > current_week:
                # Calculate notification date
                days_from_now = (week - current_week) * 7
                scheduled_date = date.today() + timedelta(days=days_from_now)
                
                if scheduled_date < date.today() or scheduled_date > due_date + timedelta(days=7):
                    continue
                
                days_remaining = (due_date - scheduled_date).days
                
                ScheduledNotification.objects.create(
                    calculation=calculation,
                    notification_type='pregnancy_milestone',
                    priority='high',
                    scheduled_date=scheduled_date,
                    scheduled_time='10:00:00',
                    title=f'🎉 Míľnik: {milestone_data["name"]}',
                    message=milestone_data['description'],
                    action_url=f'/calculator/pregnancy?id={calculation.id}'
                )
                
                notifications_created += 1
        
        return notifications_created
    
    @staticmethod
    def _create_prenatal_reminders(
        calculation: SavedCalculation,
        current_week: int,
        due_date: date
    ) -> int:
        """Create prenatal visit reminder notifications"""
        notifications_created = 0
        
        for week, visit_type in PregnancyTrackingHelper.PRENATAL_VISITS.items():
            if week > current_week:
                # Calculate notification date (3 days before the week)
                days_from_now = (week - current_week) * 7 - 3
                scheduled_date = date.today() + timedelta(days=days_from_now)
                
                if scheduled_date < date.today() or scheduled_date > due_date:
                    continue
                
                visit_description = f"Týždeň {week}: {visit_type}"
                
                ScheduledNotification.objects.create(
                    calculation=calculation,
                    notification_type='prenatal_visit',
                    priority='medium',
                    scheduled_date=scheduled_date,
                    scheduled_time='08:00:00',
                    title=f'Prenatálna kontrola - týždeň {week}',
                    message=f'Nezabudnite: {visit_type}',
                    action_url=f'/calculator/pregnancy?id={calculation.id}'
                )
                
                notifications_created += 1
        
        return notifications_created
    
    @staticmethod
    def _create_due_date_reminders(
        calculation: SavedCalculation,
        due_date: date
    ) -> int:
        """Create due date approaching reminders"""
        notifications_created = 0
        
        # Reminders: 30 days, 14 days, 7 days, 3 days, 1 day before due date
        reminder_days = [30, 14, 7, 3, 1]
        
        for days_before in reminder_days:
            scheduled_date = due_date - timedelta(days=days_before)
            
            if scheduled_date < date.today():
                continue
            
            preparation_tips = ""
            if days_before == 30:
                preparation_tips = "Tip: Pripravte si tašku do pôrodnice."
            elif days_before == 14:
                preparation_tips = "Tip: Dokončite posledné prípravy v detskej izbe."
            elif days_before == 7:
                preparation_tips = "Tip: Majte nabitý telefón a pripravené kontakty na rodinných príslušníkov."
            elif days_before == 3:
                preparation_tips = "Všetko je pripravené! Počúvajte svoje telo a nebojte sa ísť do nemocnice pri akýchkoľvek príznakoch."
            elif days_before == 1:
                preparation_tips = "Termín je zajtra! Každý okamih môže byť ten pravý. Držíme palce! 🍀"
            
            ScheduledNotification.objects.create(
                calculation=calculation,
                notification_type='due_date_approaching',
                priority='high',
                scheduled_date=scheduled_date,
                scheduled_time='10:00:00',
                title=f'Termín pôrodu o {days_before} dní!',
                message=f'Zostáva {days_before} dní do termínu pôrodu. {preparation_tips}',
                action_url=f'/calculator/pregnancy?id={calculation.id}'
            )
            
            notifications_created += 1
        
        return notifications_created


class VacationTrackingHelper:
    """
    Helper for creating vacation-related notifications.
    
    Creates:
    - Quarterly vacation reminders
    - Birthday reminders (33 years milestone)
    - Expiration warnings
    - Vacation planning suggestions
    """
    
    @staticmethod
    def create_notifications(calculation: SavedCalculation) -> int:
        """
        Create all vacation-related notifications for a saved calculation.
        
        Args:
            calculation: SavedCalculation instance with vacation data
        
        Returns:
            Number of notifications created
        """
        params = calculation.params
        result = calculation.result
        
        if not result:
            return 0
        
        notifications_created = 0
        
        # 1. Create quarterly reminders
        notifications_created += VacationTrackingHelper._create_quarterly_reminders(
            calculation, params, result
        )
        
        # 2. Create birthday reminder (33 years)
        notifications_created += VacationTrackingHelper._create_birthday_reminder(
            calculation, params
        )
        
        # 3. Create expiration warnings
        notifications_created += VacationTrackingHelper._create_expiration_warnings(
            calculation, params, result
        )
        
        return notifications_created
    
    @staticmethod
    def _create_quarterly_reminders(
        calculation: SavedCalculation,
        params: Dict[str, Any],
        result: Dict[str, Any]
    ) -> int:
        """Create quarterly vacation check reminders"""
        notifications_created = 0
        
        # Quarterly dates: March 31, June 30, September 30, December 31
        today = date.today()
        current_year = today.year
        
        quarterly_dates = [
            date(current_year, 3, 31),
            date(current_year, 6, 30),
            date(current_year, 9, 30),
            date(current_year, 12, 31),
        ]
        
        remaining_days = result.get('remaining_days', 0)
        used_days = result.get('used_days', 0)
        total_days = result.get('total_days', 0)
        
        for quarterly_date in quarterly_dates:
            # Send reminder 7 days before quarter end
            scheduled_date = quarterly_date - timedelta(days=7)
            
            if scheduled_date < today:
                continue
            
            # Recommendation based on remaining days
            recommendation = ""
            if remaining_days > total_days * 0.7:
                recommendation = "Máte ešte veľa nevyčerpanej dovolenky! Naplánujte si aspoň týždeň."
            elif remaining_days > total_days * 0.3:
                recommendation = "Ideálny čas vyčerpať časť dovolenky. Naplánujte si predĺžený víkend alebo krátku dovolenku."
            else:
                recommendation = "Dobrá práca! Máte dovolenku pod kontrolou."
            
            ScheduledNotification.objects.create(
                calculation=calculation,
                notification_type='vacation_quarterly',
                priority='medium',
                scheduled_date=scheduled_date,
                scheduled_time='09:00:00',
                title='Štvrťročná kontrola dovolenky',
                message=f'Zostáva {remaining_days} dní dovolenky. {recommendation}',
                action_url=f'/calculator/vacation?id={calculation.id}'
            )
            
            notifications_created += 1
        
        return notifications_created
    
    @staticmethod
    def _create_birthday_reminder(
        calculation: SavedCalculation,
        params: Dict[str, Any]
    ) -> int:
        """Create birthday reminder for 33 years milestone (extra vacation days)"""
        notifications_created = 0
        
        # Get birth date from params
        birth_date_str = params.get('birth_date')
        if not birth_date_str:
            return 0
        
        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
        
        # Calculate 33rd birthday
        today = date.today()
        current_year = today.year
        
        birthday_33 = date(current_year, birth_date.month, birth_date.day)
        age_this_year = current_year - birth_date.year
        
        # Adjust if 33rd birthday is next year
        if age_this_year < 32:
            birthday_33 = date(current_year + (33 - age_this_year), birth_date.month, birth_date.day)
        elif age_this_year > 33:
            # Already past 33, skip
            return 0
        
        # Send reminders 2 months and 1 month before
        reminder_dates = [
            birthday_33 - timedelta(days=60),  # 2 months
            birthday_33 - timedelta(days=30),  # 1 month
        ]
        
        for scheduled_date in reminder_dates:
            if scheduled_date < today:
                continue
            
            months_until = (birthday_33 - scheduled_date).days // 30
            
            ScheduledNotification.objects.create(
                calculation=calculation,
                notification_type='birthday_33',
                priority='medium',
                scheduled_date=scheduled_date,
                scheduled_time='09:00:00',
                title=f'O {months_until} mesiacov máte 33 rokov!',
                message=f'Narodeniny: {birthday_33.strftime("%d.%m.%Y")}. Od tohto dátumu máte +5 dní dovolenky navyše!',
                action_url=f'/calculator/vacation?id={calculation.id}'
            )
            
            notifications_created += 1
        
        return notifications_created
    
    @staticmethod
    def _create_expiration_warnings(
        calculation: SavedCalculation,
        params: Dict[str, Any],
        result: Dict[str, Any]
    ) -> int:
        """Create vacation expiration warnings"""
        notifications_created = 0
        
        # In Slovakia, vacation typically expires at the end of the calendar year
        # or by specific company policy date
        
        # Default: December 31 of current year
        today = date.today()
        expiry_date = date(today.year, 12, 31)
        
        # Check if custom expiry date provided
        expiry_date_str = params.get('expiry_date')
        if expiry_date_str:
            expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d').date()
        
        remaining_days = result.get('remaining_days', 0)
        
        if remaining_days <= 0:
            return 0
        
        # Send warnings: 60, 30, 14, 7 days before expiry
        warning_days = [60, 30, 14, 7]
        
        for days_before in warning_days:
            scheduled_date = expiry_date - timedelta(days=days_before)
            
            if scheduled_date < today:
                continue
            
            priority = 'medium'
            if days_before <= 14:
                priority = 'high'
            if days_before <= 7:
                priority = 'urgent'
            
            ScheduledNotification.objects.create(
                calculation=calculation,
                notification_type='vacation_expiry',
                priority=priority,
                scheduled_date=scheduled_date,
                scheduled_time='08:00:00',
                title=f'Dovolenka prepadne o {days_before} dní!',
                message=f'Zostáva {remaining_days} dní dovolenky. Deadline: {expiry_date.strftime("%d.%m.%Y")}',
                action_url=f'/calculator/vacation?id={calculation.id}'
            )
            
            notifications_created += 1
        
        return notifications_created


class MortgageLoanTrackingHelper:
    """
    Helper for creating mortgage/loan-related notifications.
    
    Creates:
    - Monthly payment reminders
    - Milestone notifications (25%, 50%, 75% paid)
    - Interest rate change alerts
    - Extra payment tips
    - Amortization alerts
    """
    
    @staticmethod
    def create_notifications(calculation: SavedCalculation) -> int:
        """
        Create all mortgage/loan-related notifications for a saved calculation.
        
        Args:
            calculation: SavedCalculation instance with mortgage/loan data
        
        Returns:
            Number of notifications created
        """
        params = calculation.params
        result = calculation.result
        
        if not result:
            return 0
        
        notifications_created = 0
        
        # 1. Create monthly payment reminders
        notifications_created += MortgageLoanTrackingHelper._create_payment_reminders(
            calculation, params, result
        )
        
        # 2. Create milestone notifications
        notifications_created += MortgageLoanTrackingHelper._create_milestone_notifications(
            calculation, params, result
        )
        
        # 3. Create extra payment tips (quarterly)
        notifications_created += MortgageLoanTrackingHelper._create_extra_payment_tips(
            calculation, params, result
        )
        
        return notifications_created
    
    @staticmethod
    def _create_payment_reminders(
        calculation: SavedCalculation,
        params: Dict[str, Any],
        result: Dict[str, Any]
    ) -> int:
        """Create monthly payment reminders"""
        notifications_created = 0
        
        # Get payment day (default: 15th of month)
        payment_day = params.get('payment_day', 15)
        monthly_payment = result.get('monthly_payment', 0)
        loan_type = calculation.calculator_type
        
        if monthly_payment <= 0:
            return 0
        
        # Create reminders for next 12 months
        today = date.today()
        
        for month_offset in range(1, 13):
            # Calculate payment date
            payment_month = today.month + month_offset
            payment_year = today.year
            
            while payment_month > 12:
                payment_month -= 12
                payment_year += 1
            
            # Handle day overflow (e.g., Feb 31 -> Feb 28)
            try:
                payment_date = date(payment_year, payment_month, payment_day)
            except ValueError:
                # Invalid day for month, use last day of month
                if payment_month == 12:
                    payment_date = date(payment_year, payment_month, 31)
                else:
                    payment_date = date(payment_year, payment_month + 1, 1) - timedelta(days=1)
            
            # Send reminder 5 days before payment date
            scheduled_date = payment_date - timedelta(days=5)
            
            if scheduled_date < today:
                continue
            
            ScheduledNotification.objects.create(
                calculation=calculation,
                notification_type='payment_due',
                priority='high',
                scheduled_date=scheduled_date,
                scheduled_time='08:00:00',
                title=f'Splátka o 5 dní - {calculation.name}',
                message=f'Suma: {monthly_payment:.2f} €. Splatnosť: {payment_date.strftime("%d.%m.%Y")}',
                action_url=f'/calculator/{loan_type}?id={calculation.id}'
            )
            
            notifications_created += 1
        
        return notifications_created
    
    @staticmethod
    def _create_milestone_notifications(
        calculation: SavedCalculation,
        params: Dict[str, Any],
        result: Dict[str, Any]
    ) -> int:
        """Create milestone notifications (25%, 50%, 75% paid)"""
        notifications_created = 0
        
        principal = params.get('principal', 0)
        if principal <= 0:
            return 0
        
        months = params.get('months', 0) or params.get('term_months', 0)
        if months <= 0:
            return 0
        
        # Milestones at 25%, 50%, 75% of loan term
        milestones = [
            {'percentage': 25, 'months': int(months * 0.25)},
            {'percentage': 50, 'months': int(months * 0.50)},
            {'percentage': 75, 'months': int(months * 0.75)},
        ]
        
        today = date.today()
        loan_type = calculation.calculator_type
        
        for milestone in milestones:
            # Calculate milestone date
            milestone_date = today + timedelta(days=milestone['months'] * 30)
            
            # Don't create notification if it's too far in the future (> 1 year)
            if (milestone_date - today).days > 365:
                continue
            
            paid_percentage = milestone['percentage']
            remaining_percentage = 100 - paid_percentage
            
            paid_amount = principal * (paid_percentage / 100)
            remaining_amount = principal * (remaining_percentage / 100)
            
            ScheduledNotification.objects.create(
                calculation=calculation,
                notification_type='milestone_paid',
                priority='medium',
                scheduled_date=milestone_date,
                scheduled_time='10:00:00',
                title=f'🎉 Splatili ste {paid_percentage}% - {calculation.name}',
                message=f'Gratulujeme! Splatené: {paid_amount:.2f} €, zostáva: {remaining_amount:.2f} €',
                action_url=f'/calculator/{loan_type}?id={calculation.id}'
            )
            
            notifications_created += 1
        
        return notifications_created
    
    @staticmethod
    def _create_extra_payment_tips(
        calculation: SavedCalculation,
        params: Dict[str, Any],
        result: Dict[str, Any]
    ) -> int:
        """Create quarterly tips about extra payments"""
        notifications_created = 0
        
        principal = params.get('principal', 0)
        interest_rate = params.get('interest_rate', 0)
        monthly_payment = result.get('monthly_payment', 0)
        
        if principal <= 0 or interest_rate <= 0:
            return 0
        
        # Suggest extra payment of 5-10% of principal annually
        suggested_extra = principal * 0.05  # 5% of principal
        
        # Rough calculation of savings
        # (This is simplified; real calculation would require amortization schedule)
        estimated_savings = suggested_extra * (interest_rate / 100) * 2
        estimated_months_saved = int((suggested_extra / monthly_payment) * 1.5)
        
        # Create quarterly tips (March, June, September, December)
        today = date.today()
        current_year = today.year
        
        quarterly_dates = [
            date(current_year, 3, 15),
            date(current_year, 6, 15),
            date(current_year, 9, 15),
            date(current_year, 12, 15),
        ]
        
        loan_type = calculation.calculator_type
        
        for tip_date in quarterly_dates:
            if tip_date < today:
                continue
            
            ScheduledNotification.objects.create(
                calculation=calculation,
                notification_type='extra_payment_tip',
                priority='low',
                scheduled_date=tip_date,
                scheduled_time='10:00:00',
                title=f'💡 Tip: Nadplatenie ušetrí ~{estimated_savings:.0f} € - {calculation.name}',
                message=f'Ak zaplatíte {suggested_extra:.0f} € navyše, môžete ušetriť ~{estimated_savings:.0f} € na úrokoch a zkrátiť splácanie o ~{estimated_months_saved} mesiacov.',
                action_url=f'/calculator/{loan_type}?id={calculation.id}'
            )
            
            notifications_created += 1
        
        return notifications_created
