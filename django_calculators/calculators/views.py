"""
API Views for Calculator Endpoints

Each calculator has a dedicated API endpoint that accepts POST requests
with calculation parameters and returns results.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    SalaryCalculatorSerializer,
    MortgageCalculatorSerializer,
    VATCalculatorSerializer,
    CalculatorListSerializer,
)
from .services import (
    SalaryCalculator,
    MortgageCalculator,
    VATCalculator,
)


class CalculatorListView(APIView):
    """
    List all available calculators with metadata.
    
    GET /api/calculators/
    """
    
    def get(self, request):
        """Return list of all available calculators"""
        calculators = [
            {
                'name': 'Čistá mzda',
                'slug': 'salary',
                'description': 'Výpočet čistej mzdy z hrubej mzdy (Slovak net salary calculator)',
                'search_volume': 12000,
                'endpoint': '/api/calculators/salary/',
                'keywords': ['čistá mzda', 'kalkulačka mzdy', 'výpočet platu'],
            },
            {
                'name': 'Hypotéka',
                'slug': 'mortgage',
                'description': 'Výpočet mesačnej splátky hypotéky (Mortgage payment calculator)',
                'search_volume': 8000,
                'endpoint': '/api/calculators/mortgage/',
                'keywords': ['kalkulačka hypotéky', 'splátka hypotéky', 'hypotéka výpočet'],
            },
            {
                'name': 'DPH',
                'slug': 'vat',
                'description': 'Výpočet DPH (Slovak VAT calculator)',
                'search_volume': 5000,
                'endpoint': '/api/calculators/vat/',
                'keywords': ['kalkulačka dph', 'výpočet dph', 'dph kalkulačka'],
            },
        ]
        
        serializer = CalculatorListSerializer(calculators, many=True)
        return Response({
            'count': len(calculators),
            'calculators': serializer.data
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
            calculator = SalaryCalculator()
            result = calculator.calculate(**serializer.validated_data)
            
            return Response({
                'success': True,
                'data': result,
                'calculator': 'salary',
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
            result = calculator.calculate(**serializer.validated_data)
            
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


class HealthCheckView(APIView):
    """
    Health check endpoint to verify API is running.
    
    GET /api/health/
    """
    
    def get(self, request):
        """Return API health status"""
        return Response({
            'status': 'healthy',
            'api_version': '1.0',
            'year': 2026,
            'calculators_available': 3
        })


# Blog Views

from rest_framework import generics, filters
from django.utils import timezone
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
            published_at__lte=timezone.now()
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
            published_at__lte=timezone.now()
        ).order_by('-published_at')[:5]

