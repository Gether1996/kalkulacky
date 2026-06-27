# Sick Leave (Pracovná neschopnosť / PN) Calculator Service
# Výpočet nemocenských dávok podľa slovenskej legislatívy

from decimal import Decimal
from datetime import datetime
from . import config_variables as cfg

class SickLeaveCalculator:
    """
    Service pre výpočet nemocenských dávok pri pracovnej neschopnosti na Slovensku (2026).
    
    Pravidlá (choroba):
    - 1.-3. deň: 25% denného vymeriavacieho základu (DVZ) - platí zamestnávateľ
    - 4.-10. deň: 55% DVZ - platí zamestnávateľ (náhrada príjmu)
    - od 11. dňa: 55% DVZ - platí Sociálna poisťovňa
    Ošetrovné (OČR): 55% DVZ od 1. dňa - platí Sociálna poisťovňa.

    DVZ = hrubá mzda za posledných 12 mesiacov / 365
    """

    # Konštanty pre výpočet (2026) - importované z config_variables
    EMPLOYER_PAYMENT_DAYS = cfg.SICK_LEAVE_EMPLOYER_PAYMENT_DAYS  # zamestnávateľ platí dni 1-10
    EMPLOYER_TIER1_DAYS = cfg.SICK_LEAVE_EMPLOYER_TIER1_DAYS  # dni 1-3 (25%)
    EMPLOYER_RATE = cfg.SICK_LEAVE_EMPLOYER_RATE  # 25% DVZ
    INSURANCE_RATE_ILLNESS = cfg.SICK_LEAVE_INSURANCE_RATE_ILLNESS  # 55% DVZ od 4. dňa
    INSURANCE_RATE_CARE = cfg.SICK_LEAVE_INSURANCE_RATE_CARE  # 55% DVZ pri ošetrovaní
    
    # Maximum vymeriavací základ pre 2026
    MAX_ASSESSMENT_BASE_YEARLY = cfg.SICK_LEAVE_MAX_ASSESSMENT_BASE_YEARLY  # €88,200 ročne
    MAX_ASSESSMENT_BASE_DAILY = cfg.SICK_LEAVE_MAX_ASSESSMENT_BASE_DAILY  # €241.64 denne
    
    # Minimum mzda 2026
    MIN_WAGE_MONTHLY = cfg.SICK_LEAVE_MIN_WAGE_MONTHLY  # €750/month
    MIN_WAGE_DAILY = cfg.SICK_LEAVE_MIN_WAGE_DAILY  # Daily minimum
    
    @classmethod
    def calculate_sick_leave(cls, gross_salary: Decimal, days_sick: int, 
                            leave_type: str = 'illness') -> dict:
        """
        Vypočíta nemocenskú dávku.
        
        Args:
            gross_salary: Hrubá mesačná mzda v EUR
            days_sick: Počet dní pracovnej neschopnosti
            leave_type: 'illness' (choroba) alebo 'care' (ošetrovanie člena rodiny)
            
        Returns:
            dict s detailmi výpočtu nemocenskej
        """
        # Výpočet denného vymeriavacieho základu (DVZ)
        # Predpokladáme, že mzda za posledných 12 mesiacov = aktuálna mzda * 12
        yearly_salary = gross_salary * 12
        daily_assessment_base = yearly_salary / 365
        
        # Aplikovanie stropu (maximum DVZ)
        if daily_assessment_base > cls.MAX_ASSESSMENT_BASE_DAILY:
            capped_daily_base = cls.MAX_ASSESSMENT_BASE_DAILY
            is_capped = True
        else:
            capped_daily_base = daily_assessment_base
            is_capped = False
        
        # Výpočet nemocenskej podľa dní (SK 2026)
        insurance_rate = cls.INSURANCE_RATE_CARE if leave_type == 'care' else cls.INSURANCE_RATE_ILLNESS

        if leave_type == 'care':
            # Ošetrovné (OČR): platí Sociálna poisťovňa od 1. dňa (55% DVZ).
            employer_days = 0
            insurance_days = days_sick
            employer_payment = Decimal('0')
            insurance_payment = insurance_days * capped_daily_base * insurance_rate
        else:
            # Choroba: zamestnávateľ platí dni 1-10 (1.-3. deň 25%, 4.-10. deň 55%),
            # od 11. dňa platí Sociálna poisťovňa (55%).
            tier1_days = min(days_sick, cls.EMPLOYER_TIER1_DAYS)
            tier2_days = max(0, min(days_sick, cls.EMPLOYER_PAYMENT_DAYS) - cls.EMPLOYER_TIER1_DAYS)
            employer_days = tier1_days + tier2_days
            insurance_days = max(0, days_sick - cls.EMPLOYER_PAYMENT_DAYS)
            employer_payment = (
                tier1_days * capped_daily_base * cls.EMPLOYER_RATE
                + tier2_days * capped_daily_base * cls.INSURANCE_RATE_ILLNESS
            )
            insurance_payment = insurance_days * capped_daily_base * insurance_rate

        # Celková nemocenská
        total_sick_leave = employer_payment + insurance_payment
        
        # Denná sadzba
        avg_daily_rate = total_sick_leave / days_sick if days_sick > 0 else Decimal('0')
        
        # Porovnanie s plnou mzdou
        full_salary_for_period = (gross_salary / Decimal('30')) * days_sick
        loss_vs_full_salary = full_salary_for_period - total_sick_leave
        loss_percentage = (loss_vs_full_salary / full_salary_for_period * 100) if full_salary_for_period > 0 else Decimal('0')
        
        return {
            'gross_salary': float(gross_salary),
            'days_sick': days_sick,
            'leave_type': leave_type,
            'leave_type_label': 'Choroba' if leave_type == 'illness' else 'Ošetrovanie člena rodiny',
            
            # DVZ výpočty
            'yearly_salary': float(yearly_salary),
            'daily_assessment_base': float(daily_assessment_base),
            'capped_daily_base': float(capped_daily_base),
            'is_capped': is_capped,
            'max_daily_base': float(cls.MAX_ASSESSMENT_BASE_DAILY),
            
            # Rozdelenie dní
            'employer_payment_days': employer_days,
            'insurance_payment_days': insurance_days,
            
            # Sadzby
            'employer_rate_percent': float(cls.EMPLOYER_RATE * 100),
            'insurance_rate_percent': float(insurance_rate * 100),
            
            # Výplaty
            'employer_payment': round(float(employer_payment), 2),
            'insurance_payment': round(float(insurance_payment), 2),
            'total_sick_leave': round(float(total_sick_leave), 2),
            'avg_daily_rate': round(float(avg_daily_rate), 2),
            
            # Porovnanie s plnou mzdou
            'full_salary_for_period': round(float(full_salary_for_period), 2),
            'loss_vs_full_salary': round(float(loss_vs_full_salary), 2),
            'loss_percentage': round(float(loss_percentage), 2),
            
            # Dodatočné info
            'explanation': cls._generate_explanation(
                employer_days, insurance_days, employer_payment, 
                insurance_payment, leave_type
            ),
            'breakdown': cls._generate_breakdown(
                days_sick, capped_daily_base, leave_type
            )
        }
    
    @classmethod
    def _generate_explanation(cls, employer_days: int, insurance_days: int,
                             employer_payment: Decimal, insurance_payment: Decimal,
                             leave_type: str) -> str:
        """Vygeneruje textové vysvetlenie výpočtu"""
        leave_label = 'chorobe' if leave_type == 'illness' else 'ošetrovaní člena rodiny'
        
        if employer_days > 0 and insurance_days > 0:
            return (
                f"Pri {leave_label} prvých {employer_days} dní platí zamestnávateľ "
                f"(1.–3. deň 25 % DVZ, 4.–{employer_days}. deň 55 % DVZ = spolu €{employer_payment:.2f}), "
                f"od {employer_days + 1}. dňa ďalších {insurance_days} dní platí Sociálna poisťovňa "
                f"(55 % DVZ = €{insurance_payment:.2f})."
            )
        elif employer_days > 0:
            return (
                f"Pri {leave_label} prvých {employer_days} dní platí zamestnávateľ "
                f"(1.–3. deň 25 %, ďalej 55 % denného vymeriavacieho základu; spolu €{employer_payment:.2f})."
            )
        else:
            return (
                f"Pri {leave_label} celých {insurance_days} dní platí Sociálna poisťovňa "
                f"55% denného vymeriavacieho základu (celkom €{insurance_payment:.2f})."
            )
    
    @classmethod
    def _generate_breakdown(cls, days_sick: int, daily_base: Decimal,
                           leave_type: str) -> list:
        """Vygeneruje denný rozpis nemocenskej podľa pravidiel SK 2026."""
        breakdown = []
        insurance_rate = cls.INSURANCE_RATE_CARE if leave_type == 'care' else cls.INSURANCE_RATE_ILLNESS

        for day in range(1, days_sick + 1):
            if leave_type != 'care' and day <= cls.EMPLOYER_TIER1_DAYS:
                payer, rate = 'Zamestnávateľ', cls.EMPLOYER_RATE          # dni 1-3: 25%
            elif leave_type != 'care' and day <= cls.EMPLOYER_PAYMENT_DAYS:
                payer, rate = 'Zamestnávateľ', cls.INSURANCE_RATE_ILLNESS  # dni 4-10: 55%
            else:
                payer, rate = 'Sociálna poisťovňa', insurance_rate        # od 11. dňa (alebo OČR)
            breakdown.append({
                'day': day,
                'payer': payer,
                'rate_percent': float(rate * 100),
                'daily_amount': round(float(daily_base * rate), 2),
            })

        return breakdown
    
    @classmethod
    def calculate_return_to_work_date(cls, start_date: str, days_sick: int) -> dict:
        """
        Vypočíta predpokladaný dátum návratu do práce.
        
        Args:
            start_date: Dátum začiatku PN (YYYY-MM-DD)
            days_sick: Počet dní PN
            
        Returns:
            dict s dátumami
        """
        from datetime import datetime, timedelta
        
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = start + timedelta(days=days_sick - 1)
        return_date = end + timedelta(days=1)
        
        return {
            'start_date': start.strftime('%Y-%m-%d'),
            'end_date': end.strftime('%Y-%m-%d'),
            'return_to_work_date': return_date.strftime('%Y-%m-%d'),
            'total_days': days_sick
        }
