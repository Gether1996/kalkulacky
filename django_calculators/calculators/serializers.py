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
    loan_amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=100,
        max_value=1000000,
        help_text="Loan amount in EUR"
    )
    interest_rate = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=30,
        help_text="Annual interest rate percentage (e.g., 5.5 for 5.5%)"
    )
    loan_years = serializers.IntegerField(
        min_value=1,
        max_value=50,
        help_text="Loan term in years"
    )
    include_schedule = serializers.BooleanField(
        required=False,
        default=False,
        help_text="Include full amortization schedule in response"
    )


class FuelCostCalculatorSerializer(serializers.Serializer):
    """Serializer for Fuel Cost Calculator API"""
    distance = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.1,
        max_value=10000,
        help_text="Distance to travel in kilometers"
    )
    consumption = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        min_value=0.1,
        max_value=50,
        help_text="Fuel consumption in liters per 100 km"
    )
    fuel_price = serializers.DecimalField(
        max_digits=5,
        decimal_places=3,
        min_value=0.001,
        max_value=10,
        help_text="Fuel price in EUR per liter"
    )


class PercentageCalculatorSerializer(serializers.Serializer):
    """Serializer for Percentage Calculator API"""
    calculation_type = serializers.ChoiceField(
        choices=[
            ('percent_of', 'What is X% of Y?'),
            ('is_what_percent', 'X is what % of Y?'),
            ('percentage_change', 'Percentage change from X to Y'),
            ('add_percent', 'Add X% to Y'),
            ('subtract_percent', 'Subtract X% from Y')
        ],
        help_text="Type of percentage calculation to perform"
    )
    value1 = serializers.DecimalField(
        max_digits=15,
        decimal_places=2,
        required=False,
        allow_null=True,
        help_text="First value (required for some calculation types)"
    )
    value2 = serializers.DecimalField(
        max_digits=15,
        decimal_places=2,
        required=False,
        allow_null=True,
        help_text="Second value (required for some calculation types)"
    )
    percent = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        allow_null=True,
        help_text="Percentage value (required for some calculation types)"
    )


class PregnancyCalculatorSerializer(serializers.Serializer):
    """Serializer for Pregnancy Calculator API"""
    calculation_method = serializers.ChoiceField(
        choices=[('lmp', 'Last Menstrual Period'), ('conception', 'Conception Date')],
        help_text="Method to calculate due date: from LMP or conception date"
    )
    lmp_date = serializers.DateField(
        required=False,
        allow_null=True,
        help_text="Last menstrual period date (required if method is 'lmp')"
    )
    conception_date = serializers.DateField(
        required=False,
        allow_null=True,
        help_text="Conception/ovulation date (required if method is 'conception')"
    )
    current_date = serializers.DateField(
        required=False,
        allow_null=True,
        help_text="Current date for calculation (defaults to today)"
    )


class PensionCalculatorSerializer(serializers.Serializer):
    """Serializer for Pension Calculator API"""
    current_age = serializers.IntegerField(
        min_value=18,
        max_value=70,
        help_text="Current age in years"
    )
    gross_salary = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0,
        help_text="Monthly gross salary in EUR"
    )
    years_worked = serializers.IntegerField(
        min_value=0,
        help_text="Number of years already worked"
    )
    gender = serializers.ChoiceField(
        choices=[('male', 'Male'), ('female', 'Female')],
        default='male',
        required=False,
        help_text="Gender (affects retirement age)"
    )
    include_second_pillar = serializers.BooleanField(
        default=True,
        required=False,
        help_text="Whether contributing to 2nd pillar"
    )
    second_pillar_rate = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=6.0,
        required=False,
        help_text="2nd pillar contribution rate %"
    )


class VacationCalculatorSerializer(serializers.Serializer):
    """Serializer for Vacation Days Calculator API"""
    age = serializers.IntegerField(
        min_value=15,
        max_value=100,
        help_text="Current age in years"
    )
    employment_start_date = serializers.DateField(
        help_text="Date when employment started (YYYY-MM-DD)"
    )
    current_date = serializers.DateField(
        required=False,
        allow_null=True,
        help_text="Current date for calculation (defaults to today)"
    )
    vacation_days_used = serializers.DecimalField(
        max_digits=5,
        decimal_places=1,
        default=0,
        required=False,
        help_text="Number of vacation days already used this year"
    )
    days_carried_over = serializers.DecimalField(
        max_digits=5,
        decimal_places=1,
        default=0,
        required=False,
        help_text="Vacation days carried over from previous year"
    )
    planned_vacation_days = serializers.DecimalField(
        max_digits=5,
        decimal_places=1,
        default=0,
        required=False,
        help_text="Number of days planning to take"
    )


class EnergyCalculatorSerializer(serializers.Serializer):
    """Serializer for Energy Cost Calculator API"""
    electricity_consumption = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0,
        help_text="Monthly electricity consumption in kWh"
    )
    gas_consumption = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0,
        default=0,
        required=False,
        help_text="Monthly gas consumption in kWh (0 if no gas)"
    )
    electricity_rate = serializers.DecimalField(
        max_digits=6,
        decimal_places=4,
        required=False,
        help_text="Custom electricity rate in EUR/kWh"
    )
    gas_rate = serializers.DecimalField(
        max_digits=6,
        decimal_places=4,
        required=False,
        help_text="Custom gas rate in EUR/kWh"
    )
    has_dual_tariff = serializers.BooleanField(
        default=False,
        required=False,
        help_text="Whether using dual electricity tariff"
    )
    high_tariff_percentage = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=40,
        required=False,
        help_text="Percentage of consumption during high tariff"
    )
    household_size = serializers.IntegerField(
        min_value=1,
        default=2,
        required=False,
        help_text="Number of people in household"
    )


class BMRCalculatorSerializer(serializers.Serializer):
    """Serializer for BMR (Basal Metabolic Rate) Calculator API"""
    weight = serializers.DecimalField(
        max_digits=5,
        decimal_places=1,
        min_value=1,
        help_text="Weight in kg"
    )
    height = serializers.DecimalField(
        max_digits=5,
        decimal_places=1,
        min_value=1,
        help_text="Height in cm"
    )
    age = serializers.IntegerField(
        min_value=15,
        max_value=100,
        help_text="Age in years"
    )
    gender = serializers.ChoiceField(
        choices=[('male', 'Male'), ('female', 'Female')],
        help_text="Gender (affects BMR calculation)"
    )
    activity_level = serializers.ChoiceField(
        choices=[
            ('sedentary', 'Sedentary'),
            ('light', 'Light'),
            ('moderate', 'Moderate'),
            ('active', 'Active'),
            ('very_active', 'Very Active')
        ],
        default='sedentary',
        required=False,
        help_text="Activity level"
    )
    weight_goal = serializers.ChoiceField(
        choices=[
            ('lose_fast', 'Lose Fast'),
            ('lose_moderate', 'Lose Moderate'),
            ('lose_slow', 'Lose Slow'),
            ('maintain', 'Maintain'),
            ('gain_slow', 'Gain Slow'),
            ('gain_moderate', 'Gain Moderate'),
            ('gain_fast', 'Gain Fast')
        ],
        default='maintain',
        required=False,
        help_text="Weight goal"
    )


class PaymentCalculatorSerializer(serializers.Serializer):
    """Serializer for Payment Calculator API"""
    loan_amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=0.01,
        help_text="Principal loan amount"
    )
    annual_interest_rate = serializers.DecimalField(
        max_digits=6,
        decimal_places=2,
        min_value=0,
        help_text="Annual interest rate in percentage"
    )
    loan_term_years = serializers.DecimalField(
        max_digits=5,
        decimal_places=1,
        min_value=0.1,
        help_text="Loan term in years"
    )
    payment_frequency = serializers.ChoiceField(
        choices=[('monthly', 'Monthly'), ('quarterly', 'Quarterly'), ('yearly', 'Yearly')],
        default='monthly',
        required=False,
        help_text="Payment frequency"
    )
    include_schedule = serializers.BooleanField(
        default=False,
        required=False,
        help_text="Include amortization schedule"
    )


class FreelancerTaxCalculatorSerializer(serializers.Serializer):
    """Serializer for Freelancer Tax Calculator API"""
    annual_revenue = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=0,
        help_text="Annual revenue (total income)"
    )
    annual_expenses = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=0,
        default=0,
        required=False,
        help_text="Annual expenses (actual costs)"
    )
    use_flat_expenses = serializers.BooleanField(
        default=True,
        required=False,
        help_text="Use 60% flat expense rate instead of actual expenses"
    )
    include_sickness = serializers.BooleanField(
        default=True,
        required=False,
        help_text="Include voluntary sickness insurance"
    )
    months_active = serializers.IntegerField(
        min_value=1,
        max_value=12,
        default=12,
        required=False,
        help_text="Number of active months in the year"
    )


class InflationCalculatorSerializer(serializers.Serializer):
    """Serializer for Inflation Calculator API"""
    present_value = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=0.01,
        help_text="Current value of money"
    )
    years = serializers.IntegerField(
        min_value=1,
        max_value=100,
        help_text="Number of years for projection"
    )
    inflation_rate = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        min_value=-10,
        max_value=50,
        default=3.0,
        required=False,
        help_text="Annual inflation rate in percentage"
    )
    calculate_reverse = serializers.BooleanField(
        default=False,
        required=False,
        help_text="Calculate what past money is worth now"
    )


class ROICalculatorSerializer(serializers.Serializer):
    """Serializer for ROI Calculator API"""
    initial_investment = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=0.01,
        help_text="Initial amount invested"
    )
    final_value = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=0,
        help_text="Final or current value of investment"
    )
    additional_costs = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=0,
        default=0,
        required=False,
        help_text="Additional costs incurred"
    )
    investment_period_months = serializers.IntegerField(
        min_value=1,
        max_value=1200,
        required=False,
        allow_null=True,
        help_text="Duration of investment in months"
    )


class HoursWorkedCalculatorSerializer(serializers.Serializer):
    """Serializer for Hours Worked Calculator API"""
    hours_worked = serializers.DecimalField(
        max_digits=6,
        decimal_places=2,
        min_value=0,
        max_value=744,
        help_text="Total hours worked in the period"
    )
    hourly_rate = serializers.DecimalField(
        max_digits=8,
        decimal_places=2,
        min_value=0,
        required=False,
        allow_null=True,
        help_text="Rate per hour"
    )
    standard_hours = serializers.DecimalField(
        max_digits=6,
        decimal_places=2,
        min_value=0,
        required=False,
        allow_null=True,
        help_text="Standard hours for the period"
    )
    overtime_hours = serializers.DecimalField(
        max_digits=6,
        decimal_places=2,
        min_value=0,
        required=False,
        allow_null=True,
        help_text="Overtime hours"
    )
    weekend_hours = serializers.DecimalField(
        max_digits=6,
        decimal_places=2,
        min_value=0,
        default=0,
        required=False,
        help_text="Hours worked on weekends"
    )
    holiday_hours = serializers.DecimalField(
        max_digits=6,
        decimal_places=2,
        min_value=0,
        default=0,
        required=False,
        help_text="Hours worked on holidays"
    )
    period_type = serializers.ChoiceField(
        choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly'), ('custom', 'Custom')],
        default='weekly',
        required=False,
        help_text="Type of period"
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


class UnitConverterSerializer(serializers.Serializer):
    """Serializer for Unit Converter API"""
    value = serializers.FloatField(
        min_value=-1000000000,
        max_value=1000000000,
        help_text="Hodnota na konverziu"
    )
    from_unit = serializers.CharField(
        max_length=50,
        help_text="Zdrojová jednotka (napr. 'meter', 'kilogram', 'celsius')"
    )
    to_unit = serializers.CharField(
        max_length=50,
        help_text="Cieľová jednotka (napr. 'kilometer', 'pound', 'fahrenheit')"
    )
    category = serializers.CharField(
        max_length=50,
        help_text="Kategória konverzie (length, weight, volume, area, temperature)"
    )
    
    def validate_category(self, value):
        """Validácia kategórie"""
        valid_categories = ['length', 'weight', 'volume', 'area', 'temperature']
        if value not in valid_categories:
            raise serializers.ValidationError(
                f"Neplatná kategória. Platné hodnoty: {', '.join(valid_categories)}"
            )
        return value


class SickLeaveCalculatorSerializer(serializers.Serializer):
    """Serializer for Sick Leave (Nemocenská) Calculator API"""
    gross_salary = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0,
        max_value=50000,
        help_text="Hrubá mesačná mzda v EUR"
    )
    days_sick = serializers.IntegerField(
        min_value=1,
        max_value=365,
        help_text="Počet dní pracovnej neschopnosti"
    )
    leave_type = serializers.ChoiceField(
        choices=['illness', 'care'],
        default='illness',
        help_text="Typ pracovnej neschopnosti: 'illness' (choroba) alebo 'care' (ošetrovanie člena rodiny)"
    )
    
    def validate_gross_salary(self, value):
        """Validácia hrubej mzdy"""
        if value <= 0:
            raise serializers.ValidationError("Hrubá mzda musí byť väčšia ako 0")
        return value
    
    def validate_days_sick(self, value):
        """Validácia počtu dní"""
        if value < 1:
            raise serializers.ValidationError("Počet dní musí byť aspoň 1")
        return value


class CarLeasingCalculatorSerializer(serializers.Serializer):
    """Serializer for Car Leasing Calculator API"""
    car_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=1000,
        max_value=500000,
        help_text="Cena auta v EUR"
    )
    down_payment = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0,
        help_text="Akontácia v EUR"
    )
    term_months = serializers.IntegerField(
        min_value=12,
        max_value=96,
        help_text="Doba financovania v mesiacoch"
    )
    leasing_rate = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        required=False,
        min_value=0,
        max_value=20,
        help_text="Úroková sadzba lízingu v % (napr. 5.0)"
    )
    loan_rate = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        required=False,
        min_value=0,
        max_value=20,
        help_text="Úroková sadzba úveru v % (napr. 6.0)"
    )
    residual_value_percent = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        required=False,
        default=30,
        min_value=0,
        max_value=70,
        help_text="Zostatkková hodnota v % (pre operatívny lízing)"
    )
    include_vat = serializers.BooleanField(
        required=False,
        default=True,
        help_text="Či je cena s DPH"
    )


class AreaVolumeCalculatorSerializer(serializers.Serializer):
    """Serializer for Area & Volume Calculator API"""
    shape = serializers.CharField(
        max_length=50,
        help_text="Typ tvaru (rectangle, circle, cube, sphere, atď.)"
    )
    dimensions = serializers.DictField(
        child=serializers.FloatField(min_value=0.001, max_value=10000),
        help_text="Rozmery tvaru (napr. {'length': 5, 'width': 3})"
    )
    
    def validate_shape(self, value):
        """Validácia tvaru"""
        valid_shapes = [
            'rectangle', 'square', 'circle', 'triangle', 'trapezoid',
            'cube', 'cuboid', 'cylinder', 'sphere', 'cone', 'pyramid'
        ]
        if value not in valid_shapes:
            raise serializers.ValidationError(
                f"Neplatný tvar. Platné tvary: {', '.join(valid_shapes)}"
            )
        return value


class SplitBillCalculatorSerializer(serializers.Serializer):
    """Serializer for Split Bill Calculator API"""
    split_type = serializers.ChoiceField(
        choices=['equal', 'by_items', 'custom'],
        help_text="Typ rozdelenia: equal, by_items, custom"
    )
    total_amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        required=False,
        help_text="Celková suma účtu v EUR"
    )
    num_people = serializers.IntegerField(
        required=False,
        min_value=1,
        max_value=100,
        help_text="Počet ľudí (pre equal split)"
    )
    tip_percent = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        required=False,
        default=0,
        min_value=0,
        max_value=100,
        help_text="Tip v percentách"
    )
    items = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        help_text="Položky pre by_items split"
    )
    custom_amounts = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        help_text="Vlastné sumy pre custom split"
    )
    
    def validate(self, data):
        """Cross-field validácia"""
        split_type = data['split_type']
        
        if split_type == 'equal':
            if 'num_people' not in data:
                raise serializers.ValidationError({
                    'num_people': 'Počet ľudí je povinný pre rovnomerné rozdelenie'
                })
            if 'total_amount' not in data:
                raise serializers.ValidationError({
                    'total_amount': 'Celková suma je povinná pre rovnomerné rozdelenie'
                })
        
        if split_type == 'by_items' and 'items' not in data:
            raise serializers.ValidationError({
                'items': 'Položky sú povinné pre rozdelenie podľa položiek'
            })
        
        if split_type == 'custom':
            if 'custom_amounts' not in data:
                raise serializers.ValidationError({
                    'custom_amounts': 'Vlastné sumy sú povinné pre custom rozdelenie'
                })
            if 'total_amount' not in data:
                raise serializers.ValidationError({
                    'total_amount': 'Celková suma je povinná pre custom rozdelenie'
                })
        
        return data


class ParentalBenefitCalculatorSerializer(serializers.Serializer):
    """Serializer for Parental Benefit Calculator API"""
    birth_date = serializers.DateField(
        help_text="Child's date of birth (YYYY-MM-DD)"
    )
    gross_salary = serializers.DecimalField(
        required=False,
        max_digits=10,
        decimal_places=2,
        min_value=0,
        max_value=10000,
        help_text="Mother's gross monthly salary before maternity (for materské calculation)"
    )
    benefit_type = serializers.ChoiceField(
        choices=['basic', 'alternative'],
        default='basic',
        help_text="'basic' (osnova - €381.90 for 3 years) or 'alternative' (alternatíva - €270 for 6 years)"
    )
    twins_or_more = serializers.BooleanField(
        required=False,
        default=False,
        help_text="Whether birth was twins/triplets (affects maternity duration: 43 weeks instead of 34)"
    )
    plan_to_work = serializers.BooleanField(
        required=False,
        default=False,
        help_text="Whether parent plans to work while receiving benefit"
    )
    planned_monthly_income = serializers.DecimalField(
        required=False,
        default=0,
        max_digits=10,
        decimal_places=2,
        min_value=0,
        help_text="Expected monthly income if working (gross) - must be under €635.70 to keep benefit"
    )
    second_child_birth_date = serializers.DateField(
        required=False,
        allow_null=True,
        help_text="If planning second child, date of birth (extends benefit)"
    )
    current_date = serializers.DateField(
        required=False,
        allow_null=True,
        help_text="Current date for calculations (defaults to today)"
    )


# ============================================================================
# SAVED CALCULATIONS & NOTIFICATIONS SERIALIZERS
# ============================================================================

class SavedCalculationSerializer(serializers.Serializer):
    """Serializer for SavedCalculation model"""
    id = serializers.IntegerField(read_only=True)
    session_key = serializers.CharField(max_length=100)
    email = serializers.EmailField(
        required=False,
        allow_null=True,
        help_text="Optional email for notifications"
    )
    calculator_type = serializers.ChoiceField(
        choices=[
            'pregnancy', 'vacation', 'mortgage', 'loan', 'salary', 'vat',
            'pension', 'freelancer_tax', 'bmi', 'bmr', 'energy', 'sick_leave',
            'parental_benefit', 'fuel_cost', 'percentage', 'payment',
            'inflation', 'roi', 'hours_worked', 'unit_converter',
            'car_leasing', 'area_volume', 'split_bill'
        ]
    )
    name = serializers.CharField(
        max_length=200,
        help_text="User-defined name for the calculation"
    )
    params = serializers.JSONField(
        help_text="Calculator input parameters"
    )
    result = serializers.JSONField(
        required=False,
        allow_null=True,
        help_text="Cached calculation result"
    )
    is_tracking = serializers.BooleanField(
        default=False,
        help_text="Enable notifications for this calculation"
    )
    is_favorite = serializers.BooleanField(
        default=False,
        help_text="Mark as favorite"
    )
    notification_enabled = serializers.BooleanField(
        default=True,
        help_text="Enable/disable notifications"
    )
    access_count = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    last_accessed = serializers.DateTimeField(read_only=True)
    
    def create(self, validated_data):
        from calculators.models import SavedCalculation
        return SavedCalculation.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ScheduledNotificationSerializer(serializers.Serializer):
    """Serializer for ScheduledNotification model"""
    id = serializers.IntegerField(read_only=True)
    calculation_id = serializers.IntegerField(source='calculation.id', read_only=True)
    notification_type = serializers.CharField(max_length=50)
    priority = serializers.ChoiceField(
        choices=['low', 'medium', 'high', 'urgent'],
        default='medium'
    )
    scheduled_date = serializers.DateField()
    scheduled_time = serializers.TimeField()
    title = serializers.CharField(max_length=200)
    message = serializers.CharField()
    action_url = serializers.CharField(
        max_length=500,
        required=False,
        allow_null=True
    )
    sent = serializers.BooleanField(read_only=True)
    sent_at = serializers.DateTimeField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

