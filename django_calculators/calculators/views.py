"""
API Views for Calculator Endpoints

Each calculator has a dedicated API endpoint that accepts POST requests
with calculation parameters and returns results.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from .serializers import (
    SalaryCalculatorSerializer,
    MortgageCalculatorSerializer,
    VATCalculatorSerializer,
    LoanCalculatorSerializer,
    FuelCostCalculatorSerializer,
    BMICalculatorSerializer,
    PercentageCalculatorSerializer,
    PregnancyCalculatorSerializer,
    PensionCalculatorSerializer,
    VacationCalculatorSerializer,
    EnergyCalculatorSerializer,
    BMRCalculatorSerializer,
    PaymentCalculatorSerializer,
    FreelancerTaxCalculatorSerializer,
    InflationCalculatorSerializer,
    ROICalculatorSerializer,
    HoursWorkedCalculatorSerializer,
    CalculatorListSerializer,
    UnitConverterSerializer,
    SickLeaveCalculatorSerializer,
    CarLeasingCalculatorSerializer,
    AreaVolumeCalculatorSerializer,
    SplitBillCalculatorSerializer,
    ParentalBenefitCalculatorSerializer,
    SavedCalculationSerializer,
    ScheduledNotificationSerializer,
)
from .services import (
    SalaryCalculator,
    MortgageCalculator,
    VATCalculator,
    LoanCalculator,
    FuelCostCalculator,
    BMICalculator,
    PercentageCalculator,
    PregnancyCalculator,
    PensionCalculator,
    VacationCalculator,
    EnergyCalculator,
    BMRCalculator,
    PaymentCalculator,
    FreelancerTaxCalculator,
    InflationCalculator,
    ROICalculator,
    HoursWorkedCalculator,
    UnitConverterService,
    SickLeaveCalculator,
    CarLeasingCalculator,
    AreaVolumeCalculator,
    SplitBillCalculator,
    ParentalBenefitCalculator,
)

import logging

logger = logging.getLogger('calculators')


def check_calculation_access(request, calculation):
    """
    Authorize access to a SavedCalculation. Returns a 403 ``Response`` when the
    caller is not allowed, else ``None``.

    - Owned records (``user_id`` set): only that authenticated user.
    - Anonymous records (``user_id`` is null): the caller must supply the
      matching ``session_key`` (query param on reads, request body on writes).
      This closes the IDOR where any anonymous saved calculation could be read,
      modified or deleted by enumerating integer primary keys.
    """
    user_id = getattr(request.user, 'id', None) if getattr(request, 'user', None) and request.user.is_authenticated else None

    if calculation.user_id:
        if calculation.user_id != user_id:
            return Response(
                {'success': False, 'error': 'Prístup zamietnutý'},
                status=status.HTTP_403_FORBIDDEN,
            )
        return None

    # Anonymous record — require a matching, non-empty session_key.
    supplied = request.query_params.get('session_key')
    if supplied is None:
        supplied = request.data.get('session_key') if hasattr(request, 'data') else None
    if not calculation.session_key or supplied != calculation.session_key:
        return Response(
            {'success': False, 'error': 'Prístup zamietnutý'},
            status=status.HTTP_403_FORBIDDEN,
        )
    return None


class CalculatorListView(APIView):
    """
    List all available calculators with metadata and categories.
    
    GET /api/calculators/
    """
    
    def get(self, request):
        """Return list of all available calculators organized by category"""
        categories = {
            'financial': {
                'name': 'Finančné kalkulačky',
                'slug': 'financial',
                'description': 'Kalkulačky pre úvery, hypotéky, investície a finančné výpočty',
                'calculators': [
                    {
                        'name': 'Hypotéka',
                        'slug': 'mortgage',
                        'description': 'Výpočet mesačnej splátky hypotéky',
                        'search_volume': 8000,
                        'endpoint': '/api/calculators/mortgage/',
                        'keywords': ['kalkulačka hypotéky', 'splátka hypotéky', 'hypotéka výpočet'],
                        'category': 'financial',
                        'implemented': True
                    },
                    {
                        'name': 'Úver',
                        'slug': 'loan',
                        'description': 'Výpočet splátky úveru',
                        'search_volume': 6000,
                        'endpoint': '/api/calculators/loan/',
                        'keywords': ['kalkulačka úveru', 'splátka úveru', 'úver výpočet'],
                        'category': 'financial',
                        'implemented': True
                    },
                    {
                        'name': 'Splátka',
                        'slug': 'payment',
                        'description': 'All kalkulačka splátok pre rôzne typy úverov',
                        'search_volume': 2000,
                        'endpoint': '/api/calculators/payment/',
                        'keywords': ['kalkulačka splátky', 'výpočet splátky'],
                        'category': 'financial',
                        'implemented': False
                    },
                    {
                        'name': 'ROI',
                        'slug': 'roi',
                        'description': 'Výpočet návratnosti investície',
                        'search_volume': 1000,
                        'endpoint': '/api/calculators/roi/',
                        'keywords': ['kalkulačka roi', 'návratnosť investície'],
                        'category': 'financial',
                        'implemented': False
                    },
                    {
                        'name': 'Inflácia',
                        'slug': 'inflation',
                        'description': 'Výpočet vplyvu inflácie na hodnotu peňazí',
                        'search_volume': 1500,
                        'endpoint': '/api/calculators/inflation/',
                        'keywords': ['kalkulačka inflácie', 'inflácia výpočet'],
                        'category': 'financial',
                        'implemented': False
                    },
                    {
                        'name': 'Poplatky',
                        'slug': 'fees',
                        'description': 'Výpočet poplatkov pri kúpe nehnuteľnosti',
                        'search_volume': 1000,
                        'endpoint': '/api/calculators/fees/',
                        'keywords': ['kalkulačka poplatkov', 'poplatky nehnuteľnosť'],
                        'category': 'financial',
                        'implemented': False
                    },
                ]
            },
            'taxes_salary': {
                'name': 'Dane a mzdy',
                'slug': 'taxes-salary',
                'description': 'Kalkulačky pre výpočet miezd, daní a odvodov',
                'calculators': [
                    {
                        'name': 'Čistá mzda',
                        'slug': 'salary',
                        'description': 'Výpočet čistej mzdy z hrubej mzdy',
                        'search_volume': 12000,
                        'endpoint': '/api/calculators/salary/',
                        'keywords': ['čistá mzda', 'kalkulačka mzdy', 'výpočet platu'],
                        'category': 'taxes_salary',
                        'implemented': True
                    },
                    {
                        'name': 'SZČO dane',
                        'slug': 'freelancer-tax',
                        'description': 'Výpočet daní pre SZČO',
                        'search_volume': 1500,
                        'endpoint': '/api/calculators/freelancer-tax/',
                        'keywords': ['dane szčo', 'kalkulačka szčo', 'živnostník dane'],
                        'category': 'taxes_salary',
                        'implemented': False
                    },
                    {
                        'name': 'Dovolenka',
                        'slug': 'vacation',
                        'description': 'Výpočet dovolenkových dní',
                        'search_volume': 2000,
                        'endpoint': '/api/calculators/vacation/',
                        'keywords': ['dovolenka kalkulačka', 'výpočet dovolenky'],
                        'category': 'taxes_salary',
                        'implemented': False
                    },
                    {
                        'name': 'DPH',
                        'slug': 'vat',
                        'description': 'Výpočet DPH',
                        'search_volume': 5000,
                        'endpoint': '/api/calculators/vat/',
                        'keywords': ['kalkulačka dph', 'výpočet dph', 'dph kalkulačka'],
                        'category': 'taxes_salary',
                        'implemented': True
                    },
                ]
            },
            'lifestyle': {
                'name': 'Životný štýl',
                'slug': 'lifestyle',
                'description': 'Kalkulačky pre každodenný život a cestovanie',
                'calculators': [
                    {
                        'name': 'Spotreba auta',
                        'slug': 'fuel-cost',
                        'description': 'Výpočet nákladov na palivo',
                        'search_volume': 3000,
                        'endpoint': '/api/calculators/fuel-cost/',
                        'keywords': ['spotreba auta kalkulačka', 'náklady na palivo'],
                        'category': 'lifestyle',
                        'implemented': True
                    },
                    {
                        'name': 'Renovácia',
                        'slug': 'renovation',
                        'description': 'Odhad nákladov na renováciu',
                        'search_volume': 1200,
                        'endpoint': '/api/calculators/renovation/',
                        'keywords': ['kalkulačka renovácie', 'náklady renovácia'],
                        'category': 'lifestyle',
                        'implemented': False
                    },
                    {
                        'name': 'Energia',
                        'slug': 'energy',
                        'description': 'Výpočet nákladov na elektrinu',
                        'search_volume': 2000,
                        'endpoint': '/api/calculators/energy/',
                        'keywords': ['kalkulačka energie', 'náklady elektrina'],
                        'category': 'lifestyle',
                        'implemented': False
                    },
                    {
                        'name': 'Cestovné náklady',
                        'slug': 'travel-cost',
                        'description': 'Výpočet nákladov na cestu',
                        'search_volume': 1000,
                        'endpoint': '/api/calculators/travel-cost/',
                        'keywords': ['cestovné náklady kalkulačka', 'náklady cesta'],
                        'category': 'lifestyle',
                        'implemented': False
                    },
                    {
                        'name': 'Odpracované hodiny',
                        'slug': 'hours-worked',
                        'description': 'Výpočet odpracovaných hodín a mzdy',
                        'search_volume': 800,
                        'endpoint': '/api/calculators/hours-worked/',
                        'keywords': ['odpracované hodiny kalkulačka', 'výpočet hodín'],
                        'category': 'lifestyle',
                        'implemented': False
                    },
                    {
                        'name': 'Percentá',
                        'slug': 'percentage',
                        'description': 'Výpočet percent a percent rozdielov',
                        'search_volume': 4000,
                        'endpoint': '/api/calculators/percentage/',
                        'keywords': ['kalkulačka percent', 'výpočet percent'],
                        'category': 'lifestyle',
                        'implemented': True
                    },
                ]
            },
            'health_personal': {
                'name': 'Zdravie a osobné',
                'slug': 'health-personal',
                'description': 'Kalkulačky pre zdravie, fitness a osobný život',
                'calculators': [
                    {
                        'name': 'BMI',
                        'slug': 'bmi',
                        'description': 'Výpočet indexu telesnej hmotnosti',
                        'search_volume': 10000,
                        'endpoint': '/api/calculators/bmi/',
                        'keywords': ['bmi kalkulačka', 'index telesnej hmotnosti'],
                        'category': 'health_personal',
                        'implemented': True
                    },
                    {
                        'name': 'BMR',
                        'slug': 'bmr',
                        'description': 'Výpočet bazálneho metabolizmu',
                        'search_volume': 2000,
                        'endpoint': '/api/calculators/bmr/',
                        'keywords': ['bmr kalkulačka', 'bazálny metabolizmus'],
                        'category': 'health_personal',
                        'implemented': False
                    },
                    {
                        'name': 'Tehotenstvo',
                        'slug': 'pregnancy',
                        'description': 'Výpočet termínu pôrodu',
                        'search_volume': 5000,
                        'endpoint': '/api/calculators/pregnancy/',
                        'keywords': ['kalkulačka tehotenstva', 'termín pôrodu'],
                        'category': 'health_personal',
                        'implemented': False
                    },
                    {
                        'name': 'Dôchodok',
                        'slug': 'pension',
                        'description': 'Odhad dôchodku',
                        'search_volume': 3000,
                        'endpoint': '/api/calculators/pension/',
                        'keywords': ['kalkulačka dôchodku', 'výpočet dôchodku'],
                        'category': 'health_personal',
                        'implemented': False
                    },
                ]
            }
        }
        
        # Flatten all calculators for backward compatibility
        all_calculators = []
        for category_data in categories.values():
            all_calculators.extend(category_data['calculators'])
        
        return Response({
            'count': len(all_calculators),
            'categories': categories,
            'calculators': all_calculators  # Flat list for backward compatibility
        })


class SalaryCalculatorView(APIView):
    """
    Calculate Slovak net salary from gross salary.
    
    POST /api/calculators/salary/
    
    Body:
        {
            "gross_salary": 1500.00
        }
    """
    
    def post(self, request):
        """Calculate net salary"""
        serializer = SalaryCalculatorSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            data = dict(serializer.validated_data)
            country = (data.pop('country', 'SK') or 'SK').upper()

            if country == 'SK':
                calculator = SalaryCalculator()
                result = calculator.calculate(**data)
                result.setdefault('country', 'SK')
                result.setdefault('currency', 'EUR')
            else:
                # CZ / PL / HU — structurally different payroll systems.
                from .services.salary_international import calculate_international
                data['gross_salary'] = float(data['gross_salary'])
                result = calculate_international(country, **data)

            return Response({
                'success': True,
                'data': result,
                'calculator': 'salary',
                'country': country,
                'version': '2026'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'success': False, 'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MortgageCalculatorView(APIView):
    """
    Calculate mortgage payment and amortization schedule.
    
    POST /api/calculators/mortgage/
    
    Body:
        {
            "loan_amount": 150000.00,
            "annual_interest_rate": 3.5,
            "loan_term_years": 25
        }
    """
    
    def post(self, request):
        """Calculate mortgage"""
        serializer = MortgageCalculatorSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            calculator = MortgageCalculator()
            # `country` is metadata for currency labelling, not a calc input.
            calc_kwargs = {k: v for k, v in serializer.validated_data.items() if k != 'country'}
            result = calculator.calculate(**calc_kwargs)

            return Response({
                'success': True,
                'data': result,
                'calculator': 'mortgage',
                'version': '2026'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'success': False, 'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class VATCalculatorView(APIView):
    """
    Calculate Slovak VAT (add or remove).
    
    POST /api/calculators/vat/
    
    Body:
        {
            "amount": 100.00,
            "vat_rate": 20,
            "calculation_type": "add_vat"
        }
    """
    
    def post(self, request):
        """Calculate VAT"""
        serializer = VATCalculatorSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            calculator = VATCalculator()
            result = calculator.calculate(**serializer.validated_data)
            
            return Response({
                'success': True,
                'data': result,
                'calculator': 'vat',
                'version': '2026'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'success': False, 'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LoanCalculatorView(APIView):
    """
    Calculate loan payments and amortization schedule.
    
    POST /api/calculators/loan/
    
    Body:
        {
            "loan_amount": 50000.00,
            "interest_rate": 5.5,
            "loan_years": 10,
            "include_schedule": false
        }
    """
    
    def post(self, request):
        """Calculate loan payments"""
        serializer = LoanCalculatorSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            calculator = LoanCalculator()
            result = calculator.calculate(**serializer.validated_data)
            
            return Response({
                'success': True,
                'data': result,
                'calculator': 'loan',
                'version': '2026'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'success': False, 'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class FuelCostCalculatorView(APIView):
    """
    Calculate fuel cost based on distance, consumption, and price.
    
    POST /api/calculators/fuel-cost/
    
    Body:
        {
            "distance": 350,
            "consumption": 6.5,
            "fuel_price": 1.65
        }
    """
    
    def post(self, request):
        """Calculate fuel cost"""
        serializer = FuelCostCalculatorSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            calculator = FuelCostCalculator()
            result = calculator.calculate(**serializer.validated_data)
            
            return Response({
                'success': True,
                'data': result,
                'calculator': 'fuel-cost',
                'version': '2026'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'success': False, 'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class BMICalculatorView(APIView):
    """
    Calculate BMI (Body Mass Index) and health category.
    
    POST /api/calculators/bmi/
    
    Body:
        {
            "weight": 75,
            "height": 180
        }
    """
    
    def post(self, request):
        """Calculate BMI"""
        serializer = BMICalculatorSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            calculator = BMICalculator()
            result = calculator.calculate(**serializer.validated_data)
            
            return Response({
                'success': True,
                'data': result,
                'calculator': 'bmi',
                'version': '2026'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'success': False, 'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PercentageCalculatorView(APIView):
    """
    Calculate percentages (various operations).
    
    POST /api/calculators/percentage/
    
    Body:
        {
            "calculation_type": "percent_of",
            "percent": 20,
            "value2": 150
        }
    """
    
    def post(self, request):
        """Calculate percentage"""
        serializer = PercentageCalculatorSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            calculator = PercentageCalculator()
            result = calculator.calculate(**serializer.validated_data)
            
            return Response({
                'success': True,
                'data': result,
                'calculator': 'percentage',
                'version': '2026'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'success': False, 'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PregnancyCalculatorView(APIView):
    """
    Calculate pregnancy due date, weeks, and trimester information.
    
    POST /api/calculators/pregnancy/
    
    Body (from LMP):
        {
            "calculation_method": "lmp",
            "lmp_date": "2024-01-01"
        }
    
    Body (from conception):
        {
            "calculation_method": "conception",
            "conception_date": "2024-01-15"
        }
    """
    
    def post(self, request):
        """Calculate pregnancy dates and information"""
        serializer = PregnancyCalculatorSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            calculator = PregnancyCalculator()
            result = calculator.calculate(**serializer.validated_data)
            
            return Response({
                'success': True,
                'data': result,
                'calculator': 'pregnancy',
                'version': '2026'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'success': False, 'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PensionCalculatorView(APIView):
    """
    Calculate pension estimates and contributions.
    
    POST /api/calculators/pension/
    
    Body:
        {
            "current_age": 35,
            "gross_salary": 1500,
            "years_worked": 12,
            "gender": "male",
            "include_second_pillar": true
        }
    """
    
    def post(self, request):
        """Calculate pension estimates"""
        serializer = PensionCalculatorSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            data = dict(serializer.validated_data)
            country = (data.pop('country', 'SK') or 'SK').upper()
            if country == 'CZ':
                from .services.international_benefits import calculate_cz_pension
                result = calculate_cz_pension(**data)
            else:
                result = PensionCalculator().calculate(**data)
                result.setdefault('country', 'SK')
                result.setdefault('currency', 'EUR')

            return Response({
                'success': True,
                'data': result,
                'calculator': 'pension',
                'country': country,
                'version': '2026'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'success': False, 'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class VacationCalculatorView(APIView):
    """
    Calculate vacation days entitlement based on Slovak labor law.
    
    POST /api/calculators/vacation/
    
    Body:
        {
            "age": 35,
            "employment_start_date": "2020-05-01",
            "vacation_days_used": 8,
            "days_carried_over": 3
        }
    """
    
    def post(self, request):
        """Calculate vacation days"""
        serializer = VacationCalculatorSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            data = dict(serializer.validated_data)
            country = (data.pop('country', 'SK') or 'SK').upper()
            if country == 'CZ':
                from .services.international_benefits import calculate_cz_vacation
                result = calculate_cz_vacation(**data)
            else:
                result = VacationCalculator().calculate(**data)
                result.setdefault('country', 'SK')
                result.setdefault('currency', 'EUR')

            return Response({
                'success': True,
                'data': result,
                'calculator': 'vacation',
                'country': country,
                'version': '2026'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'success': False, 'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class EnergyCalculatorView(APIView):
    """
    Energy Cost Calculator - Calculate electricity and gas costs
    
    POST /api/calculators/energy/
    
    Body:
        {
            "electricity_consumption": 300,
            "gas_consumption": 600,
            "household_size": 3,
            "has_dual_tariff": true
        }
    """
    
    def post(self, request):
        """Calculate energy costs"""
        serializer = EnergyCalculatorSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            calculator = EnergyCalculator()
            result = calculator.calculate(**serializer.validated_data)
            
            return Response({
                'success': True,
                'data': result,
                'calculator': 'energy',
                'version': '2026'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'success': False, 'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class BMRCalculatorView(APIView):
    """
    BMR (Basal Metabolic Rate) Calculator - Calculate daily caloric needs
    
    POST /api/calculators/bmr/
    
    Body:
        {
            "weight": 75,
            "height": 175,
            "age": 30,
            "gender": "male",
            "activity_level": "moderate",
            "weight_goal": "lose_moderate"
        }
    """
    
    def post(self, request):
        """Calculate BMR and caloric needs"""
        serializer = BMRCalculatorSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            calculator = BMRCalculator()
            result = calculator.calculate(**serializer.validated_data)
            
            return Response({
                'success': True,
                'data': result,
                'calculator': 'bmr',
                'version': '2026'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'success': False, 'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PaymentCalculatorView(APIView):
    """
    Payment Calculator - Calculate loan installment payments
    
    POST /api/calculators/payment/
    
    Body:
        {
            "loan_amount": 50000,
            "annual_interest_rate": 5.5,
            "loan_term_years": 10,
            "payment_frequency": "monthly"
        }
    """
    
    def post(self, request):
        """Calculate loan payments"""
        serializer = PaymentCalculatorSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            calculator = PaymentCalculator()
            result = calculator.calculate(**serializer.validated_data)
            
            return Response({
                'success': True,
                'data': result,
                'calculator': 'payment',
                'version': '2026'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'success': False, 'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class FreelancerTaxCalculatorView(APIView):
    """
    Freelancer Tax Calculator - Calculate taxes and contributions for self-employed (SZČO)
    
    POST /api/calculators/freelancer-tax/
    
    Body:
        {
            "annual_revenue": 30000,
            "use_flat_expenses": true,
            "include_sickness": true,
            "months_active": 12
        }
    """
    
    def post(self, request):
        """Calculate freelancer taxes and contributions"""
        serializer = FreelancerTaxCalculatorSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            data = dict(serializer.validated_data)
            country = (data.pop('country', 'SK') or 'SK').upper()

            if country == 'CZ':
                from .services.freelancer_international import calculate_cz_freelancer
                data['annual_revenue'] = float(data['annual_revenue'])
                if data.get('annual_expenses') is not None:
                    data['annual_expenses'] = float(data['annual_expenses'])
                result = calculate_cz_freelancer(**data)
            else:
                calculator = FreelancerTaxCalculator()
                result = calculator.calculate(**data)
                result.setdefault('country', 'SK')
                result.setdefault('currency', 'EUR')

            return Response({
                'success': True,
                'data': result,
                'calculator': 'freelancer_tax',
                'country': country,
                'version': '2026'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'success': False, 'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class InflationCalculatorView(APIView):
    """
    Inflation Calculator - Calculate real value of money over time
    
    POST /api/calculators/inflation/
    
    Body:
        {
            "present_value": 10000,
            "years": 10,
            "inflation_rate": 3.0,
            "calculate_reverse": false
        }
    """
    
    def post(self, request):
        """Calculate inflation impact"""
        serializer = InflationCalculatorSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            calculator = InflationCalculator()
            result = calculator.calculate(**serializer.validated_data)
            
            return Response({
                'success': True,
                'data': result,
                'calculator': 'inflation',
                'version': '2026'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'success': False, 'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ROICalculatorView(APIView):
    """
    ROI Calculator - Calculate return on investment
    
    POST /api/calculators/roi/
    
    Body:
        {
            "initial_investment": 10000,
            "final_value": 15000,
            "additional_costs": 500,
            "investment_period_months": 24
        }
    """
    
    def post(self, request):
        """Calculate ROI"""
        serializer = ROICalculatorSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            calculator = ROICalculator()
            result = calculator.calculate(**serializer.validated_data)
            
            return Response({
                'success': True,
                'data': result,
                'calculator': 'roi',
                'version': '2026'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'success': False, 'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class HoursWorkedCalculatorView(APIView):
    """
    Hours Worked Calculator - Calculate work hours and overtime
    
    POST /api/calculators/hours-worked/
    
    Body:
        {
            "hours_worked": 48,
            "hourly_rate": 12.50,
            "period_type": "weekly"
        }
    """
    
    def post(self, request):
        """Calculate hours worked and earnings"""
        serializer = HoursWorkedCalculatorSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            calculator = HoursWorkedCalculator()
            result = calculator.calculate(**serializer.validated_data)
            
            return Response({
                'success': True,
                'data': result,
                'calculator': 'hours_worked',
                'version': '2026'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'success': False, 'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class HealthCheckView(APIView):
    """
    Health check endpoint to verify API is running.

    GET /api/health/
    """
    throttle_classes = []  # never throttle load-balancer / uptime probes

    def get(self, request):
        """Return API health status"""
        return Response({
            'status': 'healthy',
            'api_version': '1.0',
            'year': 2026,
            'calculators_available': 7
        })


# Blog Views

from rest_framework import generics, filters
from datetime import datetime
from .models import BlogCategory, BlogPost
from .serializers import (
    BlogCategorySerializer,
    BlogPostListSerializer,
    BlogPostDetailSerializer,
)


class BlogCategoryListView(generics.ListAPIView):
    """
    List all blog categories.
    
    GET /api/blog/categories/
    """
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer


class BlogPostListView(generics.ListAPIView):
    """
    List all published blog posts with filtering.
    
    GET /api/blog/posts/
    GET /api/blog/posts/?category=dane-2026
    GET /api/blog/posts/?calculator=salary
    GET /api/blog/posts/?search=progresívne zdanenie
    """
    serializer_class = BlogPostListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'excerpt', 'content_html', 'tags']
    
    def get_queryset(self):
        queryset = BlogPost.objects.filter(
            status='published',
            published_at__lte=datetime.now()
        )
        
        # Filter by category slug
        category_slug = self.request.query_params.get('category', None)
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Filter by related calculator
        calculator = self.request.query_params.get('calculator', None)
        if calculator:
            queryset = queryset.filter(related_calculator=calculator)
        
        # Filter by tag
        tag = self.request.query_params.get('tag', None)
        if tag:
            queryset = queryset.filter(tags__icontains=tag)
        
        return queryset


class BlogPostDetailView(APIView):
    """
    Get a single blog post by slug.
    
    GET /api/blog/posts/<slug>/
    """
    
    def get(self, request, slug):
        try:
            post = BlogPost.objects.get(slug=slug, status='published')
            
            # Increment view count
            post.increment_views()
            
            serializer = BlogPostDetailSerializer(post)
            return Response({
                'success': True,
                'data': serializer.data
            })
        except BlogPost.DoesNotExist:
            return Response(
                {'success': False, 'error': 'Blog post not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class FeaturedBlogPostsView(generics.ListAPIView):
    """
    Get featured/latest blog posts.
    
    GET /api/blog/featured/
    """
    serializer_class = BlogPostListSerializer
    
    def get_queryset(self):
        return BlogPost.objects.filter(
            status='published',
            published_at__lte=datetime.now()
        ).order_by('-published_at')[:5]


class UnitConverterView(APIView):
    """
    Unit Converter API - Konvertor jednotiek
    
    POST /api/calculators/unit-converter/
    Body: {
        "value": 100,
        "from_unit": "meter",
        "to_unit": "kilometer",
        "category": "length"
    }
    """
    
    def post(self, request):
        serializer = UnitConverterSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'success': False, 'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            result = UnitConverterService.convert(
                value=serializer.validated_data['value'],
                from_unit=serializer.validated_data['from_unit'],
                to_unit=serializer.validated_data['to_unit'],
                category=serializer.validated_data['category']
            )
            
            return Response({
                'success': True,
                'data': result
            })
        
        except ValueError as e:
            return Response(
                {'success': False, 'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'success': False, 'error': f'Chyba pri výpočte: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UnitConverterCategoriesView(APIView):
    """
    Get available categories for unit converter
    
    GET /api/calculators/unit-converter/categories/
    """
    
    def get(self, request):
        return Response({
            'success': True,
            'data': UnitConverterService.get_categories()
        })


class UnitConverterUnitsView(APIView):
    """
    Get available units for a specific category
    
    GET /api/calculators/unit-converter/units/?category=length
    """
    
    def get(self, request):
        category = request.query_params.get('category', None)
        
        if not category:
            return Response(
                {'success': False, 'error': 'Parameter "category" je povinný'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        units = UnitConverterService.get_available_units(category)
        
        if not units:
            return Response(
                {'success': False, 'error': f'Neplatná kategória: {category}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response({
            'success': True,
            'data': units
        })


class SickLeaveCalculatorView(APIView):
    """
    Sick Leave Calculator API - Kalkulačka pracovnej neschopnosti (PN)
    
    POST /api/calculators/sick-leave/
    Body: {
        "gross_salary": 1500,
        "days_sick": 10,
        "leave_type": "illness"
    }
    """
    
    def post(self, request):
        serializer = SickLeaveCalculatorSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'success': False, 'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from decimal import Decimal
            vd = serializer.validated_data
            country = (vd.get('country', 'SK') or 'SK').upper()
            if country == 'CZ':
                from .services.international_benefits import calculate_cz_sick_leave
                result = calculate_cz_sick_leave(
                    gross_salary=float(vd['gross_salary']),
                    days_sick=vd['days_sick'],
                    leave_type=vd.get('leave_type', 'illness'),
                )
            else:
                result = SickLeaveCalculator.calculate_sick_leave(
                    gross_salary=Decimal(str(vd['gross_salary'])),
                    days_sick=vd['days_sick'],
                    leave_type=vd.get('leave_type', 'illness')
                )
                result.setdefault('country', 'SK')
                result.setdefault('currency', 'EUR')

            return Response({
                'success': True,
                'data': result
            })
        
        except ValueError as e:
            return Response(
                {'success': False, 'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'success': False, 'error': f'Chyba pri výpočte nemocenskej: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CarLeasingCalculatorView(APIView):
    """
    Car Leasing Calculator API - Porovnanie kúpy, úveru a lízingu
    
    POST /api/calculators/car-leasing/
    Body: {
        "car_price": 25000,
        "down_payment": 5000,
        "term_months": 60,
        "leasing_rate": 5.0,
        "loan_rate": 6.0,
        "residual_value_percent": 30,
        "include_vat": true
    }
    """
    
    def post(self, request):
        serializer = CarLeasingCalculatorSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'success': False, 'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from decimal import Decimal
            
            car_price = Decimal(str(serializer.validated_data['car_price']))
            down_payment = Decimal(str(serializer.validated_data['down_payment']))
            term_months = serializer.validated_data['term_months']
            
            leasing_rate = serializer.validated_data.get('leasing_rate')
            if leasing_rate:
                leasing_rate = Decimal(str(leasing_rate)) / 100
            
            loan_rate = serializer.validated_data.get('loan_rate')
            if loan_rate:
                loan_rate = Decimal(str(loan_rate)) / 100
            
            residual_value_percent = Decimal(str(serializer.validated_data.get('residual_value_percent', 30))) / 100
            include_vat = serializer.validated_data.get('include_vat', True)
            
            result = CarLeasingCalculator.compare_all_options(
                car_price=car_price,
                down_payment=down_payment,
                term_months=term_months,
                leasing_rate=leasing_rate,
                loan_rate=loan_rate,
                residual_value_percent=residual_value_percent,
                include_vat=include_vat
            )
            
            return Response({
                'success': True,
                'data': result
            })
        
        except ValueError as e:
            return Response(
                {'success': False, 'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'success': False, 'error': f'Chyba pri výpočte lízingu: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AreaVolumeCalculatorView(APIView):
    """
    Area & Volume Calculator API - Výpočet plochy a objemu
    
    POST /api/calculators/area-volume/
    Body: {
        "shape": "rectangle",
        "dimensions": {"length": 5, "width": 3}
    }
    """
    
    def post(self, request):
        serializer = AreaVolumeCalculatorSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'success': False, 'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            result = AreaVolumeCalculator.calculate(
                shape=serializer.validated_data['shape'],
                dimensions=serializer.validated_data['dimensions']
            )
            
            return Response({
                'success': True,
                'data': result
            })
        
        except ValueError as e:
            return Response(
                {'success': False, 'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'success': False, 'error': f'Chyba pri výpočte: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AreaVolumeShapesView(APIView):
    """
    Get available shapes for area/volume calculator
    
    GET /api/calculators/area-volume/shapes/
    """
    
    def get(self, request):
        return Response({
            'success': True,
            'data': AreaVolumeCalculator.get_available_shapes()
        })


class SplitBillCalculatorView(APIView):
    """
    Split Bill Calculator API - Rozdelenie účtu
    
    POST /api/calculators/split-bill/
    Body: {
        "split_type": "equal",
        "total_amount": 100,
        "num_people": 4,
        "tip_percent": 15
    }
    """
    
    def post(self, request):
        serializer = SplitBillCalculatorSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'success': False, 'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from decimal import Decimal
            
            split_type = serializer.validated_data['split_type']
            total_amount = Decimal(str(serializer.validated_data['total_amount']))
            tip_percent = Decimal(str(serializer.validated_data.get('tip_percent', 0)))
            
            if split_type == 'equal':
                num_people = serializer.validated_data['num_people']
                result = SplitBillCalculator.split_equally(
                    total_amount=total_amount,
                    num_people=num_people,
                    tip_percent=tip_percent
                )
            
            elif split_type == 'by_items':
                items = serializer.validated_data['items']
                result = SplitBillCalculator.split_by_items(
                    items=items,
                    tip_percent=tip_percent
                )
            
            elif split_type == 'custom':
                custom_amounts = serializer.validated_data['custom_amounts']
                result = SplitBillCalculator.split_custom(
                    total_amount=total_amount,
                    custom_amounts=custom_amounts,
                    tip_percent=tip_percent
                )
            
            return Response({
                'success': True,
                'data': result
            })
        
        except ValueError as e:
            return Response(
                {'success': False, 'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'success': False, 'error': f'Chyba pri výpočte: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TipSuggestionsView(APIView):
    """
    Get tip suggestions for an amount
    
    GET /api/calculators/split-bill/tip-suggestions/?amount=100
    """
    
    def get(self, request):
        amount_str = request.query_params.get('amount', None)
        
        if not amount_str:
            return Response(
                {'success': False, 'error': 'Parameter "amount" je povinný'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from decimal import Decimal
            amount = Decimal(amount_str)
            
            result = SplitBillCalculator.get_tip_suggestions(amount)
            
            return Response({
                'success': True,
                'data': result
            })
        except Exception as e:
            return Response(
                {'success': False, 'error': f'Neplatná suma: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )


class ParentalBenefitCalculatorView(APIView):
    """
    Parental Benefit Calculator API Endpoint.
    Rodičovský príspevok - Materské a rodičovské dávky.
    
    POST /api/calculators/parental-benefit/
    
    Calculates:
    - Maternity benefit (Materské) - 70% of daily assessment base for 34/43 weeks
    - Parental benefit basic (Osnova) - €381.90/month for 3 years
    - Parental benefit alternative (Alternatíva) - €270/month for 6 years
    - Timeline planning and expiration dates
    - Work compatibility check
    """
    
    def post(self, request):
        serializer = ParentalBenefitCalculatorSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'success': False, 'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            data = dict(serializer.validated_data)
            country = (data.pop('country', 'SK') or 'SK').upper()
            if country == 'CZ':
                from .services.international_benefits import calculate_cz_parental
                # CZ engine accepts birth_date, gross_salary, twins_or_more, current_date.
                result = calculate_cz_parental(
                    birth_date=data.get('birth_date'),
                    gross_salary=data.get('gross_salary'),
                    twins_or_more=data.get('twins_or_more', False),
                    current_date=data.get('current_date'),
                )
            else:
                result = ParentalBenefitCalculator().calculate(**data)
                result.setdefault('country', 'SK')
                result.setdefault('currency', 'EUR')

            return Response({
                'success': True,
                'data': result
            })
        
        except ValueError as e:
            return Response(
                {'success': False, 'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'success': False, 'error': f'Chyba pri výpočte rodičovského príspevku: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ============================================================================
# SAVED CALCULATIONS & NOTIFICATIONS VIEWS
# ============================================================================

class SavedCalculationViewSet(APIView):
    """
    API endpoints for Saved Calculations.
    Supports anonymous users via session_key.
    
    GET /api/saved-calculations/?session_key=XXX
    POST /api/saved-calculations/
    PUT /api/saved-calculations/{id}/
    DELETE /api/saved-calculations/{id}/
    """
    
    def get(self, request):
        """List saved calculations — for the logged-in user, or by session_key."""
        from calculators.models import SavedCalculation

        if request.user and request.user.is_authenticated:
            calculations = SavedCalculation.objects.filter(user=request.user)
        else:
            session_key = request.query_params.get('session_key')
            if not session_key:
                return Response(
                    {'success': False, 'error': 'session_key je povinný parameter'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            calculations = SavedCalculation.objects.filter(session_key=session_key)

        serializer = SavedCalculationSerializer(calculations, many=True)
        return Response({
            'success': True,
            'data': serializer.data,
            'count': calculations.count()
        })

    def post(self, request):
        """Create a new saved calculation"""
        serializer = SavedCalculationSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {'success': False, 'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Attach the owner when the request is authenticated so it shows in
            # their dashboard; anonymous saves fall back to session_key.
            owner = request.user if (request.user and request.user.is_authenticated) else None
            calculation = serializer.save(user=owner)
            
            # Generate notifications if tracking is enabled
            if calculation.is_tracking:
                self._generate_notifications(calculation)
            
            return Response({
                'success': True,
                'data': SavedCalculationSerializer(calculation).data
            }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response(
                {'success': False, 'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def _generate_notifications(self, calculation):
        """Generate scheduled notifications based on calculator type"""
        from calculators.services.notification_generator import NotificationGenerator
        
        try:
            NotificationGenerator.generate_for_calculation(calculation)
        except Exception as e:
            logger.error("Error generating notifications: %s", e)


class SavedCalculationDetailView(APIView):
    """
    Detail view for a single saved calculation.
    
    GET /api/saved-calculations/{id}/
    PUT /api/saved-calculations/{id}/
    DELETE /api/saved-calculations/{id}/
    """
    
    def get(self, request, pk):
        """Retrieve a single saved calculation (owner-scoped)."""
        try:
            from calculators.models import SavedCalculation
            calculation = SavedCalculation.objects.get(pk=pk)

            denied = check_calculation_access(request, calculation)
            if denied:
                return denied

            # Increment access counter
            calculation.increment_access()

            return Response({
                'success': True,
                'data': SavedCalculationSerializer(calculation).data
            })
        except SavedCalculation.DoesNotExist:
            return Response(
                {'success': False, 'error': 'Výpočet nebol nájdený'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    def put(self, request, pk):
        """Update a saved calculation"""
        try:
            from calculators.models import SavedCalculation
            calculation = SavedCalculation.objects.get(pk=pk)

            denied = check_calculation_access(request, calculation)
            if denied:
                return denied

            serializer = SavedCalculationSerializer(calculation, data=request.data, partial=True)
            if not serializer.is_valid():
                return Response(
                    {'success': False, 'errors': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            calculation = serializer.save()
            
            # Regenerate notifications if tracking status changed
            if 'is_tracking' in request.data:
                from calculators.models import ScheduledNotification
                # Delete old notifications
                ScheduledNotification.objects.filter(calculation=calculation, sent=False).delete()
                
                if calculation.is_tracking:
                    from calculators.services.notification_generator import NotificationGenerator
                    NotificationGenerator.generate_for_calculation(calculation)
            
            return Response({
                'success': True,
                'data': SavedCalculationSerializer(calculation).data
            })
        
        except SavedCalculation.DoesNotExist:
            return Response(
                {'success': False, 'error': 'Výpočet nebol nájdený'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'success': False, 'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def delete(self, request, pk):
        """Delete a saved calculation"""
        try:
            from calculators.models import SavedCalculation
            calculation = SavedCalculation.objects.get(pk=pk)

            denied = check_calculation_access(request, calculation)
            if denied:
                return denied

            calculation.delete()
            
            return Response({
                'success': True,
                'message': 'Výpočet bol úspešne odstránený'
            })
        except SavedCalculation.DoesNotExist:
            return Response(
                {'success': False, 'error': 'Výpočet nebol nájdený'},
                status=status.HTTP_404_NOT_FOUND
            )


class NotificationListView(APIView):
    """
    List notifications for a saved calculation.
    
    GET /api/saved-calculations/{calculation_id}/notifications/
    """
    
    def get(self, request, calculation_id):
        """List all notifications for a calculation"""
        try:
            from calculators.models import SavedCalculation, ScheduledNotification
            calculation = SavedCalculation.objects.get(pk=calculation_id)

            denied = check_calculation_access(request, calculation)
            if denied:
                return denied

            notifications = ScheduledNotification.objects.filter(calculation=calculation)
            
            serializer = ScheduledNotificationSerializer(notifications, many=True)
            return Response({
                'success': True,
                'data': serializer.data,
                'count': notifications.count()
            })
        except SavedCalculation.DoesNotExist:
            return Response(
                {'success': False, 'error': 'Výpočet nebol nájdený'},
                status=status.HTTP_404_NOT_FOUND
            )


class MyDashboardView(APIView):
    """
    Aggregated dashboard payload for the logged-in user: their saved
    calculations, upcoming (unsent) reminders and summary stats.

    GET /api/calculators/my/dashboard/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from datetime import date
        from calculators.models import SavedCalculation, ScheduledNotification

        calculations = SavedCalculation.objects.filter(user=request.user)
        calc_data = SavedCalculationSerializer(calculations, many=True).data

        upcoming = (
            ScheduledNotification.objects
            .filter(calculation__user=request.user, sent=False,
                    scheduled_date__gte=date.today())
            .order_by('scheduled_date', 'scheduled_time')[:10]
        )
        upcoming_data = ScheduledNotificationSerializer(upcoming, many=True).data

        from calculators.models import UserReminder
        from .serializers import UserReminderSerializer
        reminders = (
            UserReminder.objects
            .filter(user=request.user, sent=False, remind_date__gte=date.today())
            .order_by('remind_date', 'remind_time')
        )
        reminders_data = UserReminderSerializer(reminders, many=True).data

        from calculators.models import SavingsGoal
        from .serializers import SavingsGoalSerializer
        goals = (SavingsGoal.objects
                 .filter(user=request.user)
                 .prefetch_related('contributions'))
        goals_data = SavingsGoalSerializer(goals, many=True).data
        active_goals = sum(
            1 for g in goals_data if g['progress']['status'] != 'reached'
        )

        stats = {
            'totalCalculations': calculations.count(),
            'trackedCalculations': calculations.filter(is_tracking=True).count(),
            'favoritesCount': calculations.filter(is_favorite=True).count(),
            'upcomingNotifications': upcoming.count() + reminders.count(),
            'activeSavingsGoals': active_goals,
        }

        return Response({
            'success': True,
            'stats': stats,
            'calculations': calc_data,
            'upcomingNotifications': upcoming_data,
            'reminders': reminders_data,
            'savingsGoals': goals_data,
        })


class UserReminderListCreateView(APIView):
    """
    List / create the logged-in user's custom reminders.
    GET  /api/calculators/my/reminders/
    POST /api/calculators/my/reminders/  { title, remind_date, note?, category?, ... }
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from calculators.models import UserReminder
        from .serializers import UserReminderSerializer
        qs = UserReminder.objects.filter(user=request.user).order_by('remind_date', 'remind_time')
        return Response({'success': True, 'data': UserReminderSerializer(qs, many=True).data})

    def post(self, request):
        from .serializers import UserReminderSerializer
        serializer = UserReminderSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'success': False, 'errors': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        reminder = serializer.save(user=request.user)
        return Response({'success': True, 'data': UserReminderSerializer(reminder).data},
                        status=status.HTTP_201_CREATED)


class UserReminderDetailView(APIView):
    """
    Update / delete a single reminder (owner only).
    PATCH/DELETE /api/calculators/my/reminders/<pk>/
    """
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        from calculators.models import UserReminder
        from .serializers import UserReminderSerializer
        reminder = UserReminder.objects.filter(pk=pk, user=request.user).first()
        if not reminder:
            return Response({'success': False}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserReminderSerializer(reminder, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'success': True, 'data': serializer.data})

    def delete(self, request, pk):
        from calculators.models import UserReminder
        deleted, _ = UserReminder.objects.filter(pk=pk, user=request.user).delete()
        if not deleted:
            return Response({'success': False}, status=status.HTTP_404_NOT_FOUND)
        return Response({'success': True})


# ============================================================================
# SAVINGS GOAL — public calculator + logged-in progress tracker
# ============================================================================

class SavingsGoalCalculatorView(APIView):
    """
    Public savings-goal projection (no login required).

    POST /api/calculators/savings-goal/
      mode='time'    { target_amount, initial_amount?, monthly_contribution, annual_rate?, currency? }
      mode='monthly' { target_amount, initial_amount?, months, annual_rate?, currency? }
    """
    permission_classes = [AllowAny]

    def post(self, request):
        from .serializers import SavingsGoalCalculatorSerializer
        from .services.savings_goal_calculator import (
            project_time_to_goal, required_monthly_contribution,
        )
        serializer = SavingsGoalCalculatorSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'success': False, 'errors': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        d = serializer.validated_data

        if d['mode'] == 'monthly':
            result = required_monthly_contribution(
                d['target_amount'], d.get('initial_amount', 0),
                d['months'], d.get('annual_rate', 0),
            )
        else:
            result = project_time_to_goal(
                d['target_amount'], d.get('initial_amount', 0),
                d.get('monthly_contribution', 0), d.get('annual_rate', 0),
            )

        return Response({
            'success': True,
            'mode': d['mode'],
            'currency': d.get('currency', 'EUR'),
            'result': result,
        })


class SavingsGoalListCreateView(APIView):
    """
    List / create the logged-in user's savings goals (with progress + status).
    GET  /api/calculators/my/savings-goals/
    POST /api/calculators/my/savings-goals/  { name, target_amount, ... }
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from calculators.models import SavingsGoal
        from .serializers import SavingsGoalSerializer
        qs = (SavingsGoal.objects
              .filter(user=request.user)
              .prefetch_related('contributions'))
        data = SavingsGoalSerializer(qs, many=True).data
        return Response({'success': True, 'data': data})

    def post(self, request):
        from .serializers import SavingsGoalSerializer
        serializer = SavingsGoalSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'success': False, 'errors': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        goal = serializer.save(user=request.user)
        return Response({'success': True, 'data': SavingsGoalSerializer(goal).data},
                        status=status.HTTP_201_CREATED)


class SavingsGoalDetailView(APIView):
    """
    Update / delete a single savings goal (owner only).
    PATCH/DELETE /api/calculators/my/savings-goals/<pk>/
    """
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        from calculators.models import SavingsGoal
        from .serializers import SavingsGoalSerializer
        goal = SavingsGoal.objects.filter(pk=pk, user=request.user).first()
        if not goal:
            return Response({'success': False}, status=status.HTTP_404_NOT_FOUND)
        serializer = SavingsGoalSerializer(goal, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'success': True, 'data': serializer.data})

    def delete(self, request, pk):
        from calculators.models import SavingsGoal
        deleted, _ = SavingsGoal.objects.filter(pk=pk, user=request.user).delete()
        if not deleted:
            return Response({'success': False}, status=status.HTTP_404_NOT_FOUND)
        return Response({'success': True})


class SavingsContributionCreateView(APIView):
    """
    Log a contribution (deposit) against a savings goal, advancing its progress.
    POST /api/calculators/my/savings-goals/<goal_id>/contributions/
      { amount, date, note? }
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, goal_id):
        from calculators.models import SavingsGoal
        from .serializers import SavingsContributionSerializer, SavingsGoalSerializer
        goal = SavingsGoal.objects.filter(pk=goal_id, user=request.user).first()
        if not goal:
            return Response({'success': False}, status=status.HTTP_404_NOT_FOUND)
        serializer = SavingsContributionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'success': False, 'errors': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer.save(goal=goal)
        # Return the refreshed goal so the UI can update progress in one round-trip.
        goal.refresh_from_db()
        return Response({'success': True, 'data': SavingsGoalSerializer(goal).data},
                        status=status.HTTP_201_CREATED)


class SavingsContributionDeleteView(APIView):
    """
    Remove a logged contribution (owner only).
    DELETE /api/calculators/my/savings-goals/<goal_id>/contributions/<pk>/
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, goal_id, pk):
        from calculators.models import SavingsContribution
        deleted, _ = SavingsContribution.objects.filter(
            pk=pk, goal_id=goal_id, goal__user=request.user,
        ).delete()
        if not deleted:
            return Response({'success': False}, status=status.HTTP_404_NOT_FOUND)
        return Response({'success': True})


# ============================================================================
# FAVORITE CALCULATORS — per-user pinned tools with custom order
# ============================================================================

class FavoriteListCreateView(APIView):
    """
    GET  /api/calculators/my/favorites/            -> the user's pinned tools (ordered)
    POST /api/calculators/my/favorites/  { calculator_id }  -> pin a tool (appended)
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from calculators.models import FavoriteCalculator
        from .serializers import FavoriteCalculatorSerializer
        qs = FavoriteCalculator.objects.filter(user=request.user)
        return Response({'success': True, 'data': FavoriteCalculatorSerializer(qs, many=True).data})

    def post(self, request):
        from django.db.models import Max
        from calculators.models import FavoriteCalculator
        from .serializers import FavoriteCalculatorSerializer
        serializer = FavoriteCalculatorSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'success': False, 'errors': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        calc_id = serializer.validated_data['calculator_id']
        # Idempotent: pinning an already-pinned tool just returns it.
        existing = FavoriteCalculator.objects.filter(user=request.user, calculator_id=calc_id).first()
        if existing:
            return Response({'success': True, 'data': FavoriteCalculatorSerializer(existing).data},
                            status=status.HTTP_200_OK)
        next_order = (FavoriteCalculator.objects.filter(user=request.user)
                      .aggregate(m=Max('order'))['m'] or 0) + 1
        fav = FavoriteCalculator.objects.create(
            user=request.user, calculator_id=calc_id, order=next_order)
        return Response({'success': True, 'data': FavoriteCalculatorSerializer(fav).data},
                        status=status.HTTP_201_CREATED)


class FavoriteReorderView(APIView):
    """
    POST /api/calculators/my/favorites/reorder/  { order: ["salary","bmi", ...] }
    Persists the user's preferred ordering of their pinned tools.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        from calculators.models import FavoriteCalculator
        from .serializers import FavoriteCalculatorSerializer
        order = request.data.get('order')
        if not isinstance(order, list):
            return Response({'success': False, 'error': 'order musí byť zoznam.'},
                            status=status.HTTP_400_BAD_REQUEST)
        favs = {f.calculator_id: f for f in FavoriteCalculator.objects.filter(user=request.user)}
        to_update = []
        for idx, calc_id in enumerate(order):
            f = favs.get(calc_id)
            if f and f.order != idx:
                f.order = idx
                to_update.append(f)
        if to_update:
            FavoriteCalculator.objects.bulk_update(to_update, ['order'])
        qs = FavoriteCalculator.objects.filter(user=request.user)
        return Response({'success': True, 'data': FavoriteCalculatorSerializer(qs, many=True).data})


class FavoriteDeleteView(APIView):
    """DELETE /api/calculators/my/favorites/<calculator_id>/  -> unpin a tool."""
    permission_classes = [IsAuthenticated]

    def delete(self, request, calculator_id):
        from calculators.models import FavoriteCalculator
        deleted, _ = FavoriteCalculator.objects.filter(
            user=request.user, calculator_id=calculator_id).delete()
        if not deleted:
            return Response({'success': False}, status=status.HTTP_404_NOT_FOUND)
        return Response({'success': True})


# ============================================================================
# CALCULATOR RATINGS — public 1–5 stars + comment (one per user per calculator)
# ============================================================================

class RatingView(APIView):
    """
    GET  /api/calculators/ratings/?calculator_id=salary
         -> public aggregate (average, count, distribution) + recent comments
            + the caller's own rating if logged in.
    POST /api/calculators/ratings/  { calculator_id, rating(1-5), comment? }
         -> create/update the logged-in user's rating (upsert).
    """
    def get_permissions(self):
        from rest_framework.permissions import AllowAny as _Any
        return [_Any()] if self.request.method == 'GET' else [IsAuthenticated()]

    def get_throttles(self):
        # Throttle only writes (spam control); reads use the global anon/user caps.
        if self.request.method == 'POST':
            from rest_framework.throttling import ScopedRateThrottle
            self.throttle_scope = 'rating'
            return [ScopedRateThrottle()]
        return super().get_throttles()

    def get(self, request):
        from django.db.models import Avg, Count
        from calculators.models import CalculatorRating
        from .serializers import CalculatorRatingSerializer

        calc_id = request.query_params.get('calculator_id')
        if not calc_id:
            return Response({'success': False, 'error': 'calculator_id je povinný.'},
                            status=status.HTTP_400_BAD_REQUEST)

        qs = CalculatorRating.objects.filter(calculator_id=calc_id)
        agg = qs.aggregate(avg=Avg('rating'), count=Count('id'))
        distribution = {str(i): qs.filter(rating=i).count() for i in range(1, 6)}
        recent = qs.exclude(comment='').select_related('user').order_by('-updated_at')[:10]

        my = None
        if getattr(request.user, 'is_authenticated', False):
            mine = qs.filter(user=request.user).first()
            if mine:
                my = CalculatorRatingSerializer(mine).data

        return Response({
            'success': True,
            'calculator_id': calc_id,
            'average': round(agg['avg'], 2) if agg['avg'] else 0,
            'count': agg['count'],
            'distribution': distribution,
            'recent': CalculatorRatingSerializer(recent, many=True).data,
            'my_rating': my,
        })

    def post(self, request):
        from django.db.models import Avg, Count
        from calculators.models import CalculatorRating
        from .serializers import CalculatorRatingSerializer

        serializer = CalculatorRatingSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'success': False, 'errors': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        rating, _created = CalculatorRating.objects.update_or_create(
            user=request.user, calculator_id=data['calculator_id'],
            defaults={'rating': data['rating'], 'comment': data.get('comment', '')},
        )
        qs = CalculatorRating.objects.filter(calculator_id=data['calculator_id'])
        agg = qs.aggregate(avg=Avg('rating'), count=Count('id'))
        return Response({
            'success': True,
            'data': CalculatorRatingSerializer(rating).data,
            'average': round(agg['avg'], 2) if agg['avg'] else 0,
            'count': agg['count'],
        }, status=status.HTTP_201_CREATED if _created else status.HTTP_200_OK)


# ============================================================================
# MONETIZATION VIEWS (lead-gen capture + affiliate click tracking)
# ============================================================================

from .serializers import LeadSerializer, AffiliateClickSerializer


def _client_ip(request):
    """Best-effort client IP, honouring a single proxy hop."""
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    if xff:
        return xff.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


class LeadCreateView(APIView):
    """
    Capture a qualified lead from a calculator and persist it for routing/selling.

    POST /api/calculators/leads/
    Body: { vertical, calculator_type, name, email, phone, region, message,
            context, consent, source_url }

    This is the core of the highest-value monetization model (lead-gen).
    Stored leads are routed/sold to partners (brokers, installers, etc.).
    """
    permission_classes = [AllowAny]
    authentication_classes = []  # anonymous, public — avoid session/CSRF enforcement
    throttle_scope = 'leads'

    def post(self, request):
        serializer = LeadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'success': False, 'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not request.session.session_key:
            request.session.save()

        serializer.save(
            session_key=request.session.session_key or '',
            ip_address=_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:300],
        )
        return Response(
            {
                'success': True,
                'message': 'Ďakujeme! Ozveme sa vám čo najskôr s nezáväznou ponukou.',
                'lead_id': serializer.data.get('id'),
            },
            status=status.HTTP_201_CREATED,
        )


class AffiliateClickView(APIView):
    """
    Record an outbound click on a partner/affiliate CTA (for EPC reconciliation).

    POST /api/calculators/affiliate-click/
    Body: { partner, offer_id, calculator_type, target_url, source_url }
    """
    permission_classes = [AllowAny]
    authentication_classes = []  # anonymous, public — avoid session/CSRF enforcement

    def post(self, request):
        serializer = AffiliateClickSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'success': False, 'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not request.session.session_key:
            request.session.save()

        serializer.save(
            session_key=request.session.session_key or '',
            ip_address=_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:300],
        )
        return Response({'success': True}, status=status.HTTP_201_CREATED)


class DataReportCreateView(APIView):
    """
    Capture a "this calculator shows wrong data" report and email it to the
    operator immediately so figures can be corrected as laws/prices change.

    POST /api/calculators/data-report/
    Body: { calculator_type, page_url, message, reporter_email?, locale? }
    """
    permission_classes = [AllowAny]
    authentication_classes = []  # anonymous, public — avoid session/CSRF enforcement
    throttle_scope = 'data_report'

    def post(self, request):
        from .serializers import DataReportSerializer

        serializer = DataReportSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'success': False, 'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not request.session.session_key:
            request.session.save()

        report = serializer.save(
            session_key=request.session.session_key or '',
            ip_address=_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:300],
        )

        # Email the operator right away (best-effort — never fail the request).
        self._notify_operator(report)

        return Response(
            {'success': True,
             'message': 'Ďakujeme! Nahlásenie sme prijali a pozrieme sa naň.'},
            status=status.HTTP_201_CREATED,
        )

    def _notify_operator(self, report):
        from django.conf import settings
        from django.core.mail import send_mail

        recipient = getattr(settings, 'DATA_REPORT_RECIPIENT', None)
        if not recipient:
            return
        subject = f"Hlásenie nesprávnych údajov: {report.calculator_type or 'kalkulačka'}"
        body = (
            "Používateľ nahlásil nesprávne údaje v kalkulačke.\n\n"
            f"Kalkulačka: {report.calculator_type or '—'}\n"
            f"URL: {report.page_url or '—'}\n"
            f"Jazyk: {report.locale or '—'}\n"
            f"Kontakt (nepovinné): {report.reporter_email or '—'}\n"
            f"Čas: {report.created_at:%Y-%m-%d %H:%M}\n\n"
            f"Správa:\n{report.message}\n\n"
            f"— Admin: /admin/calculators/datareport/{report.id}/change/"
        )
        try:
            send_mail(
                subject,
                body,
                getattr(settings, 'DEFAULT_FROM_EMAIL', None),
                [recipient],
                fail_silently=False,
            )
            report.emailed = True
            report.save(update_fields=['emailed'])
        except Exception as e:
            # Stored anyway; surface the failure in logs without breaking the POST.
            print(f"DataReport email failed: {e}")


class SolarSubsidyCalculatorView(APIView):
    """
    Solar / Photovoltaic Subsidy & Payback Calculator.

    POST /api/calculators/solar/
    Body: { annual_consumption_kwh, electricity_rate?, system_size_kwp?,
            include_battery?, battery_capacity_kwh? }
    """
    permission_classes = [AllowAny]

    def post(self, request):
        from .serializers import SolarSubsidyCalculatorSerializer
        from .services import SolarSubsidyCalculator

        serializer = SolarSubsidyCalculatorSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            data = dict(serializer.validated_data)
            country = (data.pop('country', 'SK') or 'SK').upper()
            if country == 'CZ':
                from .services.solar_international import calculate_cz_solar
                result = calculate_cz_solar(**data)
            else:
                result = SolarSubsidyCalculator().calculate(**data)
                result.setdefault('country', 'SK')
                result.setdefault('currency', 'EUR')
            return Response(
                {'success': True, 'data': result, 'calculator': 'solar',
                 'country': country, 'version': '2026'},
                status=status.HTTP_200_OK,
            )
        except ValueError as e:
            return Response({'success': False, 'error': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'success': False, 'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ============================================================================
# ANALYTICS (first-party, privacy-respecting visitor tracking)
# ============================================================================

_BOT_UA = ('bot', 'crawler', 'spider', 'crawl', 'slurp', 'bingpreview',
           'facebookexternalhit', 'headless', 'python-requests', 'curl', 'wget')


class AnalyticsCollectView(APIView):
    """
    Collect a first-party page view. Called by the frontend ONLY when the user
    has granted analytics consent. No raw IP stored; `visitor_hash` is an
    anonymous rotating id for unique-visitor estimation.

    POST /api/calculators/analytics/collect/
    Body: { path, referrer_host?, locale?, device?, visitor_hash? }
    """
    permission_classes = [AllowAny]
    from rest_framework_simplejwt.authentication import JWTAuthentication
    authentication_classes = [JWTAuthentication]  # attribute logged-in users; no CSRF
    throttle_scope = 'analytics'

    def post(self, request):
        from .serializers import PageViewSerializer
        from .models import PageView

        ua = request.META.get('HTTP_USER_AGENT', '').lower()
        if any(b in ua for b in _BOT_UA):
            return Response(status=status.HTTP_204_NO_CONTENT)  # ignore bots

        serializer = PageViewSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_204_NO_CONTENT)  # never block the client

        if not request.session.session_key:
            try:
                request.session.save()
            except Exception:
                pass

        user = request.user if getattr(request.user, 'is_authenticated', False) else None
        PageView.objects.create(
            **serializer.validated_data,
            session_key=request.session.session_key or '',
            user=user,
        )
        return Response(status=status.HTTP_204_NO_CONTENT)


class AnalyticsStatsView(APIView):
    """
    Aggregated visitor stats for the operator (staff only).

    GET /api/calculators/analytics/stats/?period=week   (day|week|month|year)
    or  ?days=30
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        from datetime import timedelta
        from django.utils import timezone
        from django.db.models import Count
        from django.db.models.functions import TruncDate
        from .models import PageView, AuthEvent

        period = request.query_params.get('period', 'week')
        days_map = {'day': 1, 'week': 7, 'month': 30, 'year': 365}
        try:
            days = int(request.query_params.get('days', days_map.get(period, 7)))
        except (TypeError, ValueError):
            days = 7
        days = max(1, min(days, 730))
        since = timezone.now() - timedelta(days=days)

        views = PageView.objects.filter(created_at__gte=since)
        auth = AuthEvent.objects.filter(created_at__gte=since)

        by_day = list(
            views.annotate(d=TruncDate('created_at')).values('d')
                 .annotate(views=Count('id'), visitors=Count('visitor_hash', distinct=True))
                 .order_by('d')
        )
        top_paths = list(
            views.values('path').annotate(views=Count('id'))
                 .order_by('-views')[:15]
        )
        logins_by_event = {
            row['event']: row['n']
            for row in auth.values('event').annotate(n=Count('id'))
        }

        return Response({
            'success': True,
            'period_days': days,
            'since': since.strftime('%Y-%m-%d'),
            'totals': {
                'page_views': views.count(),
                'unique_visitors': views.values('visitor_hash').distinct().count(),
                'logins': logins_by_event.get('login', 0) + logins_by_event.get('google_login', 0),
                'failed_logins': logins_by_event.get('login_failed', 0),
                'registrations': logins_by_event.get('register', 0),
            },
            'by_day': [
                {'date': r['d'].strftime('%Y-%m-%d') if r['d'] else None,
                 'views': r['views'], 'visitors': r['visitors']}
                for r in by_day
            ],
            'top_paths': top_paths,
            'auth_events': logins_by_event,
        })
