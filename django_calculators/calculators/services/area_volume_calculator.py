# Area and Volume Calculator Service
# Kalkulačka plochy a objemu pre rôzne geometrické tvary

import math

class AreaVolumeCalculator:
    """
    Service pre výpočet plochy a objemu geometrických tvarov.
    
    Podporované tvary:
    - 2D: Obdĺžnik, štvorec, kruh, trojuholník, lichobežník
    - 3D: Kocka, kváder, valec, guľa, ihlan, kužeľ
    """
    
    # 2D SHAPES - AREA
    
    @classmethod
    def rectangle_area(cls, length: float, width: float) -> dict:
        """Plocha obdĺžnika: length × width"""
        area = length * width
        perimeter = 2 * (length + width)
        
        return {
            'shape': 'rectangle',
            'shape_label': 'Obdĺžnik',
            'length': length,
            'width': width,
            'area': round(area, 4),
            'perimeter': round(perimeter, 4),
            'formula': f'{length} × {width} = {area:.2f}',
            'unit': 'cm²'
        }
    
    @classmethod
    def square_area(cls, side: float) -> dict:
        """Plocha štvorca: side²"""
        area = side ** 2
        perimeter = 4 * side
        
        return {
            'shape': 'square',
            'shape_label': 'Štvorec',
            'side': side,
            'area': round(area, 4),
            'perimeter': round(perimeter, 4),
            'formula': f'{side}² = {area:.2f}',
            'unit': 'cm²'
        }
    
    @classmethod
    def circle_area(cls, radius: float) -> dict:
        """Plocha kruhu: π × r²"""
        area = math.pi * (radius ** 2)
        circumference = 2 * math.pi * radius
        diameter = 2 * radius
        
        return {
            'shape': 'circle',
            'shape_label': 'Kruh',
            'radius': radius,
            'diameter': round(diameter, 4),
            'area': round(area, 4),
            'circumference': round(circumference, 4),
            'formula': f'π × {radius}² = {area:.2f}',
            'unit': 'cm²'
        }
    
    @classmethod
    def triangle_area(cls, base: float, height: float) -> dict:
        """Plocha trojuholníka: (base × height) / 2"""
        area = (base * height) / 2
        
        return {
            'shape': 'triangle',
            'shape_label': 'Trojuholník',
            'base': base,
            'height': height,
            'area': round(area, 4),
            'formula': f'({base} × {height}) / 2 = {area:.2f}',
            'unit': 'cm²'
        }
    
    @classmethod
    def trapezoid_area(cls, base_a: float, base_b: float, height: float) -> dict:
        """Plocha lichobežníka: ((a + b) / 2) × h"""
        area = ((base_a + base_b) / 2) * height
        
        return {
            'shape': 'trapezoid',
            'shape_label': 'Lichobežník',
            'base_a': base_a,
            'base_b': base_b,
            'height': height,
            'area': round(area, 4),
            'formula': f'(({base_a} + {base_b}) / 2) × {height} = {area:.2f}',
            'unit': 'cm²'
        }
    
    # 3D SHAPES - VOLUME
    
    @classmethod
    def cube_volume(cls, side: float) -> dict:
        """Objem kocky: side³"""
        volume = side ** 3
        surface_area = 6 * (side ** 2)
        
        return {
            'shape': 'cube',
            'shape_label': 'Kocka',
            'side': side,
            'volume': round(volume, 4),
            'surface_area': round(surface_area, 4),
            'formula': f'{side}³ = {volume:.2f}',
            'unit': 'cm³'
        }
    
    @classmethod
    def cuboid_volume(cls, length: float, width: float, height: float) -> dict:
        """Objem kvádra: length × width × height"""
        volume = length * width * height
        surface_area = 2 * (length * width + length * height + width * height)
        
        return {
            'shape': 'cuboid',
            'shape_label': 'Kváder',
            'length': length,
            'width': width,
            'height': height,
            'volume': round(volume, 4),
            'surface_area': round(surface_area, 4),
            'formula': f'{length} × {width} × {height} = {volume:.2f}',
            'unit': 'cm³'
        }
    
    @classmethod
    def cylinder_volume(cls, radius: float, height: float) -> dict:
        """Objem valca: π × r² × h"""
        volume = math.pi * (radius ** 2) * height
        surface_area = 2 * math.pi * radius * (radius + height)
        base_area = math.pi * (radius ** 2)
        
        return {
            'shape': 'cylinder',
            'shape_label': 'Valec',
            'radius': radius,
            'height': height,
            'diameter': round(2 * radius, 4),
            'volume': round(volume, 4),
            'surface_area': round(surface_area, 4),
            'base_area': round(base_area, 4),
            'formula': f'π × {radius}² × {height} = {volume:.2f}',
            'unit': 'cm³'
        }
    
    @classmethod
    def sphere_volume(cls, radius: float) -> dict:
        """Objem gule: (4/3) × π × r³"""
        volume = (4/3) * math.pi * (radius ** 3)
        surface_area = 4 * math.pi * (radius ** 2)
        diameter = 2 * radius
        
        return {
            'shape': 'sphere',
            'shape_label': 'Guľa',
            'radius': radius,
            'diameter': round(diameter, 4),
            'volume': round(volume, 4),
            'surface_area': round(surface_area, 4),
            'formula': f'(4/3) × π × {radius}³ = {volume:.2f}',
            'unit': 'cm³'
        }
    
    @classmethod
    def cone_volume(cls, radius: float, height: float) -> dict:
        """Objem kužeľa: (1/3) × π × r² × h"""
        volume = (1/3) * math.pi * (radius ** 2) * height
        slant_height = math.sqrt(radius ** 2 + height ** 2)
        surface_area = math.pi * radius * (radius + slant_height)
        
        return {
            'shape': 'cone',
            'shape_label': 'Kužeľ',
            'radius': radius,
            'height': height,
            'slant_height': round(slant_height, 4),
            'volume': round(volume, 4),
            'surface_area': round(surface_area, 4),
            'formula': f'(1/3) × π × {radius}² × {height} = {volume:.2f}',
            'unit': 'cm³'
        }
    
    @classmethod
    def pyramid_volume(cls, base_length: float, base_width: float, height: float) -> dict:
        """Objem ihlanu s obdĺžnikovou podstavou: (1/3) × base_area × h"""
        base_area = base_length * base_width
        volume = (1/3) * base_area * height
        
        return {
            'shape': 'pyramid',
            'shape_label': 'Ihlan (obdĺžniková podstava)',
            'base_length': base_length,
            'base_width': base_width,
            'height': height,
            'base_area': round(base_area, 4),
            'volume': round(volume, 4),
            'formula': f'(1/3) × {base_area:.2f} × {height} = {volume:.2f}',
            'unit': 'cm³'
        }
    
    # HELPER METHODS
    
    @classmethod
    def get_available_shapes(cls) -> dict:
        """Vráti zoznam dostupných tvarov s kompletnou konfiguráciou"""
        return {
            '2d': [
                {
                    'id': 'rectangle',
                    'name': 'Obdĺžnik',
                    'icon': '▭',
                    'type': '2d',
                    'dimensions': ['length', 'width'],
                    'dimension_labels': {
                        'length': 'Dĺžka (cm)',
                        'width': 'Šírka (cm)'
                    }
                },
                {
                    'id': 'square',
                    'name': 'Štvorec',
                    'icon': '▢',
                    'type': '2d',
                    'dimensions': ['side'],
                    'dimension_labels': {
                        'side': 'Strana (cm)'
                    }
                },
                {
                    'id': 'circle',
                    'name': 'Kruh',
                    'icon': '●',
                    'type': '2d',
                    'dimensions': ['radius'],
                    'dimension_labels': {
                        'radius': 'Polomer (cm)'
                    }
                },
                {
                    'id': 'triangle',
                    'name': 'Trojuholník',
                    'icon': '▲',
                    'type': '2d',
                    'dimensions': ['base', 'height'],
                    'dimension_labels': {
                        'base': 'Základňa (cm)',
                        'height': 'Výška (cm)'
                    }
                },
                {
                    'id': 'trapezoid',
                    'name': 'Lichobežník',
                    'icon': '⬟',
                    'type': '2d',
                    'dimensions': ['base_a', 'base_b', 'height'],
                    'dimension_labels': {
                        'base_a': 'Základňa A (cm)',
                        'base_b': 'Základňa B (cm)',
                        'height': 'Výška (cm)'
                    }
                }
            ],
            '3d': [
                {
                    'id': 'cube',
                    'name': 'Kocka',
                    'icon': '◻',
                    'type': '3d',
                    'dimensions': ['side'],
                    'dimension_labels': {
                        'side': 'Strana (cm)'
                    }
                },
                {
                    'id': 'cuboid',
                    'name': 'Kváder',
                    'icon': '▭',
                    'type': '3d',
                    'dimensions': ['length', 'width', 'height'],
                    'dimension_labels': {
                        'length': 'Dĺžka (cm)',
                        'width': 'Šírka (cm)',
                        'height': 'Výška (cm)'
                    }
                },
                {
                    'id': 'cylinder',
                    'name': 'Valec',
                    'icon': '○',
                    'type': '3d',
                    'dimensions': ['radius', 'height'],
                    'dimension_labels': {
                        'radius': 'Polomer (cm)',
                        'height': 'Výška (cm)'
                    }
                },
                {
                    'id': 'sphere',
                    'name': 'Guľa',
                    'icon': '⬤',
                    'type': '3d',
                    'dimensions': ['radius'],
                    'dimension_labels': {
                        'radius': 'Polomer (cm)'
                    }
                },
                {
                    'id': 'cone',
                    'name': 'Kužeľ',
                    'icon': '▼',
                    'type': '3d',
                    'dimensions': ['radius', 'height'],
                    'dimension_labels': {
                        'radius': 'Polomer (cm)',
                        'height': 'Výška (cm)'
                    }
                },
                {
                    'id': 'pyramid',
                    'name': 'Ihlan',
                    'icon': '△',
                    'type': '3d',
                    'dimensions': ['base_length', 'base_width', 'height'],
                    'dimension_labels': {
                        'base_length': 'Dĺžka podstavy (cm)',
                        'base_width': 'Šírka podstavy (cm)',
                        'height': 'Výška (cm)'
                    }
                }
            ]
        }
    
    @classmethod
    def calculate(cls, shape: str, dimensions: dict) -> dict:
        """
        Univerzálna metóda pre výpočet podľa tvaru.
        
        Args:
            shape: Typ tvaru (rectangle, circle, cube, sphere, atď.)
            dimensions: Dict s rozmermi (napr. {'length': 5, 'width': 3})
            
        Returns:
            dict s výsledkom výpočtu normalizovaný pre frontend
        """
        shape_methods = {
            # 2D
            'rectangle': lambda: cls.rectangle_area(dimensions['length'], dimensions['width']),
            'square': lambda: cls.square_area(dimensions['side']),
            'circle': lambda: cls.circle_area(dimensions['radius']),
            'triangle': lambda: cls.triangle_area(dimensions['base'], dimensions['height']),
            'trapezoid': lambda: cls.trapezoid_area(dimensions['base_a'], dimensions['base_b'], dimensions['height']),
            # 3D
            'cube': lambda: cls.cube_volume(dimensions['side']),
            'cuboid': lambda: cls.cuboid_volume(dimensions['length'], dimensions['width'], dimensions['height']),
            'cylinder': lambda: cls.cylinder_volume(dimensions['radius'], dimensions['height']),
            'sphere': lambda: cls.sphere_volume(dimensions['radius']),
            'cone': lambda: cls.cone_volume(dimensions['radius'], dimensions['height']),
            'pyramid': lambda: cls.pyramid_volume(dimensions['base_length'], dimensions['base_width'], dimensions['height'])
        }
        
        if shape not in shape_methods:
            raise ValueError(f"Neznámy tvar: {shape}")
        
        try:
            raw_result = shape_methods[shape]()
            # Normalize the response for frontend
            return cls._normalize_result(raw_result)
        except KeyError as e:
            raise ValueError(f"Chýbajúci parameter pre tvar {shape}: {e}")
    
    @classmethod
    def _normalize_result(cls, raw_result: dict) -> dict:
        """
        Normalizuje výsledok z individuálnych shape metód do formátu očakávaného frontendomen.
        
        Transformuje z formátu:
        {'shape': 'cylinder', 'volume': 3141.59, 'surface_area': 1256.64, ...}
        
        Do formátu:
        {'type': '3d', 'result': 3141.59, 'result_label': 'Objem', ...}
        """
        # Determine if it's 2D or 3D based on presence of volume/area key
        is_3d = 'volume' in raw_result
        shape_type = '3d' if is_3d else '2d'
        
        # Get the main result (area or volume)
        main_result = raw_result.get('volume') if is_3d else raw_result.get('area')
        result_label = 'Objem' if is_3d else 'Plocha'
        
        # Get secondary result (surface_area for 3D, perimeter/circumference for 2D)
        secondary_result = None
        secondary_label = None
        
        if is_3d and 'surface_area' in raw_result:
            secondary_result = raw_result['surface_area']
            secondary_label = 'Povrch'
        elif 'perimeter' in raw_result:
            secondary_result = raw_result['perimeter']
            secondary_label = 'Obvod'
        elif 'circumference' in raw_result:
            secondary_result = raw_result['circumference']
            secondary_label = 'Obvod'
        
        # Build normalized response
        normalized = {
            'type': shape_type,
            'shape_name': raw_result.get('shape_label', ''),
            'result': main_result,
            'result_label': result_label,
            'unit': raw_result.get('unit', ''),
            'formula': raw_result.get('formula', ''),
        }
        
        # Add secondary result if available
        if secondary_result is not None:
            normalized['secondary_result'] = secondary_result
            normalized['secondary_label'] = secondary_label
        
        # Include all other fields from raw result for reference
        normalized['raw_data'] = raw_result
        
        return normalized
