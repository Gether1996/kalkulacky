"""
Hours Worked Calculator Service
Calculate work hours, overtime, total hours per period, and earnings.
"""
from decimal import Decimal
from typing import Dict, Any
from .base_calculator import BaseCalculator


class HoursWorkedCalculator(BaseCalculator):
    """
    Calculate hours worked, overtime, and related earnings.
    
    Includes:
    - Total hours worked
    - Regular vs overtime hours
    - Earnings calculation
    - Work period analysis
    - Efficiency metrics
    """
    
    # Standard work hours (Slovakia)
    STANDARD_HOURS_PER_DAY = Decimal('8')
    STANDARD_HOURS_PER_WEEK = Decimal('40')
    STANDARD_HOURS_PER_MONTH = Decimal('160')  # Approx 4 weeks
    
    # Overtime multipliers (Slovakia)
    OVERTIME_MULTIPLIER_BASIC = Decimal('1.25')  # 25% extra
    OVERTIME_MULTIPLIER_WEEKEND = Decimal('1.5')  # 50% extra
    OVERTIME_MULTIPLIER_HOLIDAY = Decimal('2.0')  # 100% extra
    
    def calculate(
        self,
        hours_worked: float,
        hourly_rate: float = None,
        standard_hours: float = None,
        overtime_hours: float = None,
        weekend_hours: float = 0,
        holiday_hours: float = 0,
        period_type: str = 'weekly',
        **kwargs
    ) -> Dict[str, Any]:
        """
        Calculate hours worked and earnings.
        
        Parameters:
        - hours_worked: Total hours worked in the period
        - hourly_rate: Rate per hour (optional, for earnings calculation)
        - standard_hours: Standard hours for the period (optional, default based on period_type)
        - overtime_hours: Overtime hours (optional, calculated if not provided)
        - weekend_hours: Hours worked on weekends (optional, for higher overtime rate)
        - holiday_hours: Hours worked on holidays (optional, for highest overtime rate)
        - period_type: Type of period - 'daily', 'weekly', 'monthly', 'custom' (optional, default 'weekly')
        
        Returns:
        Dictionary with hours and earnings calculations
        """
        hours_worked = Decimal(str(hours_worked))
        hourly_rate = Decimal(str(hourly_rate)) if hourly_rate is not None else None
        period_type = str(period_type)
        weekend_hours = Decimal(str(weekend_hours))
        holiday_hours = Decimal(str(holiday_hours))
        
        # Validate inputs
        if hours_worked < 0:
            raise ValueError("Odpracované hodiny nesmú byť záporné")
        
        if hours_worked > 744:  # 31 days * 24 hours
            raise ValueError("Odpracované hodiny nemôžu presiahnuť 744 (31 dní)")
        
        if hourly_rate is not None and hourly_rate < 0:
            raise ValueError("Hodinová sadzba nesmie byť záporná")
        
        if weekend_hours < 0 or holiday_hours < 0:
            raise ValueError("Víkendové a sviatkové hodiny nesmú byť záporné")
        
        if weekend_hours + holiday_hours > hours_worked:
            raise ValueError("Víkendové a sviatkové hodiny nemôžu byť viac ako celkové hodiny")
        
        # Determine standard hours for the period
        if standard_hours is not None:
            standard_hours = Decimal(str(standard_hours))
        else:
            if period_type == 'daily':
                standard_hours = self.STANDARD_HOURS_PER_DAY
            elif period_type == 'weekly':
                standard_hours = self.STANDARD_HOURS_PER_WEEK
            elif period_type == 'monthly':
                standard_hours = self.STANDARD_HOURS_PER_MONTH
            else:  # custom
                standard_hours = Decimal('0')
        
        # Calculate regular and overtime hours
        if overtime_hours is not None:
            overtime_hours = Decimal(str(overtime_hours))
            regular_hours = hours_worked - overtime_hours
        else:
            if hours_worked > standard_hours:
                overtime_hours = hours_worked - standard_hours
                regular_hours = standard_hours
            else:
                overtime_hours = Decimal('0')
                regular_hours = hours_worked
        
        # Calculate different types of overtime
        # Priority: holiday > weekend > regular overtime
        holiday_overtime = min(holiday_hours, overtime_hours)
        remaining_overtime = overtime_hours - holiday_overtime
        
        weekend_overtime = min(weekend_hours, remaining_overtime)
        remaining_overtime = remaining_overtime - weekend_overtime
        
        regular_overtime = remaining_overtime
        
        # Calculate earnings if hourly rate is provided
        earnings = None
        overtime_earnings = None
        total_earnings = None
        
        if hourly_rate is not None:
            regular_earnings = regular_hours * hourly_rate
            
            regular_overtime_earnings = regular_overtime * hourly_rate * self.OVERTIME_MULTIPLIER_BASIC
            weekend_overtime_earnings = weekend_overtime * hourly_rate * self.OVERTIME_MULTIPLIER_WEEKEND
            holiday_overtime_earnings = holiday_overtime * hourly_rate * self.OVERTIME_MULTIPLIER_HOLIDAY
            
            overtime_earnings = regular_overtime_earnings + weekend_overtime_earnings + holiday_overtime_earnings
            total_earnings = regular_earnings + overtime_earnings
            
            earnings = {
                'regular_earnings': self.round_decimal(regular_earnings),
                'overtime_earnings': self.round_decimal(overtime_earnings),
                'overtime_breakdown': {
                    'regular_overtime': self.round_decimal(regular_overtime_earnings),
                    'weekend_overtime': self.round_decimal(weekend_overtime_earnings),
                    'holiday_overtime': self.round_decimal(holiday_overtime_earnings)
                },
                'total_earnings': self.round_decimal(total_earnings),
                'average_hourly_effective': self.round_decimal(total_earnings / hours_worked if hours_worked > 0 else Decimal('0'), 2)
            }
        
        # Calculate percentages
        overtime_percentage = (overtime_hours / hours_worked * Decimal('100')) if hours_worked > 0 else Decimal('0')
        regular_percentage = (regular_hours / hours_worked * Decimal('100')) if hours_worked > 0 else Decimal('0')
        
        # Work-life balance analysis
        if period_type == 'weekly':
            if hours_worked <= 40:
                balance_category = "Výborný"
                balance_description = "Zdravý work-life balance"
            elif hours_worked <= 50:
                balance_category = "Dobrý"
                balance_description = "Mierne nadčasy"
            elif hours_worked <= 60:
                balance_category = "Upozornenie"
                balance_description = "Vysoké nadčasy"
            else:
                balance_category = "Kritický"
                balance_description = "Nadmerné pracovné zaťaženie"
        elif period_type == 'monthly':
            if hours_worked <= 160:
                balance_category = "Výborný"
                balance_description = "Zdravý work-life balance"
            elif hours_worked <= 200:
                balance_category = "Dobrý"
                balance_description = "Mierne nadčasy"
            elif hours_worked <= 240:
                balance_category = "Upozornenie"
                balance_description = "Vysoké nadčasy"
            else:
                balance_category = "Kritický"
                balance_description = "Nadmerné pracovné zaťaženie"
        else:
            balance_category = "Neurčený"
            balance_description = "Nedá sa určiť bez kontextu obdobia"
        
        # Daily average (if period type is known)
        daily_average = None
        if period_type == 'weekly':
            daily_average = hours_worked / Decimal('5')  # 5 work days
        elif period_type == 'monthly':
            daily_average = hours_worked / Decimal('20')  # Approx 20 work days
        
        return {
            'hours': {
                'total_hours': self.round_decimal(hours_worked, 2),
                'regular_hours': self.round_decimal(regular_hours, 2),
                'overtime_hours': self.round_decimal(overtime_hours, 2),
                'standard_hours': self.round_decimal(standard_hours, 2),
                'overtime_breakdown': {
                    'regular_overtime': self.round_decimal(regular_overtime, 2),
                    'weekend_overtime': self.round_decimal(weekend_overtime, 2),
                    'holiday_overtime': self.round_decimal(holiday_overtime, 2)
                }
            },
            'percentages': {
                'regular_percentage': self.round_decimal(regular_percentage, 2),
                'overtime_percentage': self.round_decimal(overtime_percentage, 2)
            },
            'earnings': earnings,
            'analysis': {
                'period_type': period_type,
                'balance_category': balance_category,
                'balance_description': balance_description,
                'daily_average': self.round_decimal(daily_average, 2) if daily_average else None,
                'exceeds_standard': hours_worked > standard_hours,
                'excess_hours': self.round_decimal(hours_worked - standard_hours, 2) if hours_worked > standard_hours else Decimal('0')
            },
            'rates': {
                'hourly_rate': self.round_decimal(hourly_rate, 2) if hourly_rate else None,
                'multipliers': {
                    'basic': float(self.OVERTIME_MULTIPLIER_BASIC),
                    'weekend': float(self.OVERTIME_MULTIPLIER_WEEKEND),
                    'holiday': float(self.OVERTIME_MULTIPLIER_HOLIDAY)
                }
            }
        }
    
    def get_metadata(self) -> Dict[str, Any]:
        """Return metadata about the hours worked calculator."""
        return {
            'name': 'Hours Worked Calculator',
            'description': 'Calculate work hours, overtime, and earnings',
            'version': '1.0.0',
            'parameters': {
                'required': ['hours_worked'],
                'optional': ['hourly_rate', 'standard_hours', 'overtime_hours', 'weekend_hours', 'holiday_hours', 'period_type'],
                'hours_worked': {
                    'type': 'decimal',
                    'description': 'Total hours worked in the period',
                    'min': 0,
                    'max': 744
                },
                'hourly_rate': {
                    'type': 'decimal',
                    'description': 'Rate per hour',
                    'min': 0,
                    'default': None
                },
                'standard_hours': {
                    'type': 'decimal',
                    'description': 'Standard hours for the period',
                    'min': 0,
                    'default': 'auto based on period_type'
                },
                'overtime_hours': {
                    'type': 'decimal',
                    'description': 'Overtime hours (calculated if not provided)',
                    'min': 0,
                    'default': 'auto calculated'
                },
                'weekend_hours': {
                    'type': 'decimal',
                    'description': 'Hours worked on weekends',
                    'min': 0,
                    'default': 0
                },
                'holiday_hours': {
                    'type': 'decimal',
                    'description': 'Hours worked on holidays',
                    'min': 0,
                    'default': 0
                },
                'period_type': {
                    'type': 'string',
                    'description': 'Type of period',
                    'choices': ['daily', 'weekly', 'monthly', 'custom'],
                    'default': 'weekly'
                }
            },
            'example_request': {
                'hours_worked': 48,
                'hourly_rate': 12.50,
                'period_type': 'weekly',
                'weekend_hours': 0,
                'holiday_hours': 0
            }
        }
