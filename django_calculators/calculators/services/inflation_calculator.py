"""
Inflation Calculator Service
Calculate the real value of money over time, accounting for inflation.
"""
from decimal import Decimal
from typing import Dict, Any, List
from .base_calculator import BaseCalculator
from . import config_variables as cfg


class InflationCalculator(BaseCalculator):
    """
    Calculate inflation impact on money value over time.
    
    Includes:
    - Real value calculation
    - Purchasing power
    - Required future value
    - Cumulative inflation
    - Year-by-year breakdown
    """
    
    # Average inflation rate - imported from config_variables
    DEFAULT_INFLATION_RATE = cfg.DEFAULT_INFLATION_RATE  # 3% default rate
    
    def calculate(
        self,
        present_value: float,
        years: int,
        inflation_rate: float = None,
        calculate_reverse: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Calculate inflation impact on money value.
        
        Parameters:
        - present_value: Current value of money
        - years: Number of years for projection
        - inflation_rate: Annual inflation rate in percentage (optional, default 3%)
        - calculate_reverse: If True, calculate what past money is worth now (optional)
        
        Returns:
        Dictionary with inflation calculations
        """
        present_value = Decimal(str(present_value))
        years = int(years)
        inflation_rate = Decimal(str(inflation_rate if inflation_rate is not None else self.DEFAULT_INFLATION_RATE))
        calculate_reverse = bool(calculate_reverse)
        
        # Validate inputs
        if present_value <= 0:
            raise ValueError("Súčasná hodnota musí byť kladná")
        
        if years < 1:
            raise ValueError("Počet rokov musí byť aspoň 1")
        
        if years > 100:
            raise ValueError("Počet rokov nemôže presiahnuť 100")
        
        if inflation_rate < -10 or inflation_rate > 50:
            raise ValueError("Inflácia musí byť medzi -10% a 50%")
        
        # Convert percentage to decimal
        inflation_decimal = inflation_rate / Decimal('100')
        
        if calculate_reverse:
            # Calculate what money from the past is worth now
            # Future Value = Present Value × (1 + inflation)^years
            future_value = present_value * ((Decimal('1') + inflation_decimal) ** years)
            total_inflation = future_value - present_value
            purchasing_power = Decimal('100') * ((Decimal('1') + inflation_decimal) ** years)
        else:
            # Calculate what today's money will be worth in the future
            # Present Value = Future Value / (1 + inflation)^years
            future_value = present_value / ((Decimal('1') + inflation_decimal) ** years)
            total_inflation = present_value - future_value
            purchasing_power = Decimal('100') / ((Decimal('1') + inflation_decimal) ** years)
        
        # Value needed in the future to have same purchasing power as present_value today
        required_future_value = present_value * ((Decimal('1') + inflation_decimal) ** years)
        
        # Calculate cumulative inflation
        cumulative_inflation_rate = (((Decimal('1') + inflation_decimal) ** years) - Decimal('1')) * Decimal('100')
        
        # Average annual loss/gain
        avg_annual_change = total_inflation / Decimal(str(years))
        
        # Year by year breakdown (limit to 50 years for performance)
        yearly_breakdown = []
        max_breakdown_years = min(years, 50)
        
        for year in range(1, max_breakdown_years + 1):
            if calculate_reverse:
                year_value = present_value * ((Decimal('1') + inflation_decimal) ** year)
                year_change = year_value - (present_value * ((Decimal('1') + inflation_decimal) ** (year - 1)) if year > 1 else present_value)
            else:
                year_value = present_value / ((Decimal('1') + inflation_decimal) ** year)
                year_prev = present_value / ((Decimal('1') + inflation_decimal) ** (year - 1)) if year > 1 else present_value
                year_change = year_prev - year_value
            
            year_inflation = (((Decimal('1') + inflation_decimal) ** year) - Decimal('1')) * Decimal('100')
            year_purchasing_power = (Decimal('100') / ((Decimal('1') + inflation_decimal) ** year)) if not calculate_reverse else (Decimal('100') * ((Decimal('1') + inflation_decimal) ** year))
            
            yearly_breakdown.append({
                'year': year,
                'value': self.round_decimal(year_value),
                'change': self.round_decimal(year_change),
                'cumulative_inflation': self.round_decimal(year_inflation, 2),
                'purchasing_power': self.round_decimal(year_purchasing_power, 2)
            })
        
        # Comparison with common inflation rates
        comparison = []
        common_rates = [Decimal('2'), Decimal('3'), Decimal('5'), Decimal('10')]
        
        for rate in common_rates:
            if rate == inflation_rate:
                continue
            
            rate_decimal = rate / Decimal('100')
            if calculate_reverse:
                rate_value = present_value * ((Decimal('1') + rate_decimal) ** years)
            else:
                rate_value = present_value / ((Decimal('1') + rate_decimal) ** years)
            
            difference = rate_value - future_value
            
            comparison.append({
                'inflation_rate': float(rate),
                'value': self.round_decimal(rate_value),
                'difference': self.round_decimal(difference),
                'difference_percent': self.round_decimal((difference / present_value) * Decimal('100'), 2)
            })
        
        # Calculate purchasing power categories
        if not calculate_reverse:
            if purchasing_power >= 90:
                power_category = "Výborná kúpna sila"
                power_description = "Minimálna strata hodnoty"
            elif purchasing_power >= 70:
                power_category = "Dobrá kúpna sila"
                power_description = "Prijateľná strata hodnoty"
            elif purchasing_power >= 50:
                power_category = "Stredná kúpna sila"
                power_description = "Výrazná strata hodnoty"
            elif purchasing_power >= 30:
                power_category = "Nízka kúpna sila"
                power_description = "Veľká strata hodnoty"
            else:
                power_category = "Veľmi nízka kúpna sila"
                power_description = "Kritická strata hodnoty"
        else:
            power_category = "Rast hodnoty"
            power_description = "Hodnota narastá s infláciou"
        
        return {
            'input': {
                'present_value': self.round_decimal(present_value),
                'years': years,
                'inflation_rate': float(inflation_rate),
                'calculation_type': 'reverse' if calculate_reverse else 'forward'
            },
            'result': {
                'future_value': self.round_decimal(future_value),
                'total_inflation': self.round_decimal(total_inflation),
                'total_inflation_percent': self.round_decimal((total_inflation / present_value) * Decimal('100'), 2),
                'purchasing_power': self.round_decimal(purchasing_power, 2),
                'required_future_value': self.round_decimal(required_future_value),
                'cumulative_inflation_rate': self.round_decimal(cumulative_inflation_rate, 2),
                'avg_annual_change': self.round_decimal(avg_annual_change)
            },
            'analysis': {
                'power_category': power_category,
                'power_description': power_description,
                'yearly_loss': self.round_decimal(avg_annual_change),
                'effective_rate': float(inflation_rate)
            },
            'yearly_breakdown': yearly_breakdown,
            'comparison': comparison
        }
    
    def get_metadata(self) -> Dict[str, Any]:
        """Return metadata about the inflation calculator."""
        return {
            'name': 'Inflation Calculator',
            'description': 'Calculate the real value of money over time accounting for inflation',
            'version': '1.0.0',
            'parameters': {
                'required': ['present_value', 'years'],
                'optional': ['inflation_rate', 'calculate_reverse'],
                'present_value': {
                    'type': 'decimal',
                    'description': 'Current value of money',
                    'min': 0.01
                },
                'years': {
                    'type': 'integer',
                    'description': 'Number of years for projection',
                    'min': 1,
                    'max': 100
                },
                'inflation_rate': {
                    'type': 'decimal',
                    'description': 'Annual inflation rate in percentage',
                    'min': -10,
                    'max': 50,
                    'default': 3.0
                },
                'calculate_reverse': {
                    'type': 'boolean',
                    'description': 'Calculate what past money is worth now',
                    'default': False
                }
            },
            'example_request': {
                'present_value': 10000,
                'years': 10,
                'inflation_rate': 3.0,
                'calculate_reverse': False
            }
        }
