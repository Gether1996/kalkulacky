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
    
    # Health check
    path('health/', HealthCheckView.as_view(), name='health-check'),
    
    # Blog endpoints
    path('blog/categories/', BlogCategoryListView.as_view(), name='blog-categories'),
    path('blog/posts/', BlogPostListView.as_view(), name='blog-posts'),
    path('blog/posts/<slug:slug>/', BlogPostDetailView.as_view(), name='blog-post-detail'),
    path('blog/featured/', FeaturedBlogPostsView.as_view(), name='blog-featured'),
]
