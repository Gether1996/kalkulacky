"""
Mortgage Calculator - Kalkulačka hypotéky

Calculates monthly mortgage payments, total interest, and amortization schedule.

Search Volume: 8,000+/month
Keywords: "kalkulačka hypotéky", "hypotéka výpočet", "splátka hypotéky"
"""

from decimal import Decimal
from typing import Dict, Any, List
from .base_calculator import BaseCalculator


class MortgageCalculator(BaseCalculator):
    """
    Mortgage Payment Calculator
    
    Calculates:
    - Monthly payment (principal + interest)
    - Total interest paid over loan term
    - Amortization schedule (year-by-year breakdown)
    - Total amount paid
    """
    
    def validate_inputs(self, **kwargs) -> bool:
        """Validate mortgage calculator inputs"""
        loan_amount = kwargs.get('loan_amount')
        annual_interest_rate = kwargs.get('annual_interest_rate')
        loan_term_years = kwargs.get('loan_term_years')
        
        # Validate loan amount
        if not loan_amount:
            raise ValueError("loan_amount is required")
        try:
            amount = self.to_decimal(loan_amount)
        except (ValueError, TypeError):
            raise ValueError("loan_amount must be a valid number")
        if amount <= 0:
            raise ValueError("loan_amount must be greater than 0")
        if amount > 1000000:
            raise ValueError("loan_amount seems unrealistically high (>€1,000,000)")
        
        # Validate interest rate
        if not annual_interest_rate:
            raise ValueError("annual_interest_rate is required")
        try:
            rate = self.to_decimal(annual_interest_rate)
        except (ValueError, TypeError):
            raise ValueError("annual_interest_rate must be a valid number")
        if rate < 0:
            raise ValueError("annual_interest_rate cannot be negative")
        if rate > 20:
            raise ValueError("annual_interest_rate seems unrealistically high (>20%)")
        
        # Validate loan term
        if not loan_term_years:
            raise ValueError("loan_term_years is required")
        try:
            years = int(loan_term_years)
        except (ValueError, TypeError):
            raise ValueError("loan_term_years must be a valid integer")
        if years <= 0:
            raise ValueError("loan_term_years must be greater than 0")
        if years > 40:
            raise ValueError("loan_term_years seems unrealistically long (>40 years)")
        
        return True
    
    def calculate(
        self, 
        loan_amount: float, 
        annual_interest_rate: float, 
        loan_term_years: int,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Calculate mortgage payment and amortization schedule.
        
        Args:
            loan_amount: Total loan amount in EUR
            annual_interest_rate: Annual interest rate (e.g., 3.5 for 3.5%)
            loan_term_years: Loan term in years
            
        Returns:
            Dict with:
                - monthly_payment: Monthly payment amount
                - total_paid: Total amount paid over loan term
                - total_interest: Total interest paid
                - loan_amount: Original loan amount
                - amortization_schedule: Year-by-year breakdown
        """
        # Validate inputs
        self.validate_inputs(
            loan_amount=loan_amount,
            annual_interest_rate=annual_interest_rate,
            loan_term_years=loan_term_years
        )
        
        # Convert to Decimal for precise calculations
        principal = self.to_decimal(loan_amount)
        annual_rate = self.to_decimal(annual_interest_rate)
        years = int(loan_term_years)
        
        # Calculate monthly interest rate and number of payments
        monthly_rate = annual_rate / Decimal('100') / Decimal('12')
        num_payments = years * 12
        
        # Calculate monthly payment using mortgage formula:
        # M = P * [r(1+r)^n] / [(1+r)^n - 1]
        # Where: M = monthly payment, P = principal, r = monthly rate, n = number of payments
        
        if monthly_rate == 0:
            # Special case: 0% interest
            monthly_payment = principal / num_payments
        else:
            # Standard calculation
            numerator = monthly_rate * ((1 + monthly_rate) ** num_payments)
            denominator = ((1 + monthly_rate) ** num_payments) - 1
            monthly_payment = principal * (numerator / denominator)
        
        # Calculate totals
        total_paid = monthly_payment * num_payments
        total_interest = total_paid - principal
        
        # Generate amortization schedule (yearly breakdown)
        amortization_schedule = self._generate_amortization_schedule(
            principal=principal,
            monthly_payment=monthly_payment,
            monthly_rate=monthly_rate,
            num_payments=num_payments
        )
        
        # Prepare result
        result = {
            'loan_amount': self.round_money(principal),
            'annual_interest_rate': float(annual_rate),
            'loan_term_years': years,
            'monthly_payment': self.round_money(monthly_payment),
            'total_paid': self.round_money(total_paid),
            'total_interest': self.round_money(total_interest),
            'total_principal': self.round_money(principal),
            
            # First year details
            'first_year': {
                'total_payment': self.round_money(monthly_payment * 12),
                'principal': self.round_money(amortization_schedule[0]['principal_paid']),
                'interest': self.round_money(amortization_schedule[0]['interest_paid']),
                'remaining_balance': self.round_money(amortization_schedule[0]['remaining_balance']),
            },
            
            # Amortization schedule (year by year)
            'amortization_schedule': amortization_schedule,
            
            # Breakdown
            'breakdown': {
                'monthly_payment': self.round_money(monthly_payment),
                'number_of_payments': num_payments,
                'total_paid': self.round_money(total_paid),
                'loan_amount': self.round_money(principal),
                'total_interest': self.round_money(total_interest),
                'interest_percentage': self.round_money((total_interest / principal) * 100),
            }
        }
        
        self.result = result
        return result
    
    def _generate_amortization_schedule(
        self,
        principal: Decimal,
        monthly_payment: Decimal,
        monthly_rate: Decimal,
        num_payments: int
    ) -> List[Dict[str, float]]:
        """
        Generate year-by-year amortization schedule.
        
        Returns:
            List of dicts with yearly breakdown
        """
        schedule = []
        remaining_balance = principal
        
        for year in range(1, (num_payments // 12) + 1):
            year_principal = Decimal('0')
            year_interest = Decimal('0')
            
            # Calculate 12 monthly payments for this year
            for month in range(12):
                payment_number = (year - 1) * 12 + month + 1
                
                if payment_number > num_payments:
                    break
                
                # Calculate interest for this month
                interest_payment = remaining_balance * monthly_rate
                
                # Calculate principal for this month
                principal_payment = monthly_payment - interest_payment
                
                # Update totals
                year_interest += interest_payment
                year_principal += principal_payment
                remaining_balance -= principal_payment
                
                # Handle last payment (might be slightly different due to rounding)
                if payment_number == num_payments:
                    principal_payment += remaining_balance
                    year_principal += remaining_balance
                    remaining_balance = Decimal('0')
            
            schedule.append({
                'year': year,
                'principal_paid': self.round_money(year_principal),
                'interest_paid': self.round_money(year_interest),
                'total_paid': self.round_money(year_principal + year_interest),
                'remaining_balance': self.round_money(max(Decimal('0'), remaining_balance)),
            })
        
        return schedule


# Example usage and testing
if __name__ == '__main__':
    calc = MortgageCalculator()
    
    # Test with common mortgage scenarios
    print("Slovak Mortgage Calculator 2026\n")
    
    # Example: €150,000 loan, 3.5% interest, 25 years
    result = calc.calculate(
        loan_amount=150000,
        annual_interest_rate=3.5,
        loan_term_years=25
    )
    
    print(f"Loan Amount: €{result['loan_amount']:,.2f}")
    print(f"Interest Rate: {result['annual_interest_rate']}%")
    print(f"Loan Term: {result['loan_term_years']} years")
    print(f"\nMonthly Payment: €{result['monthly_payment']:,.2f}")
    print(f"Total Paid: €{result['total_paid']:,.2f}")
    print(f"Total Interest: €{result['total_interest']:,.2f}")
    print(f"\nFirst Year:")
    print(f"  Total Payment: €{result['first_year']['total_payment']:,.2f}")
    print(f"  Principal: €{result['first_year']['principal']:,.2f}")
    print(f"  Interest: €{result['first_year']['interest']:,.2f}")
    print(f"  Remaining: €{result['first_year']['remaining_balance']:,.2f}")
