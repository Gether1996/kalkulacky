"""
Pension Calculator Service
Calculates pension estimates, contributions, and retirement planning metrics.
"""
from decimal import Decimal
from typing import Dict, Any
from .base_calculator import BaseCalculator
from . import config_variables as cfg


class PensionCalculator(BaseCalculator):
    """
    Calculates pension-related metrics for Slovak pension system.
    
    Includes:
    - Monthly pension estimate
    - Total contributions (employee + employer)
    - Pension savings accumulation
    - Replacement rate
    - Years to retirement
    """
    
    # Slovak pension system parameters (2026) - imported from config_variables
    RETIREMENT_AGE_MALE = cfg.RETIREMENT_AGE_MALE  # years
    RETIREMENT_AGE_FEMALE = cfg.RETIREMENT_AGE_FEMALE  # years (unified)
    
    # Pension contribution rates (% of gross salary)
    EMPLOYEE_CONTRIBUTION_RATE = cfg.PENSION_EMPLOYEE_CONTRIBUTION_RATE  # 4%
    EMPLOYER_CONTRIBUTION_RATE = cfg.PENSION_EMPLOYER_CONTRIBUTION_RATE  # 14%
    TOTAL_CONTRIBUTION_RATE = cfg.PENSION_TOTAL_CONTRIBUTION_RATE  # 18%
    
    # Average monthly pension (Slovakia 2026 estimate)
    AVERAGE_PENSION_SK = cfg.AVERAGE_PENSION_SK  # EUR
    
    # Pension point value (approximate, simplified)
    PENSION_POINT_VALUE = cfg.PENSION_POINT_VALUE  # EUR per point
    
    def calculate(self, **kwargs) -> Dict[str, Any]:
        """
        Calculate pension estimates and contributions.
        
        Parameters:
        - current_age: Current age in years
        - gross_salary: Monthly gross salary in EUR
        - years_worked: Number of years already worked
        - gender: 'male' or 'female' (affects retirement age)
        - include_second_pillar: Whether contributing to 2nd pillar (default True)
        - second_pillar_rate: 2nd pillar contribution rate (default 6%)
        - average_salary_growth: Expected annual salary growth % (default 2%)
        - pension_valorization: Expected annual pension increase % (default 2%)
        
        Returns:
        Dictionary with pension calculations and projections
        """
        # Extract parameters from kwargs
        current_age = kwargs.get('current_age')
        gross_salary = kwargs.get('gross_salary')
        years_worked = kwargs.get('years_worked')
        gender = kwargs.get('gender', 'male')
        include_second_pillar = kwargs.get('include_second_pillar', True)
        second_pillar_rate = kwargs.get('second_pillar_rate', cfg.SECOND_PILLAR_DEFAULT_RATE)
        
        # Convert to appropriate types
        current_age = int(current_age)
        gross_salary = Decimal(str(gross_salary))
        years_worked = int(years_worked)
        gender = str(gender).lower()
        second_pillar_rate = Decimal(str(second_pillar_rate))
        
        # Validate inputs
        if current_age < 18 or current_age > 70:
            raise ValueError("Vek musí byť medzi 18 a 70 rokmi")
        
        if gross_salary <= 0:
            raise ValueError("Hrubá mzda musí byť väčšia ako 0")
        
        if years_worked < 0 or years_worked > current_age - 18:
            raise ValueError("Neplatný počet odpracovaných rokov")
        
        # Determine retirement age
        retirement_age = self.RETIREMENT_AGE_MALE if gender == 'male' else self.RETIREMENT_AGE_FEMALE
        
        if current_age >= retirement_age:
            years_to_retirement = 0
            already_retired = True
        else:
            years_to_retirement = retirement_age - current_age
            already_retired = False
        
        # Calculate monthly contributions
        if include_second_pillar:
            # With 2nd pillar: contribution split between 1st and 2nd pillar
            first_pillar_rate = self.TOTAL_CONTRIBUTION_RATE - second_pillar_rate
            employee_contribution = gross_salary * (self.EMPLOYEE_CONTRIBUTION_RATE / Decimal('100'))
            employer_contribution = gross_salary * (self.EMPLOYER_CONTRIBUTION_RATE / Decimal('100'))
            second_pillar_contribution = gross_salary * (second_pillar_rate / Decimal('100'))
            first_pillar_contribution = employee_contribution + employer_contribution - second_pillar_contribution
        else:
            # Without 2nd pillar: all goes to 1st pillar
            first_pillar_rate = self.TOTAL_CONTRIBUTION_RATE
            employee_contribution = gross_salary * (self.EMPLOYEE_CONTRIBUTION_RATE / Decimal('100'))
            employer_contribution = gross_salary * (self.EMPLOYER_CONTRIBUTION_RATE / Decimal('100'))
            first_pillar_contribution = employee_contribution + employer_contribution
            second_pillar_contribution = Decimal('0')
        
        total_monthly_contribution = employee_contribution + employer_contribution
        
        # Calculate lifetime contributions
        total_months_worked = years_worked * 12
        total_contributed_so_far = total_monthly_contribution * total_months_worked
        
        # Future contributions until retirement
        future_months = years_to_retirement * 12
        total_future_contributions = total_monthly_contribution * future_months
        
        # Total lifetime contributions
        total_lifetime_contributions = total_contributed_so_far + total_future_contributions
        
        # Estimate monthly pension (simplified calculation)
        # Based on average salary and years worked
        total_years_at_retirement = years_worked + years_to_retirement
        
        # Pension points based on years worked and salary level.
        # ~1 point per year earned at the AVERAGE WAGE (not the average pension).
        salary_ratio = gross_salary / Decimal(str(cfg.AVERAGE_WAGE_MONTHLY))
        pension_points = Decimal(str(total_years_at_retirement)) * salary_ratio
        
        # Calculate estimated monthly pension
        estimated_monthly_pension = pension_points * self.PENSION_POINT_VALUE
        
        # Ensure minimum pension
        minimum_pension = cfg.MINIMUM_PENSION_SK  # Minimum pension in Slovakia
        if estimated_monthly_pension < minimum_pension and total_years_at_retirement >= 30:
            estimated_monthly_pension = minimum_pension
        
        # Replacement rate (pension as % of current salary)
        if gross_salary > 0:
            replacement_rate = (estimated_monthly_pension / gross_salary) * Decimal('100')
        else:
            replacement_rate = Decimal('0')
        
        # Average life expectancy after retirement (years)
        life_expectancy_after_retirement = cfg.LIFE_EXPECTANCY_AFTER_RETIREMENT  # Approximate
        
        # Total pension received over retirement
        total_pension_lifetime = estimated_monthly_pension * 12 * life_expectancy_after_retirement
        
        # Return on contributions (simplified)
        if total_lifetime_contributions > 0:
            roi_percentage = ((total_pension_lifetime - total_lifetime_contributions) / 
                            total_lifetime_contributions) * Decimal('100')
        else:
            roi_percentage = Decimal('0')
        
        return {
            'current_age': current_age,
            'retirement_age': retirement_age,
            'years_to_retirement': years_to_retirement,
            'already_retired': already_retired,
            'years_worked': years_worked,
            'total_years_at_retirement': total_years_at_retirement,
            'gross_salary': self.round_decimal(gross_salary),
            'estimated_monthly_pension': self.round_decimal(estimated_monthly_pension),
            'replacement_rate': self.round_decimal(replacement_rate, 1),
            'contributions': {
                'employee_monthly': self.round_decimal(employee_contribution),
                'employer_monthly': self.round_decimal(employer_contribution),
                'total_monthly': self.round_decimal(total_monthly_contribution),
                'first_pillar_monthly': self.round_decimal(first_pillar_contribution),
                'second_pillar_monthly': self.round_decimal(second_pillar_contribution),
                'total_contributed_so_far': self.round_decimal(total_contributed_so_far),
                'total_future_contributions': self.round_decimal(total_future_contributions),
                'total_lifetime_contributions': self.round_decimal(total_lifetime_contributions)
            },
            'pension_system': {
                'include_second_pillar': include_second_pillar,
                'first_pillar_rate': self.round_decimal(first_pillar_rate, 1),
                'second_pillar_rate': self.round_decimal(second_pillar_rate, 1) if include_second_pillar else Decimal('0'),
                'minimum_pension': self.round_decimal(minimum_pension)
            },
            'projections': {
                'life_expectancy_after_retirement': life_expectancy_after_retirement,
                'total_pension_lifetime': self.round_decimal(total_pension_lifetime),
                'roi_percentage': self.round_decimal(roi_percentage, 1)
            }
        }
    
    def get_metadata(self) -> Dict[str, Any]:
        """Return metadata about the pension calculator."""
        return {
            'name': 'Pension Calculator',
            'description': 'Calculate pension estimates and contributions for Slovak pension system',
            'version': '1.0.0',
            'parameters': {
                'required': ['current_age', 'gross_salary', 'years_worked'],
                'optional': ['gender', 'include_second_pillar', 'second_pillar_rate'],
                'current_age': {
                    'type': 'integer',
                    'description': 'Current age in years',
                    'min': 18,
                    'max': 70
                },
                'gross_salary': {
                    'type': 'decimal',
                    'description': 'Monthly gross salary in EUR',
                    'min': 0
                },
                'years_worked': {
                    'type': 'integer',
                    'description': 'Number of years already worked',
                    'min': 0
                },
                'gender': {
                    'type': 'string',
                    'description': 'Gender (affects retirement age)',
                    'allowed_values': ['male', 'female'],
                    'default': 'male'
                },
                'include_second_pillar': {
                    'type': 'boolean',
                    'description': 'Whether contributing to 2nd pillar',
                    'default': True
                },
                'second_pillar_rate': {
                    'type': 'decimal',
                    'description': '2nd pillar contribution rate %',
                    'default': 6.0
                }
            },
            'example_request': {
                'current_age': 35,
                'gross_salary': 1500,
                'years_worked': 12,
                'gender': 'male',
                'include_second_pillar': True
            }
        }
