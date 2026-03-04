"""
Calculator Services Package

This package contains all calculator implementations.
Each calculator is a separate module with its own business logic.
"""

from .base_calculator import BaseCalculator
from .salary_calculator import SalaryCalculator
from .mortgage_calculator import MortgageCalculator
from .vat_calculator import VATCalculator

__all__ = [
    'BaseCalculator',
    'SalaryCalculator',
    'MortgageCalculator',
    'VATCalculator',
]
