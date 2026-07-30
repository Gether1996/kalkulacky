"""
Vacation Days Calculator Service
Calculates vacation days entitlement based on Slovak labor law.
"""
from decimal import Decimal
from datetime import datetime, date
from typing import Dict, Any
from .base_calculator import BaseCalculator
from . import config_variables as cfg


class VacationCalculator(BaseCalculator):
    """
    Calculates vacation days entitlement according to Slovak labor code.
    
    Slovak vacation rules:
    - Basic entitlement: 4 weeks (20 working days) per year
    - Additional days for age: +1 week (5 days) from age 33
    - Pro-rata calculation for part-year employment
    - Carry-over rules for unused days
    """
    
    # Slovak vacation law parameters (from data/sk_2026.json → vacation)
    BASE_VACATION_DAYS = cfg.VACATION_BASE_DAYS  # 4 weeks
    ADDITIONAL_DAYS_AGE_33 = cfg.VACATION_EXTRA_DAYS_FROM_AGE  # +1 week from age 33
    AGE_THRESHOLD = cfg.VACATION_AGE_THRESHOLD
    
    # Working days
    WORKING_DAYS_PER_WEEK = 5
    WEEKS_PER_YEAR = 52
    
    def calculate(
        self,
        age: int,
        employment_start_date: str,
        current_date: str = None,
        vacation_days_used: float = 0,
        days_carried_over: float = 0,
        planned_vacation_days: float = 0,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Calculate vacation days entitlement and usage.
        
        Parameters:
        - age: Current age in years
        - employment_start_date: Date when employment started (YYYY-MM-DD)
        - current_date: Current date for calculation (defaults to today)
        - vacation_days_used: Number of vacation days already used this year
        - days_carried_over: Vacation days carried over from previous year
        - planned_vacation_days: Number of days planning to take (for remaining calculation)
        
        Returns:
        Dictionary with vacation calculations
        """
        # Convert to appropriate types
        age = int(age)
        employment_start = self._parse_date(employment_start_date)
        current_date = self._parse_date(current_date)
        vacation_days_used = Decimal(str(vacation_days_used))
        days_carried_over = Decimal(str(days_carried_over))
        planned_vacation_days = Decimal(str(planned_vacation_days))
        
        # Validate inputs
        if age < 15 or age > 100:
            raise ValueError("Vek musí byť medzi 15 a 100 rokmi")
        
        if employment_start > current_date:
            raise ValueError("Dátum nástupu nemôže byť v budúcnosti")
        
        # Calculate annual entitlement
        annual_entitlement = self.BASE_VACATION_DAYS
        if age >= self.AGE_THRESHOLD:
            annual_entitlement += self.ADDITIONAL_DAYS_AGE_33
        
        # Check if this is first year of employment
        employment_year = employment_start.year
        current_year = current_date.year
        is_first_year = (employment_year == current_year)
        
        # Calculate pro-rata entitlement for first year
        if is_first_year:
            # Calculate months worked (including partial months)
            months_worked = (current_date.year - employment_start.year) * 12 + \
                          current_date.month - employment_start.month + 1
            
            # Calculate days accrued (pro-rata)
            days_accrued_this_year = Decimal(str(annual_entitlement)) * \
                                   Decimal(str(months_worked)) / Decimal('12')
            days_accrued_this_year = days_accrued_this_year.quantize(Decimal('0.1'))
        else:
            # Full year: entitled to full annual amount
            days_accrued_this_year = Decimal(str(annual_entitlement))
        
        # Calculate total available days (accrued + carried over)
        total_available_days = days_accrued_this_year + days_carried_over
        
        # Calculate remaining days
        remaining_days = total_available_days - vacation_days_used
        
        # Calculate days after planned vacation
        days_after_planned = remaining_days - planned_vacation_days
        
        # Calculate accrual rate (per month)
        accrual_per_month = Decimal(str(annual_entitlement)) / Decimal('12')
        
        # Calculate how many months of vacation days used represents
        if annual_entitlement > 0:
            months_worth_of_vacation_used = float(vacation_days_used) / annual_entitlement * 12
        else:
            months_worth_of_vacation_used = 0
        
        # Days until end of year
        end_of_year = datetime(current_date.year, 12, 31).date()
        days_until_year_end = (end_of_year - current_date).days
        months_until_year_end = (12 - current_date.month)
        
        # Projected accrual by end of year
        projected_accrual_by_year_end = days_accrued_this_year + \
                                       (accrual_per_month * Decimal(str(months_until_year_end)))
        
        # Status checks
        is_over_limit = vacation_days_used > total_available_days
        can_take_planned = remaining_days >= planned_vacation_days
        
        # Calculate weeks representation
        weeks_available = float(remaining_days) / self.WORKING_DAYS_PER_WEEK
        weeks_used = float(vacation_days_used) / self.WORKING_DAYS_PER_WEEK
        
        return {
            'age': age,
            'employment_start_date': employment_start.strftime('%Y-%m-%d'),
            'is_first_year': is_first_year,
            'entitlement': {
                'annual_entitlement': annual_entitlement,
                'base_days': self.BASE_VACATION_DAYS,
                'age_bonus': self.ADDITIONAL_DAYS_AGE_33 if age >= self.AGE_THRESHOLD else 0,
                'has_age_bonus': age >= self.AGE_THRESHOLD,
                'age_threshold': self.AGE_THRESHOLD
            },
            'current_year': {
                'days_accrued': self.round_decimal(days_accrued_this_year, 1),
                'days_carried_over': self.round_decimal(days_carried_over, 1),
                'total_available': self.round_decimal(total_available_days, 1),
                'days_used': self.round_decimal(vacation_days_used, 1),
                'remaining_days': self.round_decimal(remaining_days, 1),
                'weeks_available': self.round_decimal(Decimal(str(weeks_available)), 1),
                'weeks_used': self.round_decimal(Decimal(str(weeks_used)), 1)
            },
            'planning': {
                'planned_vacation_days': self.round_decimal(planned_vacation_days, 1),
                'days_after_planned': self.round_decimal(days_after_planned, 1),
                'can_take_planned': can_take_planned
            },
            'accrual': {
                'accrual_per_month': self.round_decimal(accrual_per_month, 2),
                'months_until_year_end': months_until_year_end,
                'projected_accrual_by_year_end': self.round_decimal(projected_accrual_by_year_end, 1)
            },
            'status': {
                'is_over_limit': is_over_limit,
                'usage_percentage': self.round_decimal(
                    (vacation_days_used / total_available_days * Decimal('100')) 
                    if total_available_days > 0 else Decimal('0'), 
                    1
                )
            }
        }
    
    def _parse_date(self, date_value: Any) -> date:
        """Parse date from string or datetime object."""
        if date_value is None:
            return datetime.now().date()
        
        if isinstance(date_value, datetime):
            return date_value.date()
        
        if isinstance(date_value, date):
            return date_value
        
        if isinstance(date_value, str):
            try:
                return datetime.strptime(date_value, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError(f"Invalid date format: {date_value}. Expected YYYY-MM-DD")
        
        raise ValueError(f"Cannot parse date from type: {type(date_value)}")
    
    def get_metadata(self) -> Dict[str, Any]:
        """Return metadata about the vacation calculator."""
        return {
            'name': 'Vacation Days Calculator',
            'description': 'Calculate vacation days entitlement based on Slovak labor law',
            'version': '1.0.0',
            'parameters': {
                'required': ['age', 'employment_start_date'],
                'optional': ['current_date', 'vacation_days_used', 'days_carried_over', 'planned_vacation_days'],
                'age': {
                    'type': 'integer',
                    'description': 'Current age in years',
                    'min': 15,
                    'max': 100
                },
                'employment_start_date': {
                    'type': 'date',
                    'description': 'Date when employment started (YYYY-MM-DD)'
                },
                'current_date': {
                    'type': 'date',
                    'description': 'Current date for calculation (defaults to today)',
                    'default': 'today'
                },
                'vacation_days_used': {
                    'type': 'decimal',
                    'description': 'Number of vacation days already used this year',
                    'default': 0
                },
                'days_carried_over': {
                    'type': 'decimal',
                    'description': 'Vacation days carried over from previous year',
                    'default': 0
                },
                'planned_vacation_days': {
                    'type': 'decimal',
                    'description': 'Number of days planning to take',
                    'default': 0
                }
            },
            'example_request': {
                'age': 35,
                'employment_start_date': '2020-05-01',
                'vacation_days_used': 8,
                'days_carried_over': 3
            }
        }
