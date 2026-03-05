"""
BMI Calculator - Kalkulačka BMI (Body Mass Index)

Calculates Body Mass Index and provides health category classification.

Search Volume: 10,000+/month 🔥🔥
Keywords: "bmi kalkulačka", "index telesnej hmotnosti", "bmi výpočet"
"""

from decimal import Decimal
from typing import Dict, Any
from .base_calculator import BaseCalculator


class BMICalculator(BaseCalculator):
    """
    BMI Calculator (Body Mass Index)
    
    Calculates:
    - BMI value
    - Health category (underweight, normal, overweight, obese)
    - Ideal weight range
    - Weight to gain/lose to reach ideal
    """
    
    # BMI Categories (WHO standards)
    BMI_CATEGORIES = {
        'underweight': (0, 18.5),
        'normal': (18.5, 25),
        'overweight': (25, 30),
        'obese_class1': (30, 35),
        'obese_class2': (35, 40),
        'obese_class3': (40, 999)
    }
    
    def validate_inputs(self, **kwargs) -> bool:
        """Validate BMI calculator inputs"""
        weight = kwargs.get('weight')
        height = kwargs.get('height')
        
        if not all([weight, height]):
            raise ValueError("weight and height are required")
        
        try:
            w = self.to_decimal(weight)
            h = self.to_decimal(height)
        except (ValueError, TypeError):
            raise ValueError("Weight and height must be valid numbers")
        
        if w <= 0 or w > 500:
            raise ValueError("Weight must be between 1 and 500 kg")
        
        if h <= 0 or h > 300:
            raise ValueError("Height must be between 1 and 300 cm")
        
        if h < 50:
            raise ValueError("Height seems too low (less than 50 cm)")
        
        return True
    
    def calculate(
        self, 
        weight: float, 
        height: float,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Calculate BMI.
        
        Args:
            weight: Weight in kilograms
            height: Height in centimeters
            
        Returns:
            Dictionary with calculation results
        """
        # Validate inputs
        self.validate_inputs(weight=weight, height=height)
        
        # Convert to Decimal for precision
        weight_kg = self.to_decimal(weight)
        height_cm = self.to_decimal(height)
        
        # Convert height from cm to meters
        height_m = height_cm / Decimal('100')
        
        # Calculate BMI: weight (kg) / height (m)²
        bmi = weight_kg / (height_m ** 2)
        
        # Determine category
        category_info = self._get_category(float(bmi))
        
        # Calculate ideal weight range (BMI 18.5 - 25)
        ideal_weight_min = Decimal('18.5') * (height_m ** 2)
        ideal_weight_max = Decimal('25') * (height_m ** 2)
        
        # Calculate weight differences
        weight_to_ideal_min = ideal_weight_min - weight_kg
        weight_to_ideal_max = ideal_weight_max - weight_kg
        
        # Determine recommendation
        if bmi < 18.5:
            weight_to_change = weight_to_ideal_min
            recommendation = "nabrat"
        elif bmi > 25:
            weight_to_change = weight_to_ideal_max
            recommendation = "schudnúť"
        else:
            weight_to_change = Decimal('0')
            recommendation = "udržať"
        
        # Build result
        result = {
            'bmi': float(bmi),
            'weight': float(weight_kg),
            'height': float(height_cm),
            'height_meters': float(height_m),
            'category': category_info['category'],
            'category_sk': category_info['category_sk'],
            'category_description': category_info['description'],
            'health_risk': category_info['health_risk'],
            'ideal_weight_range': {
                'min': float(ideal_weight_min),
                'max': float(ideal_weight_max)
            },
            'weight_to_change': float(abs(weight_to_change)),
            'recommendation': recommendation,
            'is_healthy': 18.5 <= bmi <= 25
        }
        
        self.result = result
        return result
    
    def _get_category(self, bmi: float) -> Dict[str, str]:
        """Get BMI category information"""
        if bmi < 18.5:
            return {
                'category': 'underweight',
                'category_sk': 'Podvýživa',
                'description': 'Máte nižšiu hmotnosť než je zdravé',
                'health_risk': 'Zvýšené riziko zdravotných problémov'
            }
        elif 18.5 <= bmi < 25:
            return {
                'category': 'normal',
                'category_sk': 'Normálna hmotnosť',
                'description': 'Vaša hmotnosť je v zdravom rozmedzí',
                'health_risk': 'Minimálne riziko'
            }
        elif 25 <= bmi < 30:
            return {
                'category': 'overweight',
                'category_sk': 'Nadváha',
                'description': 'Máte vyššiu hmotnosť než je zdravé',
                'health_risk': 'Mierne zvýšené riziko'
            }
        elif 30 <= bmi < 35:
            return {
                'category': 'obese_class1',
                'category_sk': 'Obezita 1. stupňa',
                'description': 'Obezita prvého stupňa',
                'health_risk': 'Zvýšené riziko'
            }
        elif 35 <= bmi < 40:
            return {
                'category': 'obese_class2',
                'category_sk': 'Obezita 2. stupňa',
                'description': 'Obezita druhého stupňa',
                'health_risk': 'Vysoké riziko'
            }
        else:
            return {
                'category': 'obese_class3',
                'category_sk': 'Obezita 3. stupňa',
                'description': 'Obezita tretieho stupňa (morbídna)',
                'health_risk': 'Veľmi vysoké riziko'
            }
    
    @staticmethod
    def to_decimal(value) -> Decimal:
        """Convert value to Decimal for precise calculations"""
        if isinstance(value, Decimal):
            return value
        return Decimal(str(value))
