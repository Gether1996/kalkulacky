# Car Leasing Calculator Service
# Lízingová kalkulačka auta - porovnanie kúpy, úveru a lízingu

from decimal import Decimal
import math
from . import config_variables as cfg

class CarLeasingCalculator:
    """
    Service pre výpočet lízingu auta a porovnanie s kúpou a úverom.
    
    Typy lízingu na Slovensku:
    - Finančný lízing (záujemca sa stáva vlastníkom na konci)
    - Operatívny lízing (auto sa vracia, alebo sa odkúpi za zostatkovou cenou)
    """
    
    # Konštanty pre 2026 - importované z config_variables
    VAT_RATE = cfg.VAT_RATE_STANDARD / 100  # 23% DPH (Slovak standard VAT rate 2026)
    DEFAULT_INTEREST_RATE = cfg.LEASING_DEFAULT_INTEREST_RATE  # 5% úrok na lízing
    DEFAULT_LOAN_RATE = cfg.LEASING_DEFAULT_LOAN_RATE  # 6% úrok na úver
    
    @classmethod
    def calculate_financial_leasing(cls, car_price: Decimal, down_payment: Decimal,
                                    lease_term_months: int, interest_rate: Decimal,
                                    include_vat: bool = True) -> dict:
        """
        Vypočíta finančný lízing (na konci sa stávate vlastníkom).
        
        Args:
            car_price: Cena auta v EUR
            down_payment: Akontácia v EUR
            lease_term_months: Doba lízingu v mesiacoch
            interest_rate: Ročná úroková sadzba (napr. 0.05 = 5%)
            include_vat: Či je cena s DPH
            
        Returns:
            dict s detailmi finančného lízingu
        """
        # Ak je cena bez DPH, pridáme DPH
        if not include_vat:
            price_with_vat = car_price * (1 + cls.VAT_RATE)
        else:
            price_with_vat = car_price
            car_price = car_price / (1 + cls.VAT_RATE)
        
        # Suma na financovanie
        financed_amount = price_with_vat - down_payment
        
        # Mesačná úroková sadzba
        monthly_rate = interest_rate / 12
        
        # Výpočet mesačnej splátky (PMT formula)
        if monthly_rate > 0:
            monthly_payment = financed_amount * (
                monthly_rate * (1 + monthly_rate) ** lease_term_months
            ) / ((1 + monthly_rate) ** lease_term_months - 1)
        else:
            monthly_payment = financed_amount / lease_term_months
        
        # Celkové náklady
        total_paid = down_payment + (monthly_payment * lease_term_months)
        total_interest = total_paid - price_with_vat
        
        return {
            'option_type': 'financial_leasing',
            'option_name': 'Finančný lízing',
            'initial_cost': round(float(down_payment), 2),
            'monthly_payment': round(float(monthly_payment), 2),
            'final_payment': 0,
            'total_cost': round(float(total_paid), 2),
            'ownership': 'Auto sa stáva vaším vlastníctvom na konci lízingu',
            'explanation': f'Finančný lízing s {lease_term_months} mesiacmi, úrok {float(interest_rate * 100):.1f}%. Celkový úrok: {round(float(total_interest), 2)} €.'
        }
    
    @classmethod
    def calculate_operational_leasing(cls, car_price: Decimal, down_payment: Decimal,
                                     lease_term_months: int, interest_rate: Decimal,
                                     residual_value_percent: Decimal = None,
                                     include_vat: bool = True) -> dict:
        """
        Vypočíta operatívny lízing (nižšie splátky, auto sa vracia alebo odkupuje).
        
        Args:
            car_price: Cena auta v EUR
            down_payment: Akontácia v EUR
            lease_term_months: Doba lízingu v mesiacoch
            interest_rate: Ročná úroková sadzba
            residual_value_percent: Zostatkková hodnota (% z ceny), default 30%
            include_vat: Či je cena s DPH
            
        Returns:
            dict s detailmi operatívneho lízingu
        """        # Use default residual value if not provided
        if residual_value_percent is None:
            residual_value_percent = cfg.LEASING_DEFAULT_RESIDUAL_VALUE
                # Ak je cena bez DPH, pridáme DPH
        if not include_vat:
            price_with_vat = car_price * (1 + cls.VAT_RATE)
        else:
            price_with_vat = car_price
            car_price = car_price / (1 + cls.VAT_RATE)
        
        # Zostatkková hodnota
        residual_value = price_with_vat * residual_value_percent
        
        # Suma na financovanie (len depreciation)
        depreciation = price_with_vat - residual_value
        financed_amount = depreciation - down_payment
        
        # Mesačná úroková sadzba
        monthly_rate = interest_rate / 12
        
        # Výpočet mesačnej splátky
        if monthly_rate > 0:
            monthly_payment = financed_amount * (
                monthly_rate * (1 + monthly_rate) ** lease_term_months
            ) / ((1 + monthly_rate) ** lease_term_months - 1)
        else:
            monthly_payment = financed_amount / lease_term_months
        
        # Celkové náklady
        total_monthly_payments = monthly_payment * lease_term_months
        total_paid_leasing = down_payment + total_monthly_payments
        
        # Scenario 1: Vrátim auto
        total_paid_return = total_paid_leasing
        
        # Scenario 2: Odkúpim auto za zostatkovou cenou
        total_paid_buyout = total_paid_leasing + residual_value
        
        return {
            'option_type': 'operational_leasing',
            'option_name': 'Operatívny lízing',
            'initial_cost': round(float(down_payment), 2),
            'monthly_payment': round(float(monthly_payment), 2),
            'final_payment': round(float(residual_value), 2),
            'total_cost': round(float(total_paid_buyout), 2),
            'ownership': f'Auto môžete odkúpiť za {round(float(residual_value), 2)} € alebo vrátiť',
            'explanation': f'Operatívny lízing s {lease_term_months} mesiacmi. Reziduálna hodnota {float(residual_value_percent * 100):.0f}%. Pri vrátení zaplatíte celkom {round(float(total_paid_return), 2)} €.'
        }
    
    @classmethod
    def calculate_loan(cls, car_price: Decimal, down_payment: Decimal,
                      loan_term_months: int, interest_rate: Decimal,
                      include_vat: bool = True) -> dict:
        """
        Vypočíta úver na auto.
        
        Args:
            car_price: Cena auta v EUR
            down_payment: Akontácia v EUR
            loan_term_months: Doba úveru v mesiacoch
            interest_rate: Ročná úroková sadzba
            include_vat: Či je cena s DPH
            
        Returns:
            dict s detailmi úveru
        """
        # Ak je cena bez DPH, pridáme DPH
        if not include_vat:
            price_with_vat = car_price * (1 + cls.VAT_RATE)
        else:
            price_with_vat = car_price
        
        # Suma úveru
        loan_amount = price_with_vat - down_payment
        
        # Mesačná úroková sadzba
        monthly_rate = interest_rate / 12
        
        # Výpočet mesačnej splátky
        if monthly_rate > 0:
            monthly_payment = loan_amount * (
                monthly_rate * (1 + monthly_rate) ** loan_term_months
            ) / ((1 + monthly_rate) ** loan_term_months - 1)
        else:
            monthly_payment = loan_amount / loan_term_months
        
        # Celkové náklady
        total_paid = down_payment + (monthly_payment * loan_term_months)
        total_interest = total_paid - price_with_vat
        
        return {
            'option_type': 'loan',
            'option_name': 'Úver',
            'initial_cost': round(float(down_payment), 2),
            'monthly_payment': round(float(monthly_payment), 2),
            'final_payment': 0,
            'total_cost': round(float(total_paid), 2),
            'ownership': 'Auto je vo vašom vlastníctve od začiatku',
            'explanation': f'Bankový úver na {loan_term_months} mesiacov s úrokom {float(interest_rate * 100):.1f}%. Celkový úrok: {round(float(total_interest), 2)} €.'
        }
    
    @classmethod
    def calculate_cash_purchase(cls, car_price: Decimal, include_vat: bool = True) -> dict:
        """
        Výpočet kúpy na hotovosti (bez financovania).
        
        Args:
            car_price: Cena auta v EUR
            include_vat: Či je cena s DPH
            
        Returns:
            dict s detailmi kúpy
        """
        if not include_vat:
            price_with_vat = car_price * (1 + cls.VAT_RATE)
        else:
            price_with_vat = car_price
        
        return {
            'option_type': 'cash',
            'option_name': 'Hotovosť',
            'initial_cost': round(float(price_with_vat), 2),
            'monthly_payment': 0,
            'final_payment': 0,
            'total_cost': round(float(price_with_vat), 2),
            'ownership': 'Auto je okamžite vo vašom vlastníctve',
            'explanation': 'Kúpa za hotovosť bez úrokov a poplatkov. Najlacnejšia možnosť ak máte dostatok financií.'
        }
    
    @classmethod
    def compare_all_options(cls, car_price: Decimal, down_payment: Decimal,
                          term_months: int, leasing_rate: Decimal = None,
                          loan_rate: Decimal = None,
                          residual_value_percent: Decimal = None,
                          include_vat: bool = True) -> dict:
        """
        Porovná všetky možnosti: kúpa, úver, finančný lízing, operatívny lízing.
        
        Returns:
            dict s porovnaním všetkých možností
        """
        if leasing_rate is None:
            leasing_rate = cls.DEFAULT_INTEREST_RATE
        if loan_rate is None:
            loan_rate = cls.DEFAULT_LOAN_RATE
        if residual_value_percent is None:
            residual_value_percent = cfg.LEASING_DEFAULT_RESIDUAL_VALUE
        
        cash = cls.calculate_cash_purchase(car_price, include_vat)
        loan = cls.calculate_loan(car_price, down_payment, term_months, loan_rate, include_vat)
        financial_leasing = cls.calculate_financial_leasing(
            car_price, down_payment, term_months, leasing_rate, include_vat
        )
        operational_leasing = cls.calculate_operational_leasing(
            car_price, down_payment, term_months, leasing_rate, residual_value_percent, include_vat
        )
        
        # Determine cheapest options
        monthly_payments = {
            'Finančný lízing': financial_leasing['monthly_payment'],
            'Operatívny lízing': operational_leasing['monthly_payment'],
            'Úver': loan['monthly_payment']
        }
        
        total_costs = {
            'Finančný lízing': financial_leasing['total_cost'],
            'Operatívny lízing': operational_leasing['total_cost'],
            'Úver': loan['total_cost'],
            'Hotovosť': cash['total_cost']
        }
        
        cheapest_monthly = min(monthly_payments, key=monthly_payments.get)
        cheapest_total = min(total_costs, key=total_costs.get)
        most_expensive = max(total_costs, key=total_costs.get)
        
        # Get car price with VAT
        if include_vat:
            price_with_vat = car_price
        else:
            price_with_vat = car_price * (1 + cls.VAT_RATE)
        
        return {
            'car_price': float(price_with_vat),
            'down_payment': float(down_payment),
            'term_months': term_months,
            'include_vat': include_vat,
            'options': {
                'financial_leasing': financial_leasing,
                'operational_leasing': operational_leasing,
                'loan': loan,
                'cash': cash
            },
            'comparison': {
                'cheapest': cheapest_total,
                'most_expensive': most_expensive,
                'cheapest_monthly': cheapest_monthly,
                'ownership_options': ['Finančný lízing', 'Úver', 'Hotovosť']
            }
        }
