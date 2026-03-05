# Unit Converter Service
# Konvertor jednotiek pre rôzne kategórie

class UnitConverterService:
    """
    Service pre konverziu jednotiek.
    Podporované kategórie: dĺžka, hmotnosť, teplota, objem, plocha
    """
    
    # Konverzné faktory voči základnej jednotke
    # Pre dĺžku: meter
    LENGTH_UNITS = {
        'millimeter': 0.001,
        'centimeter': 0.01,
        'meter': 1,
        'kilometer': 1000,
        'inch': 0.0254,
        'foot': 0.3048,
        'yard': 0.9144,
        'mile': 1609.344
    }
    
    # Pre hmotnosť: kilogram
    WEIGHT_UNITS = {
        'milligram': 0.000001,
        'gram': 0.001,
        'kilogram': 1,
        'ton': 1000,
        'ounce': 0.028349523125,
        'pound': 0.45359237
    }
    
    # Pre objem: liter
    VOLUME_UNITS = {
        'milliliter': 0.001,
        'liter': 1,
        'cubic_meter': 1000,
        'gallon_us': 3.785411784,
        'gallon_uk': 4.54609,
        'fluid_ounce_us': 0.0295735295625,
        'fluid_ounce_uk': 0.0284130625,
        'cup': 0.240,
        'pint': 0.473176
    }
    
    # Pre plochu: square meter
    AREA_UNITS = {
        'square_millimeter': 0.000001,
        'square_centimeter': 0.0001,
        'square_meter': 1,
        'square_kilometer': 1000000,
        'hectare': 10000,
        'square_inch': 0.00064516,
        'square_foot': 0.09290304,
        'square_yard': 0.83612736,
        'acre': 4046.8564224,
        'square_mile': 2589988.110336
    }
    
    # Teplota vyžaduje špeciálne vzorce
    TEMPERATURE_UNITS = ['celsius', 'fahrenheit', 'kelvin']
    
    CATEGORY_UNITS = {
        'length': LENGTH_UNITS,
        'weight': WEIGHT_UNITS,
        'volume': VOLUME_UNITS,
        'area': AREA_UNITS,
        'temperature': TEMPERATURE_UNITS
    }
    
    # Slovenské názvy kategórií a jednotiek
    CATEGORY_NAMES_SK = {
        'length': 'Dĺžka',
        'weight': 'Hmotnosť',
        'volume': 'Objem',
        'area': 'Plocha',
        'temperature': 'Teplota'
    }
    
    UNIT_NAMES_SK = {
        # Dĺžka
        'millimeter': 'Milimeter (mm)',
        'centimeter': 'Centimeter (cm)',
        'meter': 'Meter (m)',
        'kilometer': 'Kilometer (km)',
        'inch': 'Palec (in)',
        'foot': 'Stopa (ft)',
        'yard': 'Yard (yd)',
        'mile': 'Míľa (mi)',
        # Hmotnosť
        'milligram': 'Miligram (mg)',
        'gram': 'Gram (g)',
        'kilogram': 'Kilogram (kg)',
        'ton': 'Tona (t)',
        'ounce': 'Unca (oz)',
        'pound': 'Libra (lb)',
        # Objem
        'milliliter': 'Mililiter (ml)',
        'liter': 'Liter (l)',
        'cubic_meter': 'Kubický meter (m³)',
        'gallon_us': 'Galón US (gal)',
        'gallon_uk': 'Galón UK (gal)',
        'fluid_ounce_us': 'Tekutá unca US (fl oz)',
        'fluid_ounce_uk': 'Tekutá unca UK (fl oz)',
        'cup': 'Šálka (cup)',
        'pint': 'Pinta (pt)',
        # Plocha
        'square_millimeter': 'Štvorcový milimeter (mm²)',
        'square_centimeter': 'Štvorcový centimeter (cm²)',
        'square_meter': 'Štvorcový meter (m²)',
        'square_kilometer': 'Štvorcový kilometer (km²)',
        'hectare': 'Hektár (ha)',
        'square_inch': 'Štvorcový palec (in²)',
        'square_foot': 'Štvorcová stopa (ft²)',
        'square_yard': 'Štvorcový yard (yd²)',
        'acre': 'Aker (ac)',
        'square_mile': 'Štvorcová míľa (mi²)',
        # Teplota
        'celsius': 'Celsius (°C)',
        'fahrenheit': 'Fahrenheit (°F)',
        'kelvin': 'Kelvin (K)'
    }
    
    @classmethod
    def convert(cls, value: float, from_unit: str, to_unit: str, category: str) -> dict:
        """
        Konvertuje hodnotu z jednej jednotky na inú.
        
        Args:
            value: Hodnota na konverziu
            from_unit: Zdrojová jednotka
            to_unit: Cieľová jednotka
            category: Kategória (length, weight, volume, area, temperature)
            
        Returns:
            dict s výsledkom konverzie
        """
        # Validácia
        if category not in cls.CATEGORY_UNITS:
            raise ValueError(f"Neplatná kategória: {category}")
        
        # Špeciálne spracovanie teploty
        if category == 'temperature':
            result = cls._convert_temperature(value, from_unit, to_unit)
        else:
            # Štandardná konverzia cez základnú jednotku
            units_dict = cls.CATEGORY_UNITS[category]
            
            if from_unit not in units_dict:
                raise ValueError(f"Neplatná zdrojová jednotka: {from_unit}")
            if to_unit not in units_dict:
                raise ValueError(f"Neplatná cieľová jednotka: {to_unit}")
            
            # Konverzia: value -> base_unit -> target_unit
            base_value = value * units_dict[from_unit]
            result = base_value / units_dict[to_unit]
        
        return {
            'value': value,
            'from_unit': from_unit,
            'from_unit_name': cls.UNIT_NAMES_SK.get(from_unit, from_unit),
            'to_unit': to_unit,
            'to_unit_name': cls.UNIT_NAMES_SK.get(to_unit, to_unit),
            'result': round(result, 6),
            'category': category,
            'category_name': cls.CATEGORY_NAMES_SK.get(category, category),
            'formula': cls._get_formula_explanation(value, from_unit, to_unit, category, result)
        }
    
    @classmethod
    def _convert_temperature(cls, value: float, from_unit: str, to_unit: str) -> float:
        """Konverzia teploty - Celsius, Fahrenheit, Kelvin"""
        if from_unit not in cls.TEMPERATURE_UNITS:
            raise ValueError(f"Neplatná zdrojová jednotka teploty: {from_unit}")
        if to_unit not in cls.TEMPERATURE_UNITS:
            raise ValueError(f"Neplatná cieľová jednotka teploty: {to_unit}")
        
        # Konverzia všetkého najprv na Celsius
        if from_unit == 'celsius':
            celsius = value
        elif from_unit == 'fahrenheit':
            celsius = (value - 32) * 5 / 9
        elif from_unit == 'kelvin':
            celsius = value - 273.15
        
        # Konverzia z Celsius na cieľovú jednotku
        if to_unit == 'celsius':
            return celsius
        elif to_unit == 'fahrenheit':
            return celsius * 9 / 5 + 32
        elif to_unit == 'kelvin':
            return celsius + 273.15
    
    @classmethod
    def _get_formula_explanation(cls, value: float, from_unit: str, to_unit: str, 
                                 category: str, result: float) -> str:
        """Vygeneruje vysvetlenie vzorca pre konverziu"""
        if category == 'temperature':
            if from_unit == 'celsius' and to_unit == 'fahrenheit':
                return f"{value}°C × 9/5 + 32 = {result:.2f}°F"
            elif from_unit == 'fahrenheit' and to_unit == 'celsius':
                return f"({value}°F - 32) × 5/9 = {result:.2f}°C"
            elif from_unit == 'celsius' and to_unit == 'kelvin':
                return f"{value}°C + 273.15 = {result:.2f}K"
            elif from_unit == 'kelvin' and to_unit == 'celsius':
                return f"{value}K - 273.15 = {result:.2f}°C"
            elif from_unit == 'fahrenheit' and to_unit == 'kelvin':
                return f"({value}°F - 32) × 5/9 + 273.15 = {result:.2f}K"
            elif from_unit == 'kelvin' and to_unit == 'fahrenheit':
                return f"({value}K - 273.15) × 9/5 + 32 = {result:.2f}°F"
        else:
            units_dict = cls.CATEGORY_UNITS[category]
            factor = units_dict[to_unit] / units_dict[from_unit]
            return f"{value} × {factor:.6f} = {result:.6f}"
        
        return ""
    
    @classmethod
    def get_available_units(cls, category: str) -> list:
        """Vráti zoznam dostupných jednotiek pre danú kategóriu"""
        if category not in cls.CATEGORY_UNITS:
            return []
        
        if category == 'temperature':
            units = cls.TEMPERATURE_UNITS
        else:
            units = list(cls.CATEGORY_UNITS[category].keys())
        
        return [
            {
                'value': unit,
                'label': cls.UNIT_NAMES_SK.get(unit, unit)
            }
            for unit in units
        ]
    
    @classmethod
    def get_categories(cls) -> list:
        """Vráti zoznam všetkých kategórií"""
        return [
            {
                'value': key,
                'label': cls.CATEGORY_NAMES_SK.get(key, key)
            }
            for key in cls.CATEGORY_UNITS.keys()
        ]
