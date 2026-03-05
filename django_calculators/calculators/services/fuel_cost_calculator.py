"""
Fuel Cost Calculator - Kalkulačka spotreby auta

Calculates fuel cost based on distance, consumption, and fuel price.

Search Volume: 3,000+/month
Keywords: "spotreba auta kalkulačka", "náklady na palivo"
"""

from decimal import Decimal
from typing import Dict, Any
from .base_calculator import BaseCalculator


class FuelCostCalculator(BaseCalculator):
    """
    Fuel Cost Calculator
    
    Calculates:
    - Total fuel needed
    - Total fuel cost
    - Cost per kilometer
    """
    
    def validate_inputs(self, **kwargs) -> bool:
        """Validate fuel cost calculator inputs"""
        distance = kwargs.get('distance')
        consumption = kwargs.get('consumption')
        fuel_price = kwargs.get('fuel_price')
        
        if not all([distance, consumption, fuel_price]):
            raise ValueError("distance, consumption, and fuel_price are required")
        
        try:
            dist = self.to_decimal(distance)
            cons = self.to_decimal(consumption)
            price = self.to_decimal(fuel_price)
        except (ValueError, TypeError):
            raise ValueError("All inputs must be valid numbers")
        
        if dist <= 0:
            raise ValueError("distance must be greater than 0")
        
        if dist > 10000:
            raise ValueError("distance seems unrealistically high (>10,000 km)")
        
        if cons <= 0 or cons > 50:
            raise ValueError("consumption must be between 0 and 50 liters/100km")
        
        if price <= 0 or price > 10:
            raise ValueError("fuel_price must be between 0 and 10 EUR/liter")
        
        return True
    
    def calculate(
        self, 
        distance: float, 
        consumption: float, 
        fuel_price: float,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Calculate fuel cost.
        
        Args:
            distance: Distance to travel (km)
            consumption: Fuel consumption (liters per 100 km)
            fuel_price: Fuel price (EUR per liter)
            
        Returns:
            Dictionary with calculation results
        """
        # Validate inputs
        self.validate_inputs(
            distance=distance,
            consumption=consumption,
            fuel_price=fuel_price
        )
        
        # Convert to Decimal for precision
        dist = self.to_decimal(distance)
        cons = self.to_decimal(consumption)
        price = self.to_decimal(fuel_price)
        
        # Calculate fuel needed: (distance / 100) * consumption
        fuel_needed = (dist / Decimal('100')) * cons
        
        # Calculate total cost
        total_cost = fuel_needed * price
        
        # Calculate cost per km
        cost_per_km = total_cost / dist
        
        # Calculate cost for return trip
        return_trip_cost = total_cost * Decimal('2')
        return_trip_fuel = fuel_needed * Decimal('2')
        
        # Build result
        result = {
            'distance': float(dist),
            'consumption': float(cons),
            'fuel_price': float(price),
            'fuel_needed': float(fuel_needed),
            'total_cost': float(total_cost),
            'cost_per_km': float(cost_per_km),
            'return_trip': {
                'distance': float(dist * 2),
                'fuel_needed': float(return_trip_fuel),
                'total_cost': float(return_trip_cost)
            }
        }
        
        self.result = result
        return result
    
    @staticmethod
    def to_decimal(value) -> Decimal:
        """Convert value to Decimal for precise calculations"""
        if isinstance(value, Decimal):
            return value
        return Decimal(str(value))
