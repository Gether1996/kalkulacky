"""
URL Configuration for Calculators API

API Endpoints:
    GET  /api/calculators/           - List all calculators
    POST /api/calculators/salary/    - Calculate net salary
    POST /api/calculators/mortgage/  - Calculate mortgage
    POST /api/calculators/vat/       - Calculate VAT
    GET  /api/health/                - Health check
    
Blog Endpoints:
    GET  /api/blog/categories/       - List blog categories
    GET  /api/blog/posts/            - List blog posts (filterable)
    GET  /api/blog/posts/<slug>/     - Get single blog post
    GET  /api/blog/featured/         - Get featured blog posts
"""

from django.urls import path
from .views import (
    CalculatorListView,
    SalaryCalculatorView,
    MortgageCalculatorView,
    VATCalculatorView,
    LoanCalculatorView,
    FuelCostCalculatorView,
    BMICalculatorView,
    PercentageCalculatorView,
    PregnancyCalculatorView,
    PensionCalculatorView,
    VacationCalculatorView,
    EnergyCalculatorView,
    BMRCalculatorView,
    PaymentCalculatorView,
    FreelancerTaxCalculatorView,
    InflationCalculatorView,
    ROICalculatorView,
    HoursWorkedCalculatorView,
    UnitConverterView,
    UnitConverterCategoriesView,
    UnitConverterUnitsView,
    SickLeaveCalculatorView,
    CarLeasingCalculatorView,
    AreaVolumeCalculatorView,
    AreaVolumeShapesView,
    SplitBillCalculatorView,
    TipSuggestionsView,
    HealthCheckView,
    BlogCategoryListView,
    BlogPostListView,
    BlogPostDetailView,
    FeaturedBlogPostsView,
)

app_name = 'calculators'

urlpatterns = [
    # Calculator list
    path('', CalculatorListView.as_view(), name='calculator-list'),
    
    # Individual calculators
    path('salary/', SalaryCalculatorView.as_view(), name='salary-calculator'),
    path('mortgage/', MortgageCalculatorView.as_view(), name='mortgage-calculator'),
    path('vat/', VATCalculatorView.as_view(), name='vat-calculator'),
    path('loan/', LoanCalculatorView.as_view(), name='loan-calculator'),
    path('fuel-cost/', FuelCostCalculatorView.as_view(), name='fuel-cost-calculator'),
    path('bmi/', BMICalculatorView.as_view(), name='bmi-calculator'),
    path('percentage/', PercentageCalculatorView.as_view(), name='percentage-calculator'),
    path('pregnancy/', PregnancyCalculatorView.as_view(), name='pregnancy-calculator'),
    path('pension/', PensionCalculatorView.as_view(), name='pension-calculator'),
    path('vacation/', VacationCalculatorView.as_view(), name='vacation-calculator'),
    path('energy/', EnergyCalculatorView.as_view(), name='energy-calculator'),
    path('bmr/', BMRCalculatorView.as_view(), name='bmr-calculator'),
    path('payment/', PaymentCalculatorView.as_view(), name='payment-calculator'),
    path('freelancer-tax/', FreelancerTaxCalculatorView.as_view(), name='freelancer-tax-calculator'),
    path('inflation/', InflationCalculatorView.as_view(), name='inflation-calculator'),
    path('roi/', ROICalculatorView.as_view(), name='roi-calculator'),
    path('hours-worked/', HoursWorkedCalculatorView.as_view(), name='hours-worked-calculator'),
    
    # Unit converter
    path('unit-converter/', UnitConverterView.as_view(), name='unit-converter'),
    path('unit-converter/categories/', UnitConverterCategoriesView.as_view(), name='unit-converter-categories'),
    path('unit-converter/units/', UnitConverterUnitsView.as_view(), name='unit-converter-units'),
    
    # Sick leave calculator
    path('sick-leave/', SickLeaveCalculatorView.as_view(), name='sick-leave-calculator'),
    
    # Car leasing calculator
    path('car-leasing/', CarLeasingCalculatorView.as_view(), name='car-leasing-calculator'),
    
    # Area & Volume calculator
    path('area-volume/', AreaVolumeCalculatorView.as_view(), name='area-volume-calculator'),
    path('area-volume/shapes/', AreaVolumeShapesView.as_view(), name='area-volume-shapes'),
    
    # Split bill calculator
    path('split-bill/', SplitBillCalculatorView.as_view(), name='split-bill-calculator'),
    path('split-bill/tip-suggestions/', TipSuggestionsView.as_view(), name='tip-suggestions'),
    
    # Health check
    path('health/', HealthCheckView.as_view(), name='health-check'),
    
    # Blog endpoints
    path('blog/categories/', BlogCategoryListView.as_view(), name='blog-categories'),
    path('blog/posts/', BlogPostListView.as_view(), name='blog-posts'),
    path('blog/posts/<slug:slug>/', BlogPostDetailView.as_view(), name='blog-post-detail'),
    path('blog/featured/', FeaturedBlogPostsView.as_view(), name='blog-featured'),
]
