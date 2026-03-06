"""
Loan Calculator - Kalkulačka úveru

Calculates loan payments, total interest, and amortization schedule.

Search Volume: 6,000+/month
Keywords: "kalkulačka úveru", "splátka úveru", "úver výpočet"
"""

from decimal import Decimal
from typing import Dict, Any, List
from .base_calculator import BaseCalculator


class LoanCalculator(BaseCalculator):
    """
    Loan Calculator
    
    Calculates:
    - Monthly payment amount
    - Total interest paid
    - Total amount paid
    - Amortization schedule (optional)
    """
    
    def validate_inputs(self, **kwargs) -> bool:
        """Validate loan calculator inputs"""
        loan_amount = kwargs.get('loan_amount')
        interest_rate = kwargs.get('interest_rate')
        loan_years = kwargs.get('loan_years')
        
        if not all([loan_amount, interest_rate is not None, loan_years]):
            raise ValueError("Výška pôžičky, úroková sadzba a doba splatnosti sú povinné")
        
        try:
            amount = self.to_decimal(loan_amount)
            rate = self.to_decimal(interest_rate)
            years = self.to_decimal(loan_years)
        except (ValueError, TypeError):
            raise ValueError("Všetky vstupy musia byť platné čísla")
        
        if amount <= 0:
            raise ValueError("Výška pôžičky musí byť väčšia ako 0")
        
        if amount > 1000000:
            raise ValueError("Výška pôžičky sa zdá byť nereálne vysoká (>1 000 000 €)")
        
        if rate < 0 or rate > 30:
            raise ValueError("Úroková sadzba musí byť medzi 0 a 30")
        
        if years <= 0 or years > 50:
            raise ValueError("Doba splatnosti musí byť medzi 1 a 50 rokmi")
        
        return True
    
    def calculate(
        self, 
        loan_amount: float, 
        interest_rate: float, 
        loan_years: int,
        include_schedule: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Calculate loan payments and details.
        
        Args:
            loan_amount: Principal loan amount (€)
            interest_rate: Annual interest rate (%)
            loan_years: Loan term in years
            include_schedule: Whether to include full amortization schedule
            
        Returns:
            Dictionary with calculation results
        """
        # Validate inputs
        self.validate_inputs(
            loan_amount=loan_amount,
            interest_rate=interest_rate,
            loan_years=loan_years
        )
        
        # Convert to Decimal for precision
        principal = self.to_decimal(loan_amount)
        annual_rate = self.to_decimal(interest_rate)
        years = int(loan_years)
        
        # Calculate monthly values
        months = years * 12
        monthly_rate = annual_rate / Decimal('100') / Decimal('12')
        
        # Calculate monthly payment using amortization formula
        # M = P * [r(1+r)^n] / [(1+r)^n - 1]
        if monthly_rate == 0:
            # No interest case
            monthly_payment = principal / Decimal(months)
            total_interest = Decimal('0')
        else:
            monthly_payment = principal * (
                monthly_rate * (1 + monthly_rate) ** months
            ) / (
                ((1 + monthly_rate) ** months) - 1
            )
            total_interest = (monthly_payment * Decimal(months)) - principal
        
        total_paid = principal + total_interest
        
        # Build result
        result = {
            'monthly_payment': float(monthly_payment),
            'total_interest': float(total_interest),
            'total_paid': float(total_paid),
            'principal': float(principal),
            'annual_interest_rate': float(annual_rate),
            'loan_years': years,
            'total_months': months,
            'monthly_interest_rate': float(monthly_rate * 100),
        }
        
        # Generate amortization schedule if requested
        if include_schedule:
            schedule = self._generate_amortization_schedule(
                principal, monthly_payment, monthly_rate, months
            )
            result['amortization_schedule'] = schedule
            result['schedule_summary'] = {
                'first_year_interest': sum(
                    month['interest_payment'] 
                    for month in schedule[:12]
                ),
                'first_year_principal': sum(
                    month['principal_payment'] 
                    for month in schedule[:12]
                ),
            }
        
        self.result = result
        return result
    
    def _generate_amortization_schedule(
        self, 
        principal: Decimal, 
        monthly_payment: Decimal,
        monthly_rate: Decimal,
        total_months: int
    ) -> List[Dict[str, Any]]:
        """
        Generate month-by-month amortization schedule.
        
        Returns:
            List of monthly payment breakdowns
        """
        schedule = []
        remaining_balance = principal
        
        for month in range(1, total_months + 1):
            # Calculate interest for this month
            interest_payment = remaining_balance * monthly_rate
            
            # Principal payment is the difference
            principal_payment = monthly_payment - interest_payment
            
            # Update remaining balance
            remaining_balance -= principal_payment
            
            # Avoid negative balance due to rounding
            if remaining_balance < 0:
                principal_payment += remaining_balance
                remaining_balance = Decimal('0')
            
            schedule.append({
                'month': month,
                'payment': float(monthly_payment),
                'principal_payment': float(principal_payment),
                'interest_payment': float(interest_payment),
                'remaining_balance': float(remaining_balance),
            })
        
        return schedule
    
    @staticmethod
    def to_decimal(value) -> Decimal:
        """Convert value to Decimal for precise calculations"""
        if isinstance(value, Decimal):
            return value
        return Decimal(str(value))
