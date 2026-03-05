"""
BMR (Basal Metabolic Rate) Calculator Service
Calculates daily caloric needs based on age, weight, height, gender, and activity level.
"""
from decimal import Decimal
from typing import Dict, Any
from .base_calculator import BaseCalculator


class BMRCalculator(BaseCalculator):
    """
    Calculates BMR (Basal Metabolic Rate) and daily caloric needs.
    
    Uses multiple formulas:
    - Harris-Benedict Equation (revised)
    - Mifflin-St Jeor Equation (more accurate)
    
    Also calculates TDEE (Total Daily Energy Expenditure) based on activity level.
    """
    
    # Activity multipliers for TDEE calculation
    ACTIVITY_MULTIPLIERS = {
        'sedentary': Decimal('1.2'),        # Little or no exercise
        'light': Decimal('1.375'),          # Light exercise 1-3 days/week
        'moderate': Decimal('1.55'),        # Moderate exercise 3-5 days/week
        'active': Decimal('1.725'),         # Hard exercise 6-7 days/week
        'very_active': Decimal('1.9')       # Very hard exercise, physical job
    }
    
    # Weight change goals (calories per day adjustment)
    WEIGHT_GOALS = {
        'lose_fast': Decimal('-1000'),      # Lose ~1kg per week
        'lose_moderate': Decimal('-500'),   # Lose ~0.5kg per week
        'lose_slow': Decimal('-250'),       # Lose ~0.25kg per week
        'maintain': Decimal('0'),
        'gain_slow': Decimal('250'),        # Gain ~0.25kg per week
        'gain_moderate': Decimal('500'),    # Gain ~0.5kg per week
        'gain_fast': Decimal('1000')        # Gain ~1kg per week
    }
    
    def calculate(
        self,
        weight: float,
        height: float,
        age: int,
        gender: str,
        activity_level: str = 'sedentary',
        weight_goal: str = 'maintain',
        **kwargs
    ) -> Dict[str, Any]:
        """
        Calculate BMR and daily caloric needs.
        
        Parameters:
        - weight: Weight in kg
        - height: Height in cm
        - age: Age in years
        - gender: 'male' or 'female'
        - activity_level: Activity level (sedentary, light, moderate, active, very_active)
        - weight_goal: Weight goal (lose_fast, lose_moderate, lose_slow, maintain, gain_slow, gain_moderate, gain_fast)
        
        Returns:
        Dictionary with BMR, TDEE, and caloric recommendations
        """
        weight = Decimal(str(weight))
        height = Decimal(str(height))
        age = int(age)
        gender = str(gender).lower()
        activity_level = str(activity_level)
        weight_goal = str(weight_goal)
        
        # Validate inputs
        if weight <= 0:
            raise ValueError("Hmotnosť musí byť väčšia ako 0")
        
        if height <= 0:
            raise ValueError("Výška musí byť väčšia ako 0")
        
        if age < 15 or age > 100:
            raise ValueError("Vek musí byť medzi 15 a 100 rokmi")
        
        if gender not in ['male', 'female']:
            raise ValueError("Pohlavie musí byť 'male' alebo 'female'")
        
        if activity_level not in self.ACTIVITY_MULTIPLIERS:
            raise ValueError(f"Neplatná úroveň aktivity. Použite: {', '.join(self.ACTIVITY_MULTIPLIERS.keys())}")
        
        if weight_goal not in self.WEIGHT_GOALS:
            raise ValueError(f"Neplatný cieľ hmotnosti. Použite: {', '.join(self.WEIGHT_GOALS.keys())}")
        
        # Calculate BMR using Mifflin-St Jeor Equation (more accurate)
        if gender == 'male':
            bmr_mifflin = (Decimal('10') * weight) + (Decimal('6.25') * height) - (Decimal('5') * Decimal(str(age))) + Decimal('5')
        else:  # female
            bmr_mifflin = (Decimal('10') * weight) + (Decimal('6.25') * height) - (Decimal('5') * Decimal(str(age))) - Decimal('161')
        
        # Calculate BMR using Harris-Benedict Equation (revised)
        if gender == 'male':
            bmr_harris = (Decimal('13.397') * weight) + (Decimal('4.799') * height) - (Decimal('5.677') * Decimal(str(age))) + Decimal('88.362')
        else:  # female
            bmr_harris = (Decimal('9.247') * weight) + (Decimal('3.098') * height) - (Decimal('4.330') * Decimal(str(age))) + Decimal('447.593')
        
        # Use Mifflin-St Jeor as primary (more accurate), Harris-Benedict for comparison
        bmr = bmr_mifflin
        
        # Calculate TDEE (Total Daily Energy Expenditure)
        activity_multiplier = self.ACTIVITY_MULTIPLIERS[activity_level]
        tdee = bmr * activity_multiplier
        
        # Calculate calories for weight goal
        calorie_adjustment = self.WEIGHT_GOALS[weight_goal]
        target_calories = tdee + calorie_adjustment
        
        # Ensure minimum safe calories (1200 for women, 1500 for men)
        min_safe_calories = Decimal('1200') if gender == 'female' else Decimal('1500')
        if target_calories < min_safe_calories:
            target_calories = min_safe_calories
            is_below_minimum = True
        else:
            is_below_minimum = False
        
        # Calculate macronutrient distribution (example: balanced diet)
        protein_percentage = Decimal('0.30')  # 30% protein
        carbs_percentage = Decimal('0.40')    # 40% carbs
        fats_percentage = Decimal('0.30')     # 30% fats
        
        # Calories per gram: Protein=4, Carbs=4, Fats=9
        protein_calories = target_calories * protein_percentage
        carbs_calories = target_calories * carbs_percentage
        fats_calories = target_calories * fats_percentage
        
        protein_grams = protein_calories / Decimal('4')
        carbs_grams = carbs_calories / Decimal('4')
        fats_grams = fats_calories / Decimal('9')
        
        # Calculate time to reach weight goal (if applicable)
        if weight_goal != 'maintain':
            # Assuming 7700 calories = 1kg of body weight
            calories_per_kg = Decimal('7700')
            weekly_calorie_deficit = abs(calorie_adjustment) * Decimal('7')
            kg_per_week = weekly_calorie_deficit / calories_per_kg
        else:
            kg_per_week = Decimal('0')
        
        # BMI calculation for reference
        height_m = height / Decimal('100')
        bmi = weight / (height_m * height_m)
        
        # Activity level descriptions
        activity_descriptions = {
            'sedentary': 'Sedavý životný štýl (žiadne cvičenie)',
            'light': 'Mierna aktivita (cvičenie 1-3x týždenne)',
            'moderate': 'Stredná aktivita (cvičenie 3-5x týždenne)',
            'active': 'Aktívny (intenzívne cvičenie 6-7x týždenne)',
            'very_active': 'Veľmi aktívny (veľmi intenzívne cvičenie, fyzická práca)'
        }
        
        # Weight goal descriptions
        goal_descriptions = {
            'lose_fast': 'Rýchle chudnutie (~1kg/týždeň)',
            'lose_moderate': 'Stredné chudnutie (~0.5kg/týždeň)',
            'lose_slow': 'Pomalé chudnutie (~0.25kg/týždeň)',
            'maintain': 'Udržanie hmotnosti',
            'gain_slow': 'Pomalé pribieranie (~0.25kg/týždeň)',
            'gain_moderate': 'Stredné pribieranie (~0.5kg/týždeň)',
            'gain_fast': 'Rýchle pribieranie (~1kg/týždeň)'
        }
        
        return {
            'bmr': {
                'mifflin_st_jeor': self.round_decimal(bmr_mifflin, 0),
                'harris_benedict': self.round_decimal(bmr_harris, 0),
                'recommended': self.round_decimal(bmr, 0)
            },
            'tdee': {
                'calories': self.round_decimal(tdee, 0),
                'activity_level': activity_level,
                'activity_description': activity_descriptions[activity_level],
                'activity_multiplier': float(activity_multiplier)
            },
            'recommendations': {
                'weight_goal': weight_goal,
                'goal_description': goal_descriptions[weight_goal],
                'calorie_adjustment': self.round_decimal(calorie_adjustment, 0),
                'target_calories': self.round_decimal(target_calories, 0),
                'is_below_minimum': is_below_minimum,
                'min_safe_calories': self.round_decimal(min_safe_calories, 0),
                'kg_per_week': self.round_decimal(kg_per_week, 2) if weight_goal != 'maintain' else None
            },
            'macros': {
                'protein': {
                    'grams': self.round_decimal(protein_grams, 0),
                    'calories': self.round_decimal(protein_calories, 0),
                    'percentage': float(protein_percentage * 100)
                },
                'carbs': {
                    'grams': self.round_decimal(carbs_grams, 0),
                    'calories': self.round_decimal(carbs_calories, 0),
                    'percentage': float(carbs_percentage * 100)
                },
                'fats': {
                    'grams': self.round_decimal(fats_grams, 0),
                    'calories': self.round_decimal(fats_calories, 0),
                    'percentage': float(fats_percentage * 100)
                }
            },
            'profile': {
                'weight': self.round_decimal(weight, 1),
                'height': self.round_decimal(height, 0),
                'age': age,
                'gender': gender,
                'bmi': self.round_decimal(bmi, 1)
            }
        }
    
    def get_metadata(self) -> Dict[str, Any]:
        """Return metadata about the BMR calculator."""
        return {
            'name': 'BMR Calculator',
            'description': 'Calculate Basal Metabolic Rate and daily caloric needs',
            'version': '1.0.0',
            'parameters': {
                'required': ['weight', 'height', 'age', 'gender'],
                'optional': ['activity_level', 'weight_goal'],
                'weight': {
                    'type': 'decimal',
                    'description': 'Weight in kg',
                    'min': 0
                },
                'height': {
                    'type': 'decimal',
                    'description': 'Height in cm',
                    'min': 0
                },
                'age': {
                    'type': 'integer',
                    'description': 'Age in years',
                    'min': 15,
                    'max': 100
                },
                'gender': {
                    'type': 'string',
                    'description': 'Gender',
                    'choices': ['male', 'female']
                },
                'activity_level': {
                    'type': 'string',
                    'description': 'Activity level',
                    'choices': ['sedentary', 'light', 'moderate', 'active', 'very_active'],
                    'default': 'sedentary'
                },
                'weight_goal': {
                    'type': 'string',
                    'description': 'Weight goal',
                    'choices': ['lose_fast', 'lose_moderate', 'lose_slow', 'maintain', 'gain_slow', 'gain_moderate', 'gain_fast'],
                    'default': 'maintain'
                }
            },
            'example_request': {
                'weight': 75,
                'height': 175,
                'age': 30,
                'gender': 'male',
                'activity_level': 'moderate',
                'weight_goal': 'lose_moderate'
            }
        }
