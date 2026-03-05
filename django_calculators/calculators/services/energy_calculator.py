"""
Energy Cost Calculator Service
Calculates electricity and gas costs for Slovak households.
"""
from decimal import Decimal
from typing import Dict, Any
from .base_calculator import BaseCalculator
from . import config_variables as cfg


class EnergyCalculator(BaseCalculator):
    """
    Calculates energy costs (electricity and gas) for Slovak households.
    
    Includes:
    - Electricity consumption and costs
    - Gas consumption and costs
    - Monthly and annual projections
    - Comparison with average consumption
    - Cost breakdowns
    """
    
    # Slovak electricity rates (2026 estimates) - imported from config_variables
    ELECTRICITY_RATE_LOW = cfg.ELECTRICITY_RATE_LOW  # EUR/kWh (low tariff)
    ELECTRICITY_RATE_HIGH = cfg.ELECTRICITY_RATE_HIGH  # EUR/kWh (high tariff)
    ELECTRICITY_FIXED_MONTHLY = cfg.ELECTRICITY_FIXED_MONTHLY  # EUR/month
    
    # Slovak gas rates (2026 estimates) - imported from config_variables
    GAS_RATE = cfg.GAS_RATE  # EUR/kWh
    GAS_FIXED_MONTHLY = cfg.GAS_FIXED_MONTHLY  # EUR/month
    
    # Average consumption (Slovakia) - imported from config_variables
    AVG_ELECTRICITY_MONTHLY = cfg.AVG_ELECTRICITY_MONTHLY  # kWh/month for household
    AVG_GAS_MONTHLY = cfg.AVG_GAS_MONTHLY  # kWh/month for household
    
    def calculate(
        self,
        electricity_consumption: float,
        gas_consumption: float = 0,
        electricity_rate: float = None,
        gas_rate: float = None,
        has_dual_tariff: bool = False,
        high_tariff_percentage: float = 40,
        household_size: int = 2,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Calculate energy costs.
        
        Parameters:
        - electricity_consumption: Monthly electricity consumption in kWh
        - gas_consumption: Monthly gas consumption in kWh (0 if no gas)
        - electricity_rate: Custom electricity rate (EUR/kWh, optional)
        - gas_rate: Custom gas rate (EUR/kWh, optional)
        - has_dual_tariff: Whether using dual electricity tariff (default False)
        - high_tariff_percentage: % of consumption during high tariff if dual (default 40)
        - household_size: Number of people in household (for comparison)
        
        Returns:
        Dictionary with energy cost calculations
        """
        electricity_consumption = Decimal(str(electricity_consumption))
        gas_consumption = Decimal(str(gas_consumption))
        
        # Custom rates or defaults
        electricity_rate = Decimal(str(electricity_rate if electricity_rate is not None else self.ELECTRICITY_RATE_HIGH))
        gas_rate = Decimal(str(gas_rate if gas_rate is not None else self.GAS_RATE))
        
        high_tariff_percentage = Decimal(str(high_tariff_percentage))
        household_size = int(household_size)
        
        # Validate inputs
        if electricity_consumption < 0:
            raise ValueError("Spotreba elektriny nesmie byť záporná")
        
        if gas_consumption < 0:
            raise ValueError("Spotreba plynu nesmie byť záporná")
        
        if household_size < 1:
            raise ValueError("Veľkosť domácnosti musí byť aspoň 1")
        
        # Calculate electricity costs
        if has_dual_tariff:
            # Dual tariff: split consumption between low and high tariff
            high_tariff_kwh = electricity_consumption * (high_tariff_percentage / Decimal('100'))
            low_tariff_kwh = electricity_consumption - high_tariff_kwh
            
            electricity_variable_cost = (
                (low_tariff_kwh * self.ELECTRICITY_RATE_LOW) +
                (high_tariff_kwh * self.ELECTRICITY_RATE_HIGH)
            )
        else:
            # Single tariff
            electricity_variable_cost = electricity_consumption * electricity_rate
            high_tariff_kwh = Decimal('0')
            low_tariff_kwh = electricity_consumption
        
        electricity_fixed_cost = self.ELECTRICITY_FIXED_MONTHLY
        electricity_total_monthly = electricity_variable_cost + electricity_fixed_cost
        electricity_total_annual = electricity_total_monthly * Decimal('12')
        
        # Calculate gas costs
        if gas_consumption > 0:
            gas_variable_cost = gas_consumption * gas_rate
            gas_fixed_cost = self.GAS_FIXED_MONTHLY
            gas_total_monthly = gas_variable_cost + gas_fixed_cost
            gas_total_annual = gas_total_monthly * Decimal('12')
        else:
            gas_variable_cost = Decimal('0')
            gas_fixed_cost = Decimal('0')
            gas_total_monthly = Decimal('0')
            gas_total_annual = Decimal('0')
        
        # Total energy costs
        total_monthly = electricity_total_monthly + gas_total_monthly
        total_annual = total_monthly * Decimal('12')
        
        # Per person costs
        cost_per_person_monthly = total_monthly / Decimal(str(household_size))
        cost_per_person_annual = total_annual / Decimal(str(household_size))
        
        # Comparison with average
        avg_electricity_cost = self.AVG_ELECTRICITY_MONTHLY * electricity_rate + electricity_fixed_cost
        electricity_vs_average = ((electricity_total_monthly - avg_electricity_cost) / avg_electricity_cost * Decimal('100')
                                 if avg_electricity_cost > 0 else Decimal('0'))
        
        if gas_consumption > 0:
            avg_gas_cost = self.AVG_GAS_MONTHLY * gas_rate + gas_fixed_cost
            gas_vs_average = ((gas_total_monthly - avg_gas_cost) / avg_gas_cost * Decimal('100')
                            if avg_gas_cost > 0 else Decimal('0'))
        else:
            avg_gas_cost = Decimal('0')
            gas_vs_average = Decimal('0')
        
        # Energy distribution
        if total_monthly > 0:
            electricity_percentage = (electricity_total_monthly / total_monthly * Decimal('100'))
            gas_percentage = (gas_total_monthly / total_monthly * Decimal('100'))
        else:
            electricity_percentage = Decimal('0')
            gas_percentage = Decimal('0')
        
        # Efficiency category
        electricity_per_person = electricity_consumption / Decimal(str(household_size))
        if electricity_per_person < 100:
            efficiency_category = "Veľmi úsporná"
        elif electricity_per_person < 150:
            efficiency_category = "Úsporná"
        elif electricity_per_person < 200:
            efficiency_category = "Priemerná"
        else:
            efficiency_category = "Vysoká spotreba"
        
        return {
            'electricity': {
                'consumption_kwh': self.round_decimal(electricity_consumption),
                'rate': self.round_decimal(electricity_rate, 4),
                'has_dual_tariff': has_dual_tariff,
                'high_tariff_kwh': self.round_decimal(high_tariff_kwh) if has_dual_tariff else None,
                'low_tariff_kwh': self.round_decimal(low_tariff_kwh) if has_dual_tariff else None,
                'variable_cost': self.round_decimal(electricity_variable_cost),
                'fixed_cost': self.round_decimal(electricity_fixed_cost),
                'total_monthly': self.round_decimal(electricity_total_monthly),
                'total_annual': self.round_decimal(electricity_total_annual),
                'vs_average_percentage': self.round_decimal(electricity_vs_average, 1)
            },
            'gas': {
                'consumption_kwh': self.round_decimal(gas_consumption),
                'rate': self.round_decimal(gas_rate, 4),
                'variable_cost': self.round_decimal(gas_variable_cost),
                'fixed_cost': self.round_decimal(gas_fixed_cost),
                'total_monthly': self.round_decimal(gas_total_monthly),
                'total_annual': self.round_decimal(gas_total_annual),
                'vs_average_percentage': self.round_decimal(gas_vs_average, 1) if gas_consumption > 0 else None
            },
            'total': {
                'monthly_cost': self.round_decimal(total_monthly),
                'annual_cost': self.round_decimal(total_annual),
                'electricity_percentage': self.round_decimal(electricity_percentage, 1),
                'gas_percentage': self.round_decimal(gas_percentage, 1)
            },
            'household': {
                'household_size': household_size,
                'cost_per_person_monthly': self.round_decimal(cost_per_person_monthly),
                'cost_per_person_annual': self.round_decimal(cost_per_person_annual),
                'electricity_per_person': self.round_decimal(electricity_per_person),
                'efficiency_category': efficiency_category
            },
            'averages': {
                'avg_electricity_monthly_kwh': self.round_decimal(self.AVG_ELECTRICITY_MONTHLY),
                'avg_gas_monthly_kwh': self.round_decimal(self.AVG_GAS_MONTHLY),
                'avg_electricity_cost': self.round_decimal(avg_electricity_cost),
                'avg_gas_cost': self.round_decimal(avg_gas_cost) if gas_consumption > 0 else None
            }
        }
    
    def get_metadata(self) -> Dict[str, Any]:
        """Return metadata about the energy calculator."""
        return {
            'name': 'Energy Cost Calculator',
            'description': 'Calculate electricity and gas costs for Slovak households',
            'version': '1.0.0',
            'parameters': {
                'required': ['electricity_consumption'],
                'optional': ['gas_consumption', 'electricity_rate', 'gas_rate', 'has_dual_tariff', 
                           'high_tariff_percentage', 'household_size'],
                'electricity_consumption': {
                    'type': 'decimal',
                    'description': 'Monthly electricity consumption in kWh',
                    'min': 0
                },
                'gas_consumption': {
                    'type': 'decimal',
                    'description': 'Monthly gas consumption in kWh',
                    'default': 0,
                    'min': 0
                },
                'electricity_rate': {
                    'type': 'decimal',
                    'description': 'Electricity rate in EUR/kWh',
                    'default': 0.20
                },
                'gas_rate': {
                    'type': 'decimal',
                    'description': 'Gas rate in EUR/kWh',
                    'default': 0.06
                },
                'has_dual_tariff': {
                    'type': 'boolean',
                    'description': 'Whether using dual electricity tariff',
                    'default': False
                },
                'high_tariff_percentage': {
                    'type': 'decimal',
                    'description': 'Percentage of consumption during high tariff',
                    'default': 40
                },
                'household_size': {
                    'type': 'integer',
                    'description': 'Number of people in household',
                    'default': 2,
                    'min': 1
                }
            },
            'example_request': {
                'electricity_consumption': 300,
                'gas_consumption': 600,
                'household_size': 3,
                'has_dual_tariff': True
            }
        }
