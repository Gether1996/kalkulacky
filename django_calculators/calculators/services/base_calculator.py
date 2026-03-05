"""
Base Calculator Abstract Class

All calculators inherit from this base class to ensure consistent interface.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
from decimal import Decimal


class BaseCalculator(ABC):
    """
    Abstract base class for all calculators.
    
    Every calculator must implement the calculate() method.
    """
    
    def __init__(self):
        self.result = None
        self.breakdown = {}
    
    @abstractmethod
    def calculate(self, **kwargs) -> Dict[str, Any]:
        """
        Main calculation method.
        
        Args:
            **kwargs: Calculator-specific input parameters
            
        Returns:
            Dict containing calculation results and breakdown
        """
        pass
    
    def validate_inputs(self, **kwargs) -> bool:
        """
        Validate input parameters before calculation.
        Override in child classes for custom validation.
        
        Returns:
            True if inputs are valid
            
        Raises:
            ValueError: If validation fails
        """
        return True
    
    def format_currency(self, amount: float) -> str:
        """Format amount as Euro currency"""
        return f"€{amount:,.2f}"
    
    def to_decimal(self, value: Any) -> Decimal:
        """Convert value to Decimal for precise calculations"""
        return Decimal(str(value))
    
    def round_decimal(self, value: Decimal, places: int = 2) -> Decimal:
        """Round Decimal to specified decimal places"""
        return round(value, places)
    
    def round_money(self, amount: Decimal, places: int = 2) -> float:
        """Round money to specified decimal places"""
        return float(round(amount, places))
