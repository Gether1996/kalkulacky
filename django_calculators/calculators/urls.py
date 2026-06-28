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
    ParentalBenefitCalculatorView,
    SolarSubsidyCalculatorView,
    SavingsGoalCalculatorView,
    SavingsGoalListCreateView,
    SavingsGoalDetailView,
    SavingsContributionCreateView,
    SavingsContributionDeleteView,
    FavoriteListCreateView,
    FavoriteReorderView,
    FavoriteDeleteView,
    RatingView,
    SavedCalculationViewSet,
    SavedCalculationDetailView,
    NotificationListView,
    MyDashboardView,
    UserReminderListCreateView,
    UserReminderDetailView,
    LeadCreateView,
    AffiliateClickView,
    DataReportCreateView,
    AnalyticsCollectView,
    AnalyticsStatsView,
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
    
    # Parental benefit calculator
    path('parental-benefit/', ParentalBenefitCalculatorView.as_view(), name='parental-benefit-calculator'),

    # Solar / PV subsidy & payback calculator
    path('solar/', SolarSubsidyCalculatorView.as_view(), name='solar-subsidy-calculator'),

    # Savings goal — public projection + logged-in progress tracker
    path('savings-goal/', SavingsGoalCalculatorView.as_view(), name='savings-goal-calculator'),
    path('my/savings-goals/', SavingsGoalListCreateView.as_view(), name='my-savings-goals'),
    path('my/savings-goals/<int:pk>/', SavingsGoalDetailView.as_view(), name='my-savings-goal-detail'),
    path('my/savings-goals/<int:goal_id>/contributions/', SavingsContributionCreateView.as_view(), name='my-savings-goal-contributions'),
    path('my/savings-goals/<int:goal_id>/contributions/<int:pk>/', SavingsContributionDeleteView.as_view(), name='my-savings-goal-contribution-detail'),

    # Favorite calculators (per-user pinned tools + custom order)
    path('my/favorites/', FavoriteListCreateView.as_view(), name='my-favorites'),
    path('my/favorites/reorder/', FavoriteReorderView.as_view(), name='my-favorites-reorder'),
    path('my/favorites/<str:calculator_id>/', FavoriteDeleteView.as_view(), name='my-favorite-detail'),

    # Calculator ratings (public aggregate + logged-in submit)
    path('ratings/', RatingView.as_view(), name='ratings'),

    # Saved calculations + tracking/notifications (logged-in dashboard + anon)
    path('saved-calculations/', SavedCalculationViewSet.as_view(), name='saved-calculations'),
    path('saved-calculations/<int:pk>/', SavedCalculationDetailView.as_view(), name='saved-calculation-detail'),
    path('saved-calculations/<int:calculation_id>/notifications/', NotificationListView.as_view(), name='saved-calculation-notifications'),
    path('my/dashboard/', MyDashboardView.as_view(), name='my-dashboard'),
    path('my/reminders/', UserReminderListCreateView.as_view(), name='my-reminders'),
    path('my/reminders/<int:pk>/', UserReminderDetailView.as_view(), name='my-reminder-detail'),

    # Monetization (lead-gen + affiliate tracking)
    path('leads/', LeadCreateView.as_view(), name='lead-create'),
    path('affiliate-click/', AffiliateClickView.as_view(), name='affiliate-click'),

    # Data-correction reports (user flags wrong/outdated figures → emails operator)
    path('data-report/', DataReportCreateView.as_view(), name='data-report'),

    # First-party analytics (visitor page views + operator stats)
    path('analytics/collect/', AnalyticsCollectView.as_view(), name='analytics-collect'),
    path('analytics/stats/', AnalyticsStatsView.as_view(), name='analytics-stats'),

    # Health check
    path('health/', HealthCheckView.as_view(), name='health-check'),
    
    # Blog endpoints
    path('blog/categories/', BlogCategoryListView.as_view(), name='blog-categories'),
    path('blog/posts/', BlogPostListView.as_view(), name='blog-posts'),
    path('blog/posts/<slug:slug>/', BlogPostDetailView.as_view(), name='blog-post-detail'),
    path('blog/featured/', FeaturedBlogPostsView.as_view(), name='blog-featured'),
]
