"""
Parental Benefit Calculator Service
Rodičovský príspevok kalkulačka - výpočet materských a rodičovských dávok na Slovensku

Calculates:
- Maternity benefit (Materské)
- Parental benefit basic (Rodičovský príspevok - osnova)
- Parental benefit alternative (Rodičovský príspevok - alternatíva)
- Timeline and expiration dates
- Work compatibility check
"""
from decimal import Decimal
from datetime import datetime, timedelta, date
from typing import Dict, Any
from .base_calculator import BaseCalculator
from . import config_variables as cfg


class ParentalBenefitCalculator(BaseCalculator):
    """
    Slovak Parental Benefit Calculator (2026)
    
    Includes:
    - Maternity benefit calculation (Materské)
    - Parental benefit basic (osnova)
    - Parental benefit alternative (alternatíva)
    - Timeline planning
    - Work compatibility
    """
    
    # Slovak parental benefit rates (2026) - imported from config_variables
    MATERNITY_RATE = cfg.MATERNITY_BENEFIT_RATE  # 75% of daily assessment base
    MATERNITY_WEEKS = cfg.MATERNITY_BENEFIT_WEEKS  # 34 weeks
    MATERNITY_WEEKS_TWINS = cfg.MATERNITY_BENEFIT_WEEKS_TWINS  # 43 weeks for twins+
    
    PARENTAL_BASIC_MONTHLY = cfg.PARENTAL_BENEFIT_BASIC_MONTHLY  # €381.90/month
    PARENTAL_BASIC_YEARS = cfg.PARENTAL_BENEFIT_BASIC_YEARS  # 3 years (until child is 3)
    
    PARENTAL_ALT_MONTHLY = cfg.PARENTAL_BENEFIT_ALT_MONTHLY  # €270/month
    PARENTAL_ALT_YEARS = cfg.PARENTAL_BENEFIT_ALT_YEARS  # 6 years (until child is 6)
    
    # Work income limits while receiving parental benefit
    WORK_INCOME_LIMIT_BASIC = cfg.PARENTAL_WORK_INCOME_LIMIT_BASIC  # €635.70/month for basic
    WORK_INCOME_LIMIT_ALT = cfg.PARENTAL_WORK_INCOME_LIMIT_ALT  # €635.70/month for alternative
    
    # Minimum health insurance assessment base
    MIN_ASSESSMENT_BASE_MONTHLY = cfg.PARENTAL_MIN_ASSESSMENT_BASE  # €915/month (minimálna mzda 2026)
    
    def calculate(
        self,
        birth_date: str,
        gross_salary: float = None,
        benefit_type: str = 'basic',
        twins_or_more: bool = False,
        plan_to_work: bool = False,
        planned_monthly_income: float = 0,
        second_child_birth_date: str = None,
        current_date: str = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Calculate parental benefit details.
        
        Parameters:
        - birth_date: Child's date of birth (YYYY-MM-DD)
        - gross_salary: Mother's gross monthly salary before maternity (for materské calculation)
        - benefit_type: 'basic' (osnova) or 'alternative' (alternatíva)
        - twins_or_more: Whether birth was twins/triplets (affects maternity duration)
        - plan_to_work: Whether parent plans to work while receiving benefit
        - planned_monthly_income: Expected monthly income if working (gross)
        - second_child_birth_date: If planning second child, date of birth (extends benefit)
        - current_date: Current date for calculations (defaults to today)
        
        Returns:
        Dictionary with parental benefit calculations and timeline
        """
        # Parse dates
        birth_date = self._parse_date(birth_date)
        current_date = self._parse_date(current_date) if current_date else datetime.now().date()
        
        # Validate birth date
        if birth_date > current_date:
            raise ValueError("Dátum narodenia nemôže byť v budúcnosti")
        
        # Child age in days, months, years
        age_days = (current_date - birth_date).days
        age_months = age_days // 30
        age_years = age_days // 365
        
        # Validate benefit type
        if benefit_type not in ['basic', 'alternative']:
            raise ValueError("Typ príspevku musí byť 'basic' alebo 'alternative'")
        
        # --- MATERNITY BENEFIT (Materské) ---
        maternity_weeks = self.MATERNITY_WEEKS if not twins_or_more else self.MATERNITY_WEEKS_TWINS
        maternity_end_date = birth_date + timedelta(weeks=maternity_weeks)
        
        maternity_benefit = None
        if gross_salary and gross_salary > 0:
            # Calculate daily assessment base (DVZ)
            yearly_salary = Decimal(str(gross_salary)) * 12
            daily_assessment_base = yearly_salary / 365
            
            # Maternity benefit = 70% of DVZ
            daily_maternity = daily_assessment_base * self.MATERNITY_RATE
            weekly_maternity = daily_maternity * 7
            monthly_maternity = daily_maternity * 30
            total_maternity = daily_maternity * (maternity_weeks * 7)
            
            maternity_benefit = {
                'daily_amount': float(daily_maternity.quantize(Decimal('0.01'))),
                'weekly_amount': float(weekly_maternity.quantize(Decimal('0.01'))),
                'monthly_amount': float(monthly_maternity.quantize(Decimal('0.01'))),
                'total_amount': float(total_maternity.quantize(Decimal('0.01'))),
                'duration_weeks': maternity_weeks,
                'end_date': maternity_end_date.strftime('%Y-%m-%d'),
                'daily_assessment_base': float(daily_assessment_base.quantize(Decimal('0.01')))
            }
        
        # --- PARENTAL BENEFIT (Rodičovský príspevok) ---
        # Starts after maternity ends
        parental_start_date = maternity_end_date
        
        if benefit_type == 'basic':
            monthly_benefit = self.PARENTAL_BASIC_MONTHLY
            benefit_years = self.PARENTAL_BASIC_YEARS
            work_limit = self.WORK_INCOME_LIMIT_BASIC
        else:  # alternative
            monthly_benefit = self.PARENTAL_ALT_MONTHLY
            benefit_years = self.PARENTAL_ALT_YEARS
            work_limit = self.WORK_INCOME_LIMIT_ALT
        
        # Calculate end date (child reaches age limit)
        benefit_end_date = birth_date + timedelta(days=365 * benefit_years)
        
        # Total benefit amount
        total_months = benefit_years * 12
        total_benefit = monthly_benefit * total_months
        
        # Remaining months
        if current_date < parental_start_date:
            # Still on maternity
            remaining_months = total_months
            benefit_status = 'Ešte ste na materskej'
        elif current_date >= benefit_end_date:
            # Benefit expired
            remaining_months = 0
            benefit_status = 'Rodičovský príspevok skončil'
        else:
            # Currently receiving parental benefit
            elapsed_days = (current_date - parental_start_date).days
            elapsed_months = elapsed_days // 30
            remaining_months = total_months - elapsed_months
            benefit_status = 'Poberáte rodičovský príspevok'
        
        # --- WORK COMPATIBILITY CHECK ---
        can_work = True
        work_warning = None
        
        if plan_to_work and planned_monthly_income > 0:
            planned_income = Decimal(str(planned_monthly_income))
            
            if planned_income > work_limit:
                can_work = False
                work_warning = (
                    f"POZOR! Váš plánovaný príjem €{planned_income:.2f}/mes prevyšuje limit "
                    f"€{work_limit:.2f}/mes. Stratíte nárok na rodičovský príspevok!"
                )
            else:
                work_warning = (
                    f"Môžete pracovať. Váš príjem €{planned_income:.2f}/mes je pod limitom "
                    f"€{work_limit:.2f}/mes."
                )
        
        # --- SECOND CHILD EXTENSION ---
        second_child_extension = None
        if second_child_birth_date:
            second_birth = self._parse_date(second_child_birth_date)
            
            # If second child is born before first child benefit expires
            if second_birth < benefit_end_date:
                # Benefit extends for second child
                new_end_date = second_birth + timedelta(days=365 * benefit_years)
                extension_months = ((new_end_date - benefit_end_date).days // 30)
                
                second_child_extension = {
                    'second_child_birth': second_birth.strftime('%Y-%m-%d'),
                    'original_end_date': benefit_end_date.strftime('%Y-%m-%d'),
                    'new_end_date': new_end_date.strftime('%Y-%m-%d'),
                    'extension_months': extension_months,
                    'additional_amount': float(monthly_benefit * extension_months)
                }
        
        # --- COMPARISON: Basic vs Alternative ---
        comparison = self._compare_benefit_types(
            birth_date,
            current_date,
            maternity_end_date
        )
        
        # --- NOTIFICATIONS & MILESTONES ---
        notifications = self._generate_notifications(
            current_date,
            benefit_end_date,
            maternity_end_date,
            benefit_type
        )
        
        # --- RETURN RESULTS ---
        return {
            # Child info
            'birth_date': birth_date.strftime('%Y-%m-%d'),
            'child_age_days': age_days,
            'child_age_months': age_months,
            'child_age_years': age_years,
            
            # Maternity benefit
            'maternity_benefit': maternity_benefit,
            'maternity_end_date': maternity_end_date.strftime('%Y-%m-%d'),
            
            # Parental benefit
            'benefit_type': benefit_type,
            'benefit_type_label': 'Rodičovská osnova (3 roky)' if benefit_type == 'basic' else 'Rodičovská alternatíva (6 rokov)',
            'monthly_benefit': float(monthly_benefit),
            'parental_start_date': parental_start_date.strftime('%Y-%m-%d'),
            'parental_end_date': benefit_end_date.strftime('%Y-%m-%d'),
            'total_months': total_months,
            'remaining_months': max(0, remaining_months),
            'total_benefit': float(total_benefit),
            'benefit_status': benefit_status,
            
            # Work compatibility
            'can_work_and_receive': can_work,
            'work_income_limit': float(work_limit),
            'work_warning': work_warning,
            
            # Second child extension
            'second_child_extension': second_child_extension,
            
            # Comparison
            'comparison': comparison,
            
            # Notifications
            'notifications': notifications,
            
            # Progress percentage
            'progress_percentage': round(
                ((total_months - remaining_months) / total_months * 100) if total_months > 0 else 0,
                1
            )
        }
    
    def _compare_benefit_types(
        self,
        birth_date: date,
        current_date: date,
        maternity_end_date: date
    ) -> Dict[str, Any]:
        """Compare basic vs alternative benefit types"""
        
        # Basic (osnova)
        basic_end = birth_date + timedelta(days=365 * self.PARENTAL_BASIC_YEARS)
        basic_months = self.PARENTAL_BASIC_YEARS * 12
        basic_total = self.PARENTAL_BASIC_MONTHLY * basic_months
        
        # Alternative (alternatíva)
        alt_end = birth_date + timedelta(days=365 * self.PARENTAL_ALT_YEARS)
        alt_months = self.PARENTAL_ALT_YEARS * 12
        alt_total = self.PARENTAL_ALT_MONTHLY * alt_months
        
        # Difference
        difference = basic_total - alt_total
        
        return {
            'basic': {
                'monthly_amount': float(self.PARENTAL_BASIC_MONTHLY),
                'duration_months': basic_months,
                'duration_years': self.PARENTAL_BASIC_YEARS,
                'total_amount': float(basic_total),
                'end_date': basic_end.strftime('%Y-%m-%d')
            },
            'alternative': {
                'monthly_amount': float(self.PARENTAL_ALT_MONTHLY),
                'duration_months': alt_months,
                'duration_years': self.PARENTAL_ALT_YEARS,
                'total_amount': float(alt_total),
                'end_date': alt_end.strftime('%Y-%m-%d')
            },
            'difference': float(difference),
            'recommendation': (
                'Osnova je výhodnejšia ak plánujete vrátiť sa do práce skôr (vyššia mesačná suma).'
                if difference > 0 else
                'Alternatíva je výhodnejšia ak chcete zostať doma dlhšie (celková suma je nižšia, ale dlhšie trvanie).'
            )
        }
    
    def _generate_notifications(
        self,
        current_date: date,
        benefit_end_date: date,
        maternity_end_date: date,
        benefit_type: str
    ) -> list:
        """Generate notification events"""
        notifications = []
        
        # Maternity ending soon
        days_to_maternity_end = (maternity_end_date - current_date).days
        if 0 < days_to_maternity_end <= 30:
            notifications.append({
                'type': 'maternity_ending',
                'title': 'Materská čoskoro končí',
                'message': f'O {days_to_maternity_end} dní končí materská. Začína rodičovský príspevok.',
                'days_until': days_to_maternity_end,
                'priority': 'high'
            })
        
        # Parental benefit ending soon
        days_to_benefit_end = (benefit_end_date - current_date).days
        
        if days_to_benefit_end == 180:  # 6 months
            notifications.append({
                'type': 'benefit_6months',
                'title': 'Rodičovský príspevok končí o 6 mesiacov',
                'message': 'Pripravte sa na návrat do práce alebo plánujte ďalšie riešenie.',
                'days_until': 180,
                'priority': 'medium'
            })
        
        if days_to_benefit_end == 90:  # 3 months
            notifications.append({
                'type': 'benefit_3months',
                'title': 'Rodičovský príspevok končí o 3 mesiace',
                'message': 'Čas dohodnúť návrat do práce alebo hľadať škôlku/jasle.',
                'days_until': 90,
                'priority': 'high'
            })
        
        if days_to_benefit_end == 30:  # 1 month
            notifications.append({
                'type': 'benefit_1month',
                'title': 'Rodičovský príspevok končí o 1 mesiac!',
                'message': 'Posledný mesiac rodičovského príspevku.',
                'days_until': 30,
                'priority': 'urgent'
            })
        
        return notifications
    
    def _parse_date(self, date_value: Any) -> date:
        """Parse date from string or datetime object."""
        if date_value is None:
            return datetime.now().date()
        
        if isinstance(date_value, date):
            return date_value
        
        if isinstance(date_value, datetime):
            return date_value.date()
        
        if isinstance(date_value, str):
            try:
                return datetime.strptime(date_value, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError(f"Invalid date format: {date_value}. Expected YYYY-MM-DD")
        
        raise ValueError(f"Cannot parse date from type: {type(date_value)}")
