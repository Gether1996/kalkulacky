# Split Bill Calculator Service
# Kalkulačka na rozdelenie účtu medzi ľudí s tipom

from decimal import Decimal
from typing import List, Optional

class SplitBillCalculator:
    """
    Service pre rozdelenie účtu medzi viacerých ľudí.
    Podporuje tip a nerovnomerné rozdelenie.
    """
    
    # Štandardné sadzby tipu
    TIP_RATES = {
        'none': Decimal('0'),
        'low': Decimal('0.10'),      # 10%
        'standard': Decimal('0.15'),  # 15%
        'high': Decimal('0.20'),      # 20%
        'excellent': Decimal('0.25')  # 25%
    }
    
    TIP_LABELS = {
        'none': 'Bez tipu',
        'low': 'Nízky (10%)',
        'standard': 'Štandardný (15%)',
        'high': 'Vysoký (20%)',
        'excellent': 'Výborný (25%)'
    }
    
    @classmethod
    def split_equally(cls, total_amount: Decimal, num_people: int,
                     tip_percent: Decimal = Decimal('0'),
                     include_tip_in_total: bool = False) -> dict:
        """
        Rovnomerne rozdelí účet medzi ľudí.
        
        Args:
            total_amount: Celková suma účtu
            num_people: Počet ľudí
            tip_percent: Tip v percentách (napr. 15 = 15%)
            include_tip_in_total: Či je tip už zarátaný v celkovej sume
            
        Returns:
            dict s rozdelením účtu
        """
        if num_people <= 0:
            raise ValueError("Počet ľudí musí byť aspoň 1")
        
        if include_tip_in_total:
            # Tip je už v total_amount
            total_with_tip = total_amount
            tip_amount = Decimal('0')
            bill_before_tip = total_amount
        else:
            # Vypočítame tip
            tip_amount = total_amount * (tip_percent / 100)
            total_with_tip = total_amount + tip_amount
            bill_before_tip = total_amount
        
        # Rozdelenie na osobu
        per_person = total_with_tip / num_people
        per_person_before_tip = bill_before_tip / num_people
        tip_per_person = tip_amount / num_people if tip_amount > 0 else Decimal('0')
        
        return {
            'split_type': 'equal',
            'split_type_label': 'Rovnomerné rozdelenie',
            'total_amount': float(bill_before_tip),
            'num_people': num_people,
            'tip_percent': float(tip_percent),
            'tip_amount': round(float(tip_amount), 2),
            'total_with_tip': round(float(total_with_tip), 2),
            'per_person_before_tip': round(float(per_person_before_tip), 2),
            'per_person_tip': round(float(tip_per_person), 2),
            'per_person_total': round(float(per_person), 2),
            'breakdown': [
                {
                    'person': f'Osoba {i+1}',
                    'amount_before_tip': round(float(per_person_before_tip), 2),
                    'tip': round(float(tip_per_person), 2),
                    'total': round(float(per_person), 2)
                }
                for i in range(num_people)
            ]
        }
    
    @classmethod
    def split_by_items(cls, items: List[dict], tip_percent: Decimal = Decimal('0')) -> dict:
        """
        Rozdelí účet podľa toho, čo kto konzumoval.
        
        Args:
            items: List items, každý item má {'person': str, 'amount': float}
            tip_percent: Tip v percentách
            
        Returns:
            dict s rozdelením účtu podľa ľudí
        """
        if not items:
            raise ValueError("Musí byť aspoň jedna položka")
        
        # Zoskupíme položky podľa osôb
        people_dict = {}
        total_before_tip = Decimal('0')
        
        for item in items:
            person = item['person']
            amount = Decimal(str(item['amount']))
            
            if person not in people_dict:
                people_dict[person] = Decimal('0')
            
            people_dict[person] += amount
            total_before_tip += amount
        
        # Vypočítame tip
        tip_amount = total_before_tip * (tip_percent / 100)
        total_with_tip = total_before_tip + tip_amount
        
        # Rozdelíme tip proporcionálne
        breakdown = []
        for person, person_amount in people_dict.items():
            # Tip pre túto osobu (proporcionálne k jej podiel)
            person_tip = (person_amount / total_before_tip) * tip_amount if total_before_tip > 0 else Decimal('0')
            person_total = person_amount + person_tip
            
            breakdown.append({
                'person': person,
                'amount_before_tip': round(float(person_amount), 2),
                'tip': round(float(person_tip), 2),
                'total': round(float(person_total), 2),
                'percentage_of_bill': round(float(person_amount / total_before_tip * 100), 1) if total_before_tip > 0 else 0
            })
        
        # Zoradíme podľa sumy
        breakdown.sort(key=lambda x: x['total'], reverse=True)
        
        return {
            'split_type': 'by_items',
            'split_type_label': 'Podľa položiek',
            'total_amount': float(total_before_tip),
            'num_people': len(people_dict),
            'tip_percent': float(tip_percent),
            'tip_amount': round(float(tip_amount), 2),
            'total_with_tip': round(float(total_with_tip), 2),
            'breakdown': breakdown
        }
    
    @classmethod
    def split_custom(cls, total_amount: Decimal, custom_amounts: List[dict],
                    tip_percent: Decimal = Decimal('0')) -> dict:
        """
        Vlastné rozdelenie, kde určíte presnú sumu pre každú osobu.
        
        Args:
            total_amount: Celková suma účtu
            custom_amounts: List [{'person': str, 'amount': float}, ...]
            tip_percent: Tip v percentách
            
        Returns:
            dict s vlastným rozdelením
        """
        if not custom_amounts:
            raise ValueError("Musí byť aspoň jedna osoba")
        
        # Spočítame custom sumy
        custom_total = sum(Decimal(str(item['amount'])) for item in custom_amounts)
        
        # Check if custom amounts match total
        difference = total_amount - custom_total
        
        # Vypočítame tip
        tip_amount = total_amount * (tip_percent / 100)
        total_with_tip = total_amount + tip_amount
        
        breakdown = []
        for item in custom_amounts:
            person = item['person']
            amount_before_tip = Decimal(str(item['amount']))
            
            # Tip pre túto osobu (proporcionálne)
            person_tip = (amount_before_tip / total_amount) * tip_amount if total_amount > 0 else Decimal('0')
            person_total = amount_before_tip + person_tip
            
            breakdown.append({
                'person': person,
                'amount_before_tip': round(float(amount_before_tip), 2),
                'tip': round(float(person_tip), 2),
                'total': round(float(person_total), 2)
            })
        
        return {
            'split_type': 'custom',
            'split_type_label': 'Vlastné rozdelenie',
            'total_amount': float(total_amount),
            'custom_total': float(custom_total),
            'difference': round(float(difference), 2),
            'num_people': len(custom_amounts),
            'tip_percent': float(tip_percent),
            'tip_amount': round(float(tip_amount), 2),
            'total_with_tip': round(float(total_with_tip), 2),
            'breakdown': breakdown
        }
    
    @classmethod
    def calculate_tip_only(cls, amount: Decimal, tip_percent: Decimal) -> dict:
        """
        Vypočíta len tip pre danú sumu.
        
        Args:
            amount: Suma účtu
            tip_percent: Tip v percentách
            
        Returns:
            dict s tipom a celkovou sumou
        """
        tip_amount = amount * (tip_percent / 100)
        total = amount + tip_amount
        
        return {
            'amount': float(amount),
            'tip_percent': float(tip_percent),
            'tip_amount': round(float(tip_amount), 2),
            'total': round(float(total), 2)
        }
    
    @classmethod
    def get_tip_suggestions(cls, amount: Decimal) -> dict:
        """
        Vráti návrhy tipov pre rôzne sadzby.
        
        Args:
            amount: Suma účtu
            
        Returns:
            dict s návrhmi tipov (pole)
        """
        suggestions = []
        
        for key, rate in cls.TIP_RATES.items():
            tip = amount * rate
            total = amount + tip
            
            suggestions.append({
                'id': key,
                'label': cls.TIP_LABELS[key],
                'percent': float(rate * 100),
                'tip_amount': round(float(tip), 2),
                'total': round(float(total), 2)
            })
        
        return {
            'amount': float(amount),
            'suggestions': suggestions
        }
