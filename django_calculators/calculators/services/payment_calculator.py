"""
Payment Calculator Service
Calculates loan installment payments and amortization schedules.
"""
from decimal import Decimal
from typing import Dict, Any, List
from .base_calculator import BaseCalculator


class PaymentCalculator(BaseCalculator):
    """
    Calculates loan payment amounts and amortization schedules.
    
    Includes:
    - Monthly payment calculation
    - Total cost and interest breakdown
    - Amortization schedule
    - Payment frequency options (monthly, quarterly, yearly)
    """
    
    # Payment frequency multipliers (payments per year)
    PAYMENT_FREQUENCIES = {
        'monthly': 12,
        'quarterly': 4,
        'yearly': 1
    }
    
    def calculate(
        self,
        loan_amount: float,
        annual_interest_rate: float,
        loan_term_years: float,
        payment_frequency: str = 'monthly',
        include_schedule: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Calculate loan payments.
        
        Parameters:
        - loan_amount: Principal loan amount
        - annual_interest_rate: Annual interest rate in percentage (e.g., 5.5 for 5.5%)
        - loan_term_years: Loan term in years
        - payment_frequency: Payment frequency ('monthly', 'quarterly', 'yearly')
        - include_schedule: Whether to include amortization schedule (default False)
        
        Returns:
        Dictionary with payment calculations and optional amortization schedule
        """
        loan_amount = Decimal(str(loan_amount))
        annual_interest_rate = Decimal(str(annual_interest_rate))
        loan_term_years = Decimal(str(loan_term_years))
        payment_frequency = str(payment_frequency)
        include_schedule = bool(include_schedule)
        
        # Validate inputs
        if loan_amount <= 0:
            raise ValueError("Výška úveru musí byť väčšia ako 0")
        
        if annual_interest_rate < 0:
            raise ValueError("Úroková sadzba nesmie byť záporná")
        
        if loan_term_years <= 0:
            raise ValueError("Doba splácania musí byť väčšia ako 0")
        
        if payment_frequency not in self.PAYMENT_FREQUENCIES:
            raise ValueError(f"Neplatná frekvencia splátok. Použite: {', '.join(self.PAYMENT_FREQUENCIES.keys())}")
        
        # Calculate payment frequency details
        payments_per_year = Decimal(str(self.PAYMENT_FREQUENCIES[payment_frequency]))
        total_payments = loan_term_years * payments_per_year
        
        # Convert annual rate to period rate
        period_interest_rate = (annual_interest_rate / Decimal('100')) / payments_per_year
        
        # Calculate payment amount using loan payment formula
        # Payment = P * [r(1+r)^n] / [(1+r)^n - 1]
        # Where P = principal, r = period rate, n = number of payments
        
        if period_interest_rate > 0:
            # Standard formula with interest
            numerator = period_interest_rate * ((Decimal('1') + period_interest_rate) ** total_payments)
            denominator = ((Decimal('1') + period_interest_rate) ** total_payments) - Decimal('1')
            payment_amount = loan_amount * (numerator / denominator)
        else:
            # No interest - simple division
            payment_amount = loan_amount / total_payments
        
        # Calculate totals
        total_paid = payment_amount * total_payments
        total_interest = total_paid - loan_amount
        interest_percentage = (total_interest / loan_amount * Decimal('100')) if loan_amount > 0 else Decimal('0')
        
        # Calculate yearly totals
        payments_per_year_count = int(payments_per_year)
        yearly_payment_amount = payment_amount * payments_per_year
        
        # Payment frequency labels
        frequency_labels = {
            'monthly': 'Mesačne',
            'quarterly': 'Štvrťročne',
            'yearly': 'Ročne'
        }
        
        result = {
            'payment': {
                'amount': self.round_decimal(payment_amount),
                'frequency': payment_frequency,
                'frequency_label': frequency_labels[payment_frequency],
                'payments_per_year': int(payments_per_year),
                'total_payments': int(total_payments),
                'yearly_amount': self.round_decimal(yearly_payment_amount)
            },
            'loan': {
                'principal': self.round_decimal(loan_amount),
                'interest_rate': self.round_decimal(annual_interest_rate, 2),
                'term_years': self.round_decimal(loan_term_years, 1),
                'period_interest_rate': self.round_decimal(period_interest_rate * Decimal('100'), 4)
            },
            'totals': {
                'total_paid': self.round_decimal(total_paid),
                'total_interest': self.round_decimal(total_interest),
                'interest_percentage': self.round_decimal(interest_percentage, 2),
                'principal_percentage': self.round_decimal(Decimal('100') - interest_percentage, 2)
            },
            'breakdown': {
                'first_payment': {
                    'payment': self.round_decimal(payment_amount),
                    # Month 1: interest = balance × rate; principal = payment − interest.
                    'principal': self.round_decimal(payment_amount - (loan_amount * period_interest_rate))
                                if period_interest_rate > 0 else self.round_decimal(payment_amount),
                    'interest': self.round_decimal(loan_amount * period_interest_rate) if period_interest_rate > 0
                               else Decimal('0')
                }
            }
        }
        
        # Generate amortization schedule if requested
        if include_schedule:
            schedule = self._generate_amortization_schedule(
                loan_amount,
                payment_amount,
                period_interest_rate,
                int(total_payments)
            )
            result['schedule'] = schedule
        
        return result
    
    def _generate_amortization_schedule(
        self,
        principal: Decimal,
        payment: Decimal,
        period_rate: Decimal,
        total_payments: int
    ) -> List[Dict[str, Any]]:
        """
        Generate amortization schedule showing payment breakdown over time.
        
        Returns list of payment details for each period.
        """
        schedule = []
        remaining_balance = principal
        
        for payment_number in range(1, total_payments + 1):
            # Calculate interest for this period
            interest_payment = remaining_balance * period_rate
            
            # Calculate principal payment
            principal_payment = payment - interest_payment
            
            # Ensure last payment doesn't create negative balance
            if payment_number == total_payments:
                principal_payment = remaining_balance
                payment = remaining_balance + interest_payment
            
            # Update remaining balance
            remaining_balance = remaining_balance - principal_payment
            
            # Add to schedule (limit to reasonable number of entries)
            if payment_number <= 360:  # Max 30 years monthly payments
                schedule.append({
                    'payment_number': payment_number,
                    'payment': self.round_decimal(payment),
                    'principal': self.round_decimal(principal_payment),
                    'interest': self.round_decimal(interest_payment),
                    'remaining_balance': self.round_decimal(remaining_balance)
                })
        
        return schedule
    
    def get_metadata(self) -> Dict[str, Any]:
        """Return metadata about the payment calculator."""
        return {
            'name': 'Payment Calculator',
            'description': 'Calculate loan installment payments and amortization schedules',
            'version': '1.0.0',
            'parameters': {
                'required': ['loan_amount', 'annual_interest_rate', 'loan_term_years'],
                'optional': ['payment_frequency', 'include_schedule'],
                'loan_amount': {
                    'type': 'decimal',
                    'description': 'Principal loan amount',
                    'min': 0
                },
                'annual_interest_rate': {
                    'type': 'decimal',
                    'description': 'Annual interest rate in percentage',
                    'min': 0
                },
                'loan_term_years': {
                    'type': 'decimal',
                    'description': 'Loan term in years',
                    'min': 0
                },
                'payment_frequency': {
                    'type': 'string',
                    'description': 'Payment frequency',
                    'choices': ['monthly', 'quarterly', 'yearly'],
                    'default': 'monthly'
                },
                'include_schedule': {
                    'type': 'boolean',
                    'description': 'Include amortization schedule',
                    'default': False
                }
            },
            'example_request': {
                'loan_amount': 50000,
                'annual_interest_rate': 5.5,
                'loan_term_years': 10,
                'payment_frequency': 'monthly',
                'include_schedule': False
            }
        }
