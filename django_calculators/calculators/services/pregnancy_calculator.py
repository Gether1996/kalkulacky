"""
Pregnancy Calculator Service
Calculates due date, current week, trimester, and other pregnancy metrics.
"""
from datetime import datetime, timedelta, date
from typing import Dict, Any
from .base_calculator import BaseCalculator


class PregnancyCalculator(BaseCalculator):
    """
    Calculates pregnancy-related dates and information.
    
    Supports two calculation methods:
    1. From Last Menstrual Period (LMP) - standard method
    2. From conception date (ovulation date)
    """
    
    # Pregnancy duration constants
    PREGNANCY_DAYS = 280  # 40 weeks from LMP
    CONCEPTION_TO_BIRTH_DAYS = 266  # 38 weeks from conception
    
    def calculate(
        self,
        calculation_method: str,
        lmp_date: str = None,
        conception_date: str = None,
        current_date: str = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Calculate pregnancy dates and information.
        
        Parameters:
        - calculation_method: 'lmp' or 'conception'
        - lmp_date: Last menstrual period date (if method is 'lmp')
        - conception_date: Conception/ovulation date (if method is 'conception')
        - current_date: Optional - date to calculate from (defaults to today)
        
        Returns:
        Dictionary with:
        - due_date: Estimated delivery date
        - conception_date: Estimated conception date
        - current_week: Current week of pregnancy
        - current_day: Current day within the week
        - total_days_pregnant: Total days since conception
        - days_remaining: Days until due date
        - trimester: Current trimester (1, 2, or 3)
        - trimester_progress: Percentage of current trimester completed
        - is_past_due: Boolean indicating if past due date
        - weeks_description: Human-readable description
        """
        method = calculation_method
        current_date = self._parse_date(current_date)
        
        if method == 'lmp':
            if not lmp_date:
                raise ValueError("lmp_date is required when calculation_method is 'lmp'")
            lmp_date = self._parse_date(lmp_date)
            due_date = self._calculate_due_date_from_lmp(lmp_date)
            conception_date = lmp_date + timedelta(days=14)  # Typical ovulation day
            
        elif method == 'conception':
            if not conception_date:
                raise ValueError("conception_date is required when calculation_method is 'conception'")
            conception_date = self._parse_date(conception_date)
            due_date = conception_date + timedelta(days=self.CONCEPTION_TO_BIRTH_DAYS)
            lmp_date = conception_date - timedelta(days=14)
            
        else:
            raise ValueError("calculation_method must be 'lmp' or 'conception'")
        
        # Validate dates
        if current_date < lmp_date:
            raise ValueError("Current date cannot be before LMP date")
        
        # Calculate pregnancy progress
        days_since_lmp = (current_date - lmp_date).days
        days_remaining = (due_date - current_date).days
        
        # Calculate weeks and days
        current_week = days_since_lmp // 7
        current_day = days_since_lmp % 7
        
        # Determine trimester
        if current_week < 13:
            trimester = 1
            trimester_start_week = 0
            trimester_end_week = 12
        elif current_week < 27:
            trimester = 2
            trimester_start_week = 13
            trimester_end_week = 26
        else:
            trimester = 3
            trimester_start_week = 27
            trimester_end_week = 40
        
        # Calculate trimester progress
        trimester_weeks = trimester_end_week - trimester_start_week + 1
        weeks_into_trimester = current_week - trimester_start_week
        trimester_progress = round((weeks_into_trimester / trimester_weeks) * 100, 1)
        
        # Check if past due
        is_past_due = current_date > due_date
        
        # Create human-readable description
        if current_week == 0:
            weeks_description = f"{days_since_lmp} dní"
        else:
            weeks_description = f"{current_week} týždňov a {current_day} dní"
        
        # Calculate percentage of pregnancy completed
        pregnancy_progress = round((days_since_lmp / self.PREGNANCY_DAYS) * 100, 1)
        
        return {
            'due_date': due_date.strftime('%Y-%m-%d'),
            'lmp_date': lmp_date.strftime('%Y-%m-%d'),
            'conception_date': conception_date.strftime('%Y-%m-%d'),
            'current_week': current_week,
            'current_day': current_day,
            'total_days_pregnant': days_since_lmp,
            'days_remaining': days_remaining if days_remaining > 0 else 0,
            'trimester': trimester,
            'trimester_progress': trimester_progress,
            'pregnancy_progress': pregnancy_progress,
            'is_past_due': is_past_due,
            'weeks_description': weeks_description,
            'calculation_method': method
        }
    
    def _parse_date(self, date_value: Any) -> datetime:
        """Parse date from string or datetime object."""
        if date_value is None:
            return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        if isinstance(date_value, datetime):
            return date_value.replace(hour=0, minute=0, second=0, microsecond=0)
        
        if isinstance(date_value, date):
            return datetime.combine(date_value, datetime.min.time())
        
        if isinstance(date_value, str):
            try:
                return datetime.strptime(date_value, '%Y-%m-%d')
            except ValueError:
                raise ValueError(f"Invalid date format: {date_value}. Expected YYYY-MM-DD")
        
        raise ValueError(f"Cannot parse date from type: {type(date_value)}")
    
    def _calculate_due_date_from_lmp(self, lmp_date: datetime) -> datetime:
        """
        Calculate due date using Naegele's Rule: LMP + 280 days.
        """
        return lmp_date + timedelta(days=self.PREGNANCY_DAYS)
    
    def get_metadata(self) -> Dict[str, Any]:
        """Return metadata about the pregnancy calculator."""
        return {
            'name': 'Pregnancy Calculator',
            'description': 'Calculate pregnancy due date, current week, and trimester',
            'version': '1.0.0',
            'parameters': {
                'required': ['calculation_method'],
                'optional': ['current_date'],
                'calculation_method': {
                    'type': 'string',
                    'description': 'Calculation method: lmp or conception',
                    'allowed_values': ['lmp', 'conception']
                },
                'lmp_date': {
                    'type': 'date',
                    'description': 'Last menstrual period date (YYYY-MM-DD)',
                    'required_if': 'calculation_method=lmp'
                },
                'conception_date': {
                    'type': 'date',
                    'description': 'Conception/ovulation date (YYYY-MM-DD)',
                    'required_if': 'calculation_method=conception'
                },
                'current_date': {
                    'type': 'date',
                    'description': 'Current date for calculation (defaults to today)',
                    'default': 'today'
                }
            },
            'example_request': {
                'calculation_method': 'lmp',
                'lmp_date': '2024-01-01'
            }
        }
