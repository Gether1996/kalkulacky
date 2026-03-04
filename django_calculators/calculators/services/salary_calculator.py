"""
Salary Calculator - Čistá mzda (Net Salary)

Calculates Slovak net salary from gross salary based on 2026 tax laws.

Search Volume: 12,000+/month
Keywords: "čistá mzda kalkulačka", "výpočet čistej mzdy"
"""

from decimal import Decimal
from typing import Dict, Any
from .base_calculator import BaseCalculator
from . import config_variables as config


class SalaryCalculator(BaseCalculator):
    """
    Slovak Net Salary Calculator (2026)
    
    All tax rates and constants are loaded from config_variables.py
    Update config_variables.py to change tax rates for future years.
    """
    
    # Import all constants from config (2026 Tax Configuration)
    # Employee contributions
    SOCIAL_INSURANCE_RATE = config.SOCIAL_INSURANCE_RATE_EMPLOYEE
    HEALTH_INSURANCE_RATE = config.HEALTH_INSURANCE_RATE_EMPLOYEE
    HEALTH_INSURANCE_RATE_DISABILITY = config.HEALTH_INSURANCE_RATE_DISABILITY
    
    # Employer contributions (simplified - single rate)
    EMPLOYER_CONTRIBUTIONS_RATE = config.EMPLOYER_CONTRIBUTIONS_RATE
    
    # Progressive tax rates
    TAX_RATE_1 = config.TAX_RATE_BRACKET_1
    TAX_RATE_2 = config.TAX_RATE_BRACKET_2
    TAX_RATE_3 = config.TAX_RATE_BRACKET_3
    TAX_RATE_4 = config.TAX_RATE_BRACKET_4
    
    # Tax thresholds
    TAX_THRESHOLD_1_YEARLY = config.TAX_THRESHOLD_1_YEARLY
    TAX_THRESHOLD_2_YEARLY = config.TAX_THRESHOLD_2_YEARLY
    TAX_THRESHOLD_3_YEARLY = config.TAX_THRESHOLD_3_YEARLY
    TAX_THRESHOLD_1_MONTHLY = config.TAX_THRESHOLD_1_MONTHLY
    TAX_THRESHOLD_2_MONTHLY = config.TAX_THRESHOLD_2_MONTHLY
    TAX_THRESHOLD_3_MONTHLY = config.TAX_THRESHOLD_3_MONTHLY
    
    # Non-taxable amount (NČZD)
    NON_TAXABLE_AMOUNT_YEARLY = config.NON_TAXABLE_AMOUNT_YEARLY
    NON_TAXABLE_AMOUNT_MONTHLY = config.NON_TAXABLE_AMOUNT_MONTHLY
    NON_TAXABLE_AMOUNT_DISABILITY_YEARLY = config.NON_TAXABLE_AMOUNT_DISABILITY_YEARLY
    NON_TAXABLE_AMOUNT_DISABILITY_MONTHLY = config.NON_TAXABLE_AMOUNT_DISABILITY_MONTHLY
    
    # Child tax bonus
    CHILD_TAX_BONUS_UNDER_15 = config.CHILD_TAX_BONUS_UNDER_15
    CHILD_TAX_BONUS_15_TO_18 = config.CHILD_TAX_BONUS_15_TO_18
    
    # Social insurance limits
    SOCIAL_INSURANCE_MAX_BASE_MONTHLY = config.SOCIAL_INSURANCE_MAX_BASE_MONTHLY
    
    def validate_inputs(self, **kwargs) -> bool:
        """Validate salary calculator inputs"""
        gross_salary = kwargs.get('gross_salary')
        
        if not gross_salary:
            raise ValueError("gross_salary is required")
        
        try:
            gross = self.to_decimal(gross_salary)
        except (ValueError, TypeError):
            raise ValueError("gross_salary must be a valid number")
        
        if gross <= 0:
            raise ValueError("gross_salary must be greater than 0")
        
        if gross > 50000:
            raise ValueError("gross_salary seems unrealistically high (>€50,000/month)")
        
        return True
    
    def calculate(self, gross_salary: float, children_under_15: int = 0, children_15_to_18: int = 0, apply_nontaxable_amount: bool = True, has_disability: bool = False, **kwargs) -> Dict[str, Any]:
        """
        Calculate net salary from gross salary.
        
        Args:
            gross_salary: Gross monthly salary in EUR
            children_under_15: Number of dependent children under 15 years (100 EUR/month each)
            children_15_to_18: Number of dependent children 15-18 years (50 EUR/month each)
            apply_nontaxable_amount: Whether to apply non-taxable amount (NČZD) - default True
            has_disability: Whether person has disability (ZŤP) - reduces health insurance to 2.5% (instead of 5%)
            
        Returns:
            Dict with:
                - gross_salary: Original gross salary
                - social_insurance: Social insurance contribution
                - health_insurance: Health insurance contribution
                - tax_base: Base for tax calculation (after insurances)
                - non_taxable_amount: Non-taxable amount applied (NČZD)
                - taxable_base: Base after deducting non-taxable amount
                - income_tax: Income tax amount (before child bonus)
                - child_tax_bonus: Tax bonus for children (if applicable)
                - final_tax: Final tax after child bonus
                - net_salary: Final net salary
                - effective_tax_rate: Effective tax rate as percentage
        """
        # Validate inputs
        self.validate_inputs(gross_salary=gross_salary)
        
        # Convert to Decimal for precise calculations
        gross = self.to_decimal(gross_salary)
        children_under_15 = int(children_under_15) if children_under_15 else 0
        children_15_to_18 = int(children_15_to_18) if children_15_to_18 else 0
        total_children = children_under_15 + children_15_to_18
        
        # 1. Calculate Social Insurance (9.4%)
        # Note: There's a maximum base for social insurance
        social_insurance_base = min(gross, self.SOCIAL_INSURANCE_MAX_BASE_MONTHLY)
        social_insurance = social_insurance_base * self.SOCIAL_INSURANCE_RATE
        
        # 2. Calculate Health Insurance (5% or 2.5% for ZŤP)
        health_ins_rate = self.HEALTH_INSURANCE_RATE_DISABILITY if has_disability else self.HEALTH_INSURANCE_RATE
        health_insurance = gross * health_ins_rate
        
        # 3. Calculate Tax Base (gross minus insurances)
        tax_base = gross - social_insurance - health_insurance
        
        # 4. Apply Non-Taxable Amount (NČZD) - deducted BEFORE tax calculation (if applicable)
        non_taxable_amount = self.NON_TAXABLE_AMOUNT_MONTHLY if apply_nontaxable_amount else Decimal('0')
        taxable_base = max(Decimal('0'), tax_base - non_taxable_amount)
        
        # 5. Calculate Income Tax from taxable base - Progressive 4-bracket system (2026)
        income_tax_before_child_bonus = Decimal('0')
        
        if taxable_base <= Decimal('0'):
            # No tax if taxable base is 0 or negative
            income_tax_before_child_bonus = Decimal('0')
        elif taxable_base <= self.TAX_THRESHOLD_1_MONTHLY:
            # Bracket 1: 19% up to €3,665.28/month (€43,983.32/year)
            income_tax_before_child_bonus = taxable_base * self.TAX_RATE_1
        elif taxable_base <= self.TAX_THRESHOLD_2_MONTHLY:
            # Bracket 2: 19% up to threshold 1, then 25% up to threshold 2
            bracket_1 = self.TAX_THRESHOLD_1_MONTHLY * self.TAX_RATE_1
            bracket_2 = (taxable_base - self.TAX_THRESHOLD_1_MONTHLY) * self.TAX_RATE_2
            income_tax_before_child_bonus = bracket_1 + bracket_2
        elif taxable_base <= self.TAX_THRESHOLD_3_MONTHLY:
            # Bracket 3: Brackets 1+2 + 30% up to threshold 3
            bracket_1 = self.TAX_THRESHOLD_1_MONTHLY * self.TAX_RATE_1
            bracket_2 = (self.TAX_THRESHOLD_2_MONTHLY - self.TAX_THRESHOLD_1_MONTHLY) * self.TAX_RATE_2
            bracket_3 = (taxable_base - self.TAX_THRESHOLD_2_MONTHLY) * self.TAX_RATE_3
            income_tax_before_child_bonus = bracket_1 + bracket_2 + bracket_3
        else:
            # Bracket 4: Brackets 1+2+3 + 35% above threshold 3
            bracket_1 = self.TAX_THRESHOLD_1_MONTHLY * self.TAX_RATE_1
            bracket_2 = (self.TAX_THRESHOLD_2_MONTHLY - self.TAX_THRESHOLD_1_MONTHLY) * self.TAX_RATE_2
            bracket_3 = (self.TAX_THRESHOLD_3_MONTHLY - self.TAX_THRESHOLD_2_MONTHLY) * self.TAX_RATE_3
            bracket_4 = (taxable_base - self.TAX_THRESHOLD_3_MONTHLY) * self.TAX_RATE_4
            income_tax_before_child_bonus = bracket_1 + bracket_2 + bracket_3 + bracket_4
        
        # 6. Apply Child Tax Bonus (if applicable) - reduces tax (cannot be negative)
        child_tax_bonus_total = Decimal('0')
        if children_under_15 > 0 or children_15_to_18 > 0:
            # Calculate bonus for each age group
            bonus_under_15 = self.CHILD_TAX_BONUS_UNDER_15 * children_under_15
            bonus_15_to_18 = self.CHILD_TAX_BONUS_15_TO_18 * children_15_to_18
            total_bonus = bonus_under_15 + bonus_15_to_18
            
            # Bonus cannot exceed the tax amount
            child_tax_bonus_total = min(income_tax_before_child_bonus, total_bonus)
        
        final_tax = max(Decimal('0'), income_tax_before_child_bonus - child_tax_bonus_total)
        
        # 7. Calculate Net Salary
        net_salary = gross - social_insurance - health_insurance - final_tax
        
        # 8. Calculate Effective Tax Rate
        total_deductions = social_insurance + health_insurance + final_tax
        effective_tax_rate = (total_deductions / gross * 100) if gross > 0 else Decimal('0')
        
        # 9. Calculate Super-Gross Salary (Superhrubá mzda) - Total employer cost
        # Simplified: Gross × 36.2% for employer contributions
        total_employer_contributions = gross * self.EMPLOYER_CONTRIBUTIONS_RATE
        super_gross_salary = gross + total_employer_contributions
        
        # 10. Prepare result (matching frontend SalaryCalculationResponse interface)
        result = {
            'gross_salary': self.round_money(gross),
            'social_insurance': self.round_money(social_insurance),
            'health_insurance': self.round_money(health_insurance),
            'tax_base': self.round_money(tax_base),
            'non_taxable_amount': self.round_money(non_taxable_amount),
            'taxable_base': self.round_money(taxable_base),
            'income_tax': self.round_money(income_tax_before_child_bonus),
            'child_tax_bonus': self.round_money(child_tax_bonus_total),
            'children_under_15': children_under_15,
            'children_15_to_18': children_15_to_18,
            'total_children': total_children,
            'apply_nontaxable_amount': apply_nontaxable_amount,
            'has_disability': has_disability,
            'final_tax': self.round_money(final_tax),
            'net_salary': self.round_money(net_salary),
            'effective_tax_rate': self.round_money(effective_tax_rate),
            
            # Super-gross salary (employer cost)
            'super_gross_salary': self.round_money(super_gross_salary),
            'total_employer_contributions': self.round_money(total_employer_contributions),
            
            # Additional fields for detailed view
            'total_insurance': self.round_money(social_insurance + health_insurance),
            'total_deductions': self.round_money(total_deductions),
            
            # Breakdown for detailed view
            'breakdown': {
                'gross_salary': self.round_money(gross),
                'minus_social_insurance': self.round_money(social_insurance),
                'minus_health_insurance': self.round_money(health_insurance),
                'equals_tax_base': self.round_money(tax_base),
                'minus_non_taxable_amount': self.round_money(non_taxable_amount),
                'equals_taxable_base': self.round_money(taxable_base),
                'tax_before_child_bonus': self.round_money(income_tax_before_child_bonus),
                'child_tax_bonus': self.round_money(child_tax_bonus_total),
                'final_tax': self.round_money(final_tax),
                'net_salary': self.round_money(net_salary),
            },
            
            # Yearly projections
            'yearly': {
                'gross': self.round_money(gross * 12),
                'net': self.round_money(net_salary * 12),
                'total_deductions': self.round_money(total_deductions * 12),
            },
            
            # Rates used (2026 progressive system)
            'rates': {
                'social_insurance_rate': float(self.SOCIAL_INSURANCE_RATE * 100),
                'health_insurance_rate': float(health_ins_rate * 100),
                'health_insurance_rate_regular': float(self.HEALTH_INSURANCE_RATE * 100),
                'health_insurance_rate_disability': float(self.HEALTH_INSURANCE_RATE_DISABILITY * 100),
                'employer_contributions_rate': float(self.EMPLOYER_CONTRIBUTIONS_RATE * 100),
                'tax_rate_applied': self._get_applicable_tax_rate(taxable_base),
                'non_taxable_amount_monthly': float(self.NON_TAXABLE_AMOUNT_MONTHLY),
                'child_tax_bonus_under_15': float(self.CHILD_TAX_BONUS_UNDER_15),
                'child_tax_bonus_15_to_18': float(self.CHILD_TAX_BONUS_15_TO_18),
                'tax_brackets': {
                    'bracket_1': {'rate': 19, 'up_to_monthly': float(self.TAX_THRESHOLD_1_MONTHLY)},
                    'bracket_2': {'rate': 25, 'up_to_monthly': float(self.TAX_THRESHOLD_2_MONTHLY)},
                    'bracket_3': {'rate': 30, 'up_to_monthly': float(self.TAX_THRESHOLD_3_MONTHLY)},
                    'bracket_4': {'rate': 35, 'above': float(self.TAX_THRESHOLD_3_MONTHLY)},
                }
            }
        }
        
        self.result = result
        return result
    
    def _get_applicable_tax_rate(self, taxable_base: Decimal) -> float:
        """Get the highest applicable tax rate based on taxable base"""
        if taxable_base <= Decimal('0'):
            return 0.0
        elif taxable_base <= self.TAX_THRESHOLD_1_MONTHLY:
            return float(self.TAX_RATE_1 * 100)
        elif taxable_base <= self.TAX_THRESHOLD_2_MONTHLY:
            return float(self.TAX_RATE_2 * 100)
        elif taxable_base <= self.TAX_THRESHOLD_3_MONTHLY:
            return float(self.TAX_RATE_3 * 100)
        else:
            return float(self.TAX_RATE_4 * 100)


# Example usage and testing
if __name__ == '__main__':
    calc = SalaryCalculator()
    
    # Test with common salaries
    test_salaries = [1000, 1500, 2000, 3000, 5000]
    
    print("Slovak Net Salary Calculator 2026\n")
    print(f"{'Gross':>10} | {'Social Ins.':>12} | {'Health Ins.':>12} | {'Tax':>10} | {'Net':>10} | {'Effective Rate':>15}")
    print("-" * 90)
    
    for salary in test_salaries:
        result = calc.calculate(gross_salary=salary)
        print(f"€{result['gross']:>9.2f} | €{result['social_insurance']:>11.2f} | €{result['health_insurance']:>11.2f} | €{result['income_tax']:>9.2f} | €{result['net']:>9.2f} | {result['effective_tax_rate']:>14.2f}%")
