"""
Percentage Calculator - Kalkulačka percent

Calculates various percentage operations.

Search Volume: 4,000+/month
Keywords: "kalkulačka percent", "výpočet percent"
"""

from decimal import Decimal
from typing import Dict, Any
from .base_calculator import BaseCalculator


class PercentageCalculator(BaseCalculator):
    """
    Percentage Calculator
    
    Supports multiple calculation types:
    - What is X% of Y?
    - X is what % of Y?
    - What number is X% of Y?
    - Percentage change/difference
    - Add X% to Y
    - Subtract X% from Y
    """
    
    def validate_inputs(self, **kwargs) -> bool:
        """Validate percentage calculator inputs"""
        calculation_type = kwargs.get('calculation_type')
        
        if not calculation_type:
            raise ValueError("Typ výpočtu je povinný")
        
        valid_types = [
            'percent_of',  # What is X% of Y?
            'is_what_percent',  # X is what % of Y?
            'percentage_change',  # % change from X to Y
            'add_percent',  # Add X% to Y
            'subtract_percent'  # Subtract X% from Y
        ]
        
        if calculation_type not in valid_types:
            raise ValueError(f"Typ výpočtu musí byť jeden z: {', '.join(valid_types)}")
        
        return True
    
    def calculate(
        self, 
        calculation_type: str,
        value1: float = None,
        value2: float = None,
        percent: float = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Calculate percentage based on calculation type.
        
        Args:
            calculation_type: Type of calculation to perform
            value1: First value (optional depending on type)
            value2: Second value (optional depending on type)
            percent: Percentage value (optional depending on type)
            
        Returns:
            Dictionary with calculation results
        """
        # Validate inputs
        self.validate_inputs(calculation_type=calculation_type)
        
        result = {
            'calculation_type': calculation_type,
            'input_values': {}
        }
        
        if calculation_type == 'percent_of':
            # What is X% of Y?
            if percent is None or value2 is None:
                raise ValueError("Pre výpočet 'X% z Y' sú potrebné hodnoty percent a základná hodnota")
            
            percent_dec = self.to_decimal(percent)
            value2_dec = self.to_decimal(value2)
            
            result_value = (percent_dec / Decimal('100')) * value2_dec
            
            result.update({
                'input_values': {
                    'percent': float(percent_dec),
                    'of_value': float(value2_dec)
                },
                'result': float(result_value),
                'formula': f"{percent}% of {value2} = {float(result_value)}"
            })
        
        elif calculation_type == 'is_what_percent':
            # X is what % of Y?
            if value1 is None or value2 is None:
                raise ValueError("Pre výpočet 'X je koľko % z Y' sú potrebné obe hodnoty")
            
            value1_dec = self.to_decimal(value1)
            value2_dec = self.to_decimal(value2)
            
            if value2_dec == 0:
                raise ValueError("Základná hodnota nemôže byť nula")
            
            percent_result = (value1_dec / value2_dec) * Decimal('100')
            
            result.update({
                'input_values': {
                    'value': float(value1_dec),
                    'of_value': float(value2_dec)
                },
                'result': float(percent_result),
                'formula': f"{value1} is {float(percent_result)}% of {value2}"
            })
        
        elif calculation_type == 'percentage_change':
            # Percentage change from X to Y
            if value1 is None or value2 is None:
                raise ValueError("Pre výpočet percentuálnej zmeny sú potrebné pôvodná a nová hodnota")
            
            value1_dec = self.to_decimal(value1)
            value2_dec = self.to_decimal(value2)
            
            if value1_dec == 0:
                raise ValueError("Pôvodná hodnota nemôže byť nula")
            
            change = value2_dec - value1_dec
            percent_change = (change / value1_dec) * Decimal('100')
            
            result.update({
                'input_values': {
                    'original_value': float(value1_dec),
                    'new_value': float(value2_dec)
                },
                'absolute_change': float(change),
                'percent_change': float(percent_change),
                'result': float(percent_change),
                'is_increase': change > 0,
                'formula': f"Change from {value1} to {value2} is {float(percent_change)}%"
            })
        
        elif calculation_type == 'add_percent':
            # Add X% to Y
            if percent is None or value2 is None:
                raise ValueError("Pre pridanie percent sú potrebné hodnoty percent a základná hodnota")
            
            percent_dec = self.to_decimal(percent)
            value2_dec = self.to_decimal(value2)
            
            increase_amount = (percent_dec / Decimal('100')) * value2_dec
            result_value = value2_dec + increase_amount
            
            result.update({
                'input_values': {
                    'percent': float(percent_dec),
                    'base_value': float(value2_dec)
                },
                'increase_amount': float(increase_amount),
                'result': float(result_value),
                'formula': f"{value2} + {percent}% = {float(result_value)}"
            })
        
        elif calculation_type == 'subtract_percent':
            # Subtract X% from Y
            if percent is None or value2 is None:
                raise ValueError("Pre odpočítanie percent sú potrebné hodnoty percent a základná hodnota")
            
            percent_dec = self.to_decimal(percent)
            value2_dec = self.to_decimal(value2)
            
            decrease_amount = (percent_dec / Decimal('100')) * value2_dec
            result_value = value2_dec - decrease_amount
            
            result.update({
                'input_values': {
                    'percent': float(percent_dec),
                    'base_value': float(value2_dec)
                },
                'decrease_amount': float(decrease_amount),
                'result': float(result_value),
                'formula': f"{value2} - {percent}% = {float(result_value)}"
            })
        
        self.result = result
        return result
    
    @staticmethod
    def to_decimal(value) -> Decimal:
        """Convert value to Decimal for precise calculations"""
        if isinstance(value, Decimal):
            return value
        if value is None:
            return None
        return Decimal(str(value))
