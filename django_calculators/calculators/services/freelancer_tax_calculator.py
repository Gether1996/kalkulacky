"""
Freelancer Tax Calculator Service
Calculates taxes and contributions for self-employed persons (SZČO) in Slovakia.
"""
from decimal import Decimal
from typing import Dict, Any
from .base_calculator import BaseCalculator
from . import config_variables as cfg


class FreelancerTaxCalculator(BaseCalculator):
    """
    Calculates taxes and social contributions for freelancers (SZČO) in Slovakia.
    
    Includes:
    - Income tax (19% or 25%)
    - Health insurance contributions
    - Social security contributions
    - Net income calculation
    """
    
    # 2026 Slovak tax rates and limits - imported from config_variables
    TAX_RATE_LOW = cfg.FREELANCER_TAX_RATE_LOW  # 19% tax rate
    TAX_RATE_HIGH = cfg.FREELANCER_TAX_RATE_HIGH  # 25% tax rate for higher incomes
    TAX_THRESHOLD = cfg.FREELANCER_TAX_THRESHOLD  # Annual income threshold for higher tax rate (2026)
    
    # Health insurance
    HEALTH_INSURANCE_RATE = cfg.FREELANCER_HEALTH_INSURANCE_RATE  # 14%
    MIN_HEALTH_BASE_MONTHLY = cfg.FREELANCER_MIN_HEALTH_BASE_MONTHLY  # Minimum monthly base for health insurance (2026)
    
    # Social insurance contributions (rates for SZČO)
    SOCIAL_SICKNESS_RATE = cfg.FREELANCER_SOCIAL_SICKNESS_RATE  # 1.4% - voluntary
    SOCIAL_PENSION_RATE = cfg.FREELANCER_SOCIAL_PENSION_RATE  # 18%
    SOCIAL_DISABILITY_RATE = cfg.FREELANCER_SOCIAL_DISABILITY_RATE  # 6%
    SOCIAL_ACCIDENT_RATE = cfg.FREELANCER_SOCIAL_ACCIDENT_RATE  # 0.8%
    SOCIAL_GUARANTEE_RATE = cfg.FREELANCER_SOCIAL_GUARANTEE_RATE  # 0.25%
    SOCIAL_RESERVE_RATE = cfg.FREELANCER_SOCIAL_RESERVE_RATE  # 4.75%
    
    MIN_SOCIAL_BASE_MONTHLY = cfg.FREELANCER_MIN_SOCIAL_BASE_MONTHLY  # Minimum monthly base for social insurance (2026)
    
    # Flat expense rate (paušálne výdavky)
    FLAT_EXPENSE_RATE = cfg.FREELANCER_FLAT_EXPENSE_RATE  # 60% flat expenses
    
    # Non-taxable amount per person per year
    NON_TAXABLE_AMOUNT_ANNUAL = cfg.FREELANCER_NON_TAXABLE_AMOUNT_ANNUAL  # €4,579.26/year (2026)
    
    def calculate(
        self,
        annual_revenue: float,
        annual_expenses: float = 0,
        use_flat_expenses: bool = True,
        include_sickness: bool = True,
        months_active: int = 12,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Calculate freelancer taxes and contributions.
        
        Parameters:
        - annual_revenue: Annual revenue (total income)
        - annual_expenses: Annual expenses (actual costs) - optional if using flat rate
        - use_flat_expenses: Whether to use flat expense rate (60%) instead of actual expenses
        - include_sickness: Whether to pay voluntary sickness insurance (default True)
        - months_active: Number of months active in the year (default 12)
        
        Returns:
        Dictionary with tax and contribution calculations
        """
        annual_revenue = Decimal(str(annual_revenue))
        use_flat_expenses = bool(use_flat_expenses)
        include_sickness = bool(include_sickness)
        months_active = int(months_active)
        
        # Validate inputs
        if annual_revenue < 0:
            raise ValueError("Ročný príjem nesmie byť záporný")
        
        if months_active < 1 or months_active > 12:
            raise ValueError("Počet aktívnych mesiacov musí byť 1-12")
        
        # Calculate expenses
        if use_flat_expenses:
            # Use 60% flat expense rate
            annual_expenses = annual_revenue * self.FLAT_EXPENSE_RATE
            expenses_note = "Paušálne výdavky (60%)"
        else:
            annual_expenses = Decimal(str(annual_expenses))
            expenses_note = "Skutočné výdavky"
            
            if annual_expenses < 0:
                raise ValueError("Výdavky nesmú byť záporné")
        
        # Tax base (income - expenses)
        tax_base = annual_revenue - annual_expenses
        if tax_base < 0:
            tax_base = Decimal('0')
        
        # Apply non-taxable amount
        taxable_income = tax_base - self.NON_TAXABLE_AMOUNT_ANNUAL
        if taxable_income < 0:
            taxable_income = Decimal('0')
        
        # Calculate income tax (progressive)
        if taxable_income <= self.TAX_THRESHOLD:
            income_tax = taxable_income * self.TAX_RATE_LOW
            tax_rate_applied = self.TAX_RATE_LOW
        else:
            # Split into two brackets
            tax_low_bracket = self.TAX_THRESHOLD * self.TAX_RATE_LOW
            tax_high_bracket = (taxable_income - self.TAX_THRESHOLD) * self.TAX_RATE_HIGH
            income_tax = tax_low_bracket + tax_high_bracket
            tax_rate_applied = self.TAX_RATE_HIGH
        
        # Calculate assessment base for contributions (half-year delay rule simplified)
        # In reality, it's based on previous year's income, but we'll use current year for simplicity
        monthly_assessment_base = tax_base / Decimal('12')
        
        # Health insurance
        health_base_monthly = max(monthly_assessment_base, self.MIN_HEALTH_BASE_MONTHLY)
        health_insurance_monthly = health_base_monthly * self.HEALTH_INSURANCE_RATE
        health_insurance_annual = health_insurance_monthly * Decimal(str(months_active))
        
        # Social insurance
        social_base_monthly = max(monthly_assessment_base, self.MIN_SOCIAL_BASE_MONTHLY)
        
        # Calculate individual social contributions
        sickness_monthly = social_base_monthly * self.SOCIAL_SICKNESS_RATE if include_sickness else Decimal('0')
        pension_monthly = social_base_monthly * self.SOCIAL_PENSION_RATE
        disability_monthly = social_base_monthly * self.SOCIAL_DISABILITY_RATE
        accident_monthly = social_base_monthly * self.SOCIAL_ACCIDENT_RATE
        guarantee_monthly = social_base_monthly * self.SOCIAL_GUARANTEE_RATE
        reserve_monthly = social_base_monthly * self.SOCIAL_RESERVE_RATE
        
        social_total_monthly = (sickness_monthly + pension_monthly + disability_monthly + 
                               accident_monthly + guarantee_monthly + reserve_monthly)
        social_total_annual = social_total_monthly * Decimal(str(months_active))
        
        # Total contributions
        total_contributions = health_insurance_annual + social_total_annual
        
        # Total taxes and contributions
        total_tax_and_contributions = income_tax + total_contributions
        
        # Net income
        net_income = annual_revenue - annual_expenses - total_tax_and_contributions
        
        # Monthly averages
        monthly_revenue = annual_revenue / Decimal('12')
        monthly_net = net_income / Decimal('12')
        monthly_total_deductions = total_tax_and_contributions / Decimal('12')
        
        # Effective tax rate
        effective_rate = (total_tax_and_contributions / annual_revenue * Decimal('100')) if annual_revenue > 0 else Decimal('0')
        
        return {
            'income': {
                'annual_revenue': self.round_decimal(annual_revenue),
                'annual_expenses': self.round_decimal(annual_expenses),
                'expenses_note': expenses_note,
                'tax_base': self.round_decimal(tax_base),
                'non_taxable_amount': self.round_decimal(self.NON_TAXABLE_AMOUNT_ANNUAL),
                'taxable_income': self.round_decimal(taxable_income)
            },
            'tax': {
                'income_tax': self.round_decimal(income_tax),
                'tax_rate_applied': float(tax_rate_applied * 100),
                'monthly_average': self.round_decimal(income_tax / Decimal('12'))
            },
            'health_insurance': {
                'monthly_base': self.round_decimal(health_base_monthly),
                'monthly_payment': self.round_decimal(health_insurance_monthly),
                'annual_payment': self.round_decimal(health_insurance_annual),
                'rate': float(self.HEALTH_INSURANCE_RATE * 100),
                'min_base': self.round_decimal(self.MIN_HEALTH_BASE_MONTHLY)
            },
            'social_insurance': {
                'monthly_base': self.round_decimal(social_base_monthly),
                'monthly_payment': self.round_decimal(social_total_monthly),
                'annual_payment': self.round_decimal(social_total_annual),
                'breakdown': {
                    'sickness': {
                        'monthly': self.round_decimal(sickness_monthly),
                        'annual': self.round_decimal(sickness_monthly * Decimal(str(months_active))),
                        'rate': float(self.SOCIAL_SICKNESS_RATE * 100),
                        'included': include_sickness
                    },
                    'pension': {
                        'monthly': self.round_decimal(pension_monthly),
                        'annual': self.round_decimal(pension_monthly * Decimal(str(months_active))),
                        'rate': float(self.SOCIAL_PENSION_RATE * 100)
                    },
                    'disability': {
                        'monthly': self.round_decimal(disability_monthly),
                        'annual': self.round_decimal(disability_monthly * Decimal(str(months_active))),
                        'rate': float(self.SOCIAL_DISABILITY_RATE * 100)
                    },
                    'accident': {
                        'monthly': self.round_decimal(accident_monthly),
                        'annual': self.round_decimal(accident_monthly * Decimal(str(months_active))),
                        'rate': float(self.SOCIAL_ACCIDENT_RATE * 100)
                    },
                    'guarantee': {
                        'monthly': self.round_decimal(guarantee_monthly),
                        'annual': self.round_decimal(guarantee_monthly * Decimal(str(months_active))),
                        'rate': float(self.SOCIAL_GUARANTEE_RATE * 100)
                    },
                    'reserve': {
                        'monthly': self.round_decimal(reserve_monthly),
                        'annual': self.round_decimal(reserve_monthly * Decimal(str(months_active))),
                        'rate': float(self.SOCIAL_RESERVE_RATE * 100)
                    }
                }
            },
            'summary': {
                'total_contributions': self.round_decimal(total_contributions),
                'total_tax_and_contributions': self.round_decimal(total_tax_and_contributions),
                'net_income': self.round_decimal(net_income),
                'effective_rate': self.round_decimal(effective_rate, 2),
                'monthly_revenue': self.round_decimal(monthly_revenue),
                'monthly_deductions': self.round_decimal(monthly_total_deductions),
                'monthly_net': self.round_decimal(monthly_net),
                'months_active': months_active
            }
        }
    
    def get_metadata(self) -> Dict[str, Any]:
        """Return metadata about the freelancer tax calculator."""
        return {
            'name': 'Freelancer Tax Calculator',
            'description': 'Calculate taxes and contributions for self-employed persons in Slovakia',
            'version': '1.0.0',
            'parameters': {
                'required': ['annual_revenue'],
                'optional': ['annual_expenses', 'use_flat_expenses', 'include_sickness', 'months_active'],
                'annual_revenue': {
                    'type': 'decimal',
                    'description': 'Annual revenue (total income)',
                    'min': 0
                },
                'annual_expenses': {
                    'type': 'decimal',
                    'description': 'Annual expenses (actual costs)',
                    'min': 0,
                    'default': 0
                },
                'use_flat_expenses': {
                    'type': 'boolean',
                    'description': 'Use 60% flat expense rate',
                    'default': True
                },
                'include_sickness': {
                    'type': 'boolean',
                    'description': 'Include voluntary sickness insurance',
                    'default': True
                },
                'months_active': {
                    'type': 'integer',
                    'description': 'Number of active months in the year',
                    'min': 1,
                    'max': 12,
                    'default': 12
                }
            },
            'example_request': {
                'annual_revenue': 30000,
                'use_flat_expenses': True,
                'include_sickness': True,
                'months_active': 12
            }
        }
