"""
API Serializers for Calculator Endpoints

Each calculator has its own request/response serializers for data validation.
"""

from rest_framework import serializers


class SalaryCalculatorSerializer(serializers.Serializer):
    """Serializer for Salary Calculator API"""
    gross_salary = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2,
        min_value=0,
        max_value=50000,
        help_text="Gross monthly salary in EUR"
    )
    children_under_15 = serializers.IntegerField(
        required=False,
        default=0,
        min_value=0,
        max_value=10,
        help_text="Number of dependent children under 15 years (100 EUR/month tax bonus each)"
    )
    children_15_to_18 = serializers.IntegerField(
        required=False,
        default=0,
        min_value=0,
        max_value=10,
        help_text="Number of dependent children 15-18 years (50 EUR/month tax bonus each)"
    )
    apply_nontaxable_amount = serializers.BooleanField(
        required=False,
        default=True,
        help_text="Apply non-taxable amount (NČZD) 497.23 EUR/month - typically True for single employer, False for retirees or multiple employers"
    )
    has_disability = serializers.BooleanField(
        required=False,
        default=False,
        help_text="Person has disability (ZŤP) - reduces health insurance to 2.5% instead of 5% (total contributions 11.9% instead of 14.4%)"
    )
    
    def validate_gross_salary(self, value):
        """Custom validation for gross salary"""
        if value <= 0:
            raise serializers.ValidationError("Gross salary must be greater than 0")
        return value
    
    def validate_children_under_15(self, value):
        """Custom validation for number of children under 15"""
        if value < 0:
            raise serializers.ValidationError("Number of children cannot be negative")
        return value
    
    def validate_children_15_to_18(self, value):
        """Custom validation for number of children 15-18"""
        if value < 0:
            raise serializers.ValidationError("Number of children cannot be negative")
        return value


class MortgageCalculatorSerializer(serializers.Serializer):
    """Serializer for Mortgage Calculator API"""
    loan_amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=1,
        max_value=1000000,
        help_text="Total loan amount in EUR"
    )
    annual_interest_rate = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=20,
        help_text="Annual interest rate (e.g., 3.5 for 3.5%)"
    )
    loan_term_years = serializers.IntegerField(
        min_value=1,
        max_value=40,
        help_text="Loan term in years"
    )
    
    def validate(self, data):
        """Cross-field validation"""
        if data['loan_amount'] < 1000:
            raise serializers.ValidationError(
                {"loan_amount": "Loan amount should be at least €1,000"}
            )
        return data


class VATCalculatorSerializer(serializers.Serializer):
    """Serializer for VAT Calculator API"""
    amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=0,
        help_text="Amount in EUR"
    )
    vat_rate = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
        default=20,
        help_text="VAT rate percentage (default: 20 for Slovak standard rate)"
    )
    calculation_type = serializers.ChoiceField(
        choices=['add_vat', 'remove_vat'],
        default='add_vat',
        help_text="'add_vat' to add VAT to amount, 'remove_vat' to extract VAT from amount"
    )
    
    def validate_calculation_type(self, value):
        """Validate calculation type"""
        if value not in ['add_vat', 'remove_vat']:
            raise serializers.ValidationError(
                "calculation_type must be 'add_vat' or 'remove_vat'"
            )
        return value


class BMICalculatorSerializer(serializers.Serializer):
    """Serializer for BMI Calculator API"""
    weight = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        min_value=1,
        max_value=500,
        help_text="Weight in kilograms"
    )
    height = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        min_value=50,
        max_value=300,
        help_text="Height in centimeters"
    )


class LoanCalculatorSerializer(serializers.Serializer):
    """Serializer for Generic Loan Calculator API"""
    principal = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=100,
        max_value=100000,
        help_text="Loan principal amount in EUR"
    )
    annual_interest_rate = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=30,
        help_text="Annual interest rate percentage"
    )
    term_months = serializers.IntegerField(
        min_value=1,
        max_value=360,
        help_text="Loan term in months"
    )


class CalculatorListSerializer(serializers.Serializer):
    """Serializer for listing available calculators"""
    name = serializers.CharField()
    slug = serializers.CharField()
    description = serializers.CharField()
    search_volume = serializers.IntegerField()
    endpoint = serializers.CharField()
    keywords = serializers.ListField(child=serializers.CharField())


# Blog Serializers

from .models import BlogCategory, BlogPost


class BlogCategorySerializer(serializers.ModelSerializer):
    """Serializer for Blog Categories"""
    post_count = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogCategory
        fields = ['id', 'name', 'slug', 'description', 'color', 'icon', 'order', 'post_count', 'created_at']
    
    def get_post_count(self, obj):
        return obj.posts.filter(status='published').count()


class BlogPostListSerializer(serializers.ModelSerializer):
    """Serializer for Blog Post List (summary view)"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_slug = serializers.CharField(source='category.slug', read_only=True)
    category_color = serializers.CharField(source='category.color', read_only=True)
    tags_list = serializers.SerializerMethodField()
    read_time = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'excerpt', 'featured_image_url',
            'category_name', 'category_slug', 'category_color',
            'tags_list', 'published_at', 'view_count', 'read_time',
            'related_calculator'
        ]
    
    def get_tags_list(self, obj):
        return obj.get_tags_list()
    
    def get_read_time(self, obj):
        """Estimate read time based on content length"""
        word_count = len(obj.content_html.split())
        minutes = max(1, round(word_count / 200))  # 200 words per minute
        return f"{minutes} min"


class BlogPostDetailSerializer(serializers.ModelSerializer):
    """Serializer for Blog Post Detail (full content)"""
    category = BlogCategorySerializer(read_only=True)
    tags_list = serializers.SerializerMethodField()
    read_time = serializers.SerializerMethodField()
    related_posts = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'excerpt', 'content_html',
            'meta_keywords', 'featured_image_url', 'category',
            'tags_list', 'related_calculator', 'status',
            'published_at', 'view_count', 'read_time', 'related_posts',
            'created_at', 'updated_at'
        ]
    
    def get_tags_list(self, obj):
        return obj.get_tags_list()
    
    def get_read_time(self, obj):
        word_count = len(obj.content_html.split())
        minutes = max(1, round(word_count / 200))
        return f"{minutes} min"
    
    def get_related_posts(self, obj):
        """Get related posts from same category"""
        related = BlogPost.objects.filter(
            category=obj.category,
            status='published'
        ).exclude(id=obj.id)[:3]
        return BlogPostListSerializer(related, many=True).data

