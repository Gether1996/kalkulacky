"""
VAT Calculator - Kalkulačka DPH (Daň z pridanej hodnoty)

Calculates VAT (Value Added Tax) for Slovak market.

Search Volume: 5,000+/month
Keywords: "kalkulačka dph", "výpočet dph", "dph kalkulačka"
"""

from decimal import Decimal
from typing import Dict, Any
from .base_calculator import BaseCalculator
from . import config_variables as config


class VATCalculator(BaseCalculator):
    """
    Slovak VAT (DPH) Calculator
    
    All VAT rates are loaded from config_variables.py
    Update config_variables.py to change VAT rates for future years.
    """
    
    # Import Slovak VAT rates from config (2026)
    STANDARD_RATE = config.VAT_RATE_STANDARD      # 23% - základná sadzba
    REDUCED_RATE_1 = config.VAT_RATE_REDUCED_1    # 19% - prvá znížená sadzba
    REDUCED_RATE_2 = config.VAT_RATE_REDUCED_2    # 5% - druhá znížená sadzba
    ZERO_RATE = config.VAT_RATE_ZERO              # 0% - nulová sadzba
    
    def validate_inputs(self, **kwargs) -> bool:
        """Validate VAT calculator inputs"""
        amount = kwargs.get('amount')
        vat_rate = kwargs.get('vat_rate', 20)
        calculation_type = kwargs.get('calculation_type', 'add_vat')
        
        # Validate amount
        if not amount:
            raise ValueError("Suma je povinná")
        try:
            amt = self.to_decimal(amount)
        except (ValueError, TypeError):
            raise ValueError("Suma musí byť platné číslo")
        if amt < 0:
            raise ValueError("Suma nemôže byť záporná")
        
        # Validate VAT rate
        try:
            rate = self.to_decimal(vat_rate)
        except (ValueError, TypeError):
            raise ValueError("Sadzba DPH musí byť platné číslo")
        if rate < 0:
            raise ValueError("Sadzba DPH nemôže byť záporná")
        if rate > 100:
            raise ValueError("Sadzba DPH nemôže byť väčšia ako 100%")
        
        # Validate calculation type
        if calculation_type not in ['add_vat', 'remove_vat']:
            raise ValueError("Typ výpočtu musí byť 'add_vat' alebo 'remove_vat'")
        
        return True
    
    def calculate(
        self, 
        amount: float, 
        vat_rate: float = 23.0,
        calculation_type: str = 'add_vat',
        **kwargs
    ) -> Dict[str, Any]:
        """
        Calculate VAT (add or remove).
        
        Args:
            amount: Base amount in EUR
            vat_rate: VAT rate percentage (default: 23 for Slovak standard rate)
            calculation_type: 'add_vat' (add VAT to amount) or 'remove_vat' (extract VAT from amount)
            
        Returns:
            Dict with:
                - amount_without_vat: Base amount without VAT
                - vat_amount: VAT amount
                - amount_with_vat: Total amount including VAT
                - vat_rate: VAT rate used
        """
        # Validate inputs
        self.validate_inputs(
            amount=amount,
            vat_rate=vat_rate,
            calculation_type=calculation_type
        )
        
        # Convert to Decimal for precise calculations
        amt = self.to_decimal(amount)
        rate = self.to_decimal(vat_rate)
        
        # Calculate based on type
        if calculation_type == 'add_vat':
            # Add VAT to amount
            amount_without_vat = amt
            vat_amount = amt * (rate / Decimal('100'))
            amount_with_vat = amt + vat_amount
        else:  # remove_vat
            # Remove/extract VAT from amount
            amount_with_vat = amt
            amount_without_vat = amt / (Decimal('1') + (rate / Decimal('100')))
            vat_amount = amt - amount_without_vat
        
        # Prepare result
        result = {
            'calculation_type': calculation_type,
            'vat_rate': float(rate),
            'amount_without_vat': self.round_money(amount_without_vat),
            'vat_amount': self.round_money(vat_amount),
            'amount_with_vat': self.round_money(amount_with_vat),
            
            # Breakdown
            'breakdown': {
                'base_amount': self.round_money(amount_without_vat),
                'vat_percentage': float(rate),
                'vat_amount': self.round_money(vat_amount),
                'total_with_vat': self.round_money(amount_with_vat),
            },
            
            # Common Slovak VAT rates for reference (2026)
            'slovak_vat_rates': {
                'standard': float(self.STANDARD_RATE),           # 23%
                'reduced_1': float(self.REDUCED_RATE_1),         # 19%
                'reduced_2': float(self.REDUCED_RATE_2),         # 5%
                'zero': float(self.ZERO_RATE),                   # 0%
            }
        }
        
        self.result = result
        return result
    
    def calculate_both_directions(self, amount: float, vat_rate: float = 23.0) -> Dict[str, Any]:
        """
        Calculate VAT in both directions (add and remove) for comparison.
        
        Useful for showing users both scenarios.
        """
        add_result = self.calculate(amount, vat_rate, 'add_vat')
        remove_result = self.calculate(amount, vat_rate, 'remove_vat')
        
        return {
            'add_vat': add_result,
            'remove_vat': remove_result,
        }


# Example usage and testing
if __name__ == '__main__':
    calc = VATCalculator()
    
    print("Slovak VAT (DPH) Calculator 2026\n")
    
    # Test: Add VAT to €100
    print("=" * 50)
    print("Scenario 1: Add 23% VAT to €100 (2026)")
    print("=" * 50)
    result = calc.calculate(amount=100, vat_rate=23, calculation_type='add_vat')
    print(f"Amount without VAT: €{result['amount_without_vat']:,.2f}")
    print(f"VAT (23%): €{result['vat_amount']:,.2f}")
    print(f"Amount with VAT: €{result['amount_with_vat']:,.2f}")
    
    print("\n" + "=" * 50)
    print("Scenario 2: Remove 23% VAT from €123")
    print("=" * 50)
    result = calc.calculate(amount=123, vat_rate=23, calculation_type='remove_vat')
    print(f"Amount with VAT: €123.00")
    print(f"VAT (23%): €{result['vat_amount']:,.2f}")
    print(f"Amount without VAT: €{result['amount_without_vat']:,.2f}")
    
    print("\n" + "=" * 50)
    print("Both directions for €500:")
    print("=" * 50)
    both = calc.calculate_both_directions(amount=500, vat_rate=23)
    print(f"Add VAT: €500 → €{both['add_vat']['amount_with_vat']:,.2f}")
    print(f"Remove VAT: €500 → €{both['remove_vat']['amount_without_vat']:,.2f}")
