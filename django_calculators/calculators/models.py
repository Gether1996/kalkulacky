from django.db import models
from django.utils.text import slugify

"""
Blog Models for Kalkulačky.sk

Stores blog posts about tax changes, calculator tutorials, Slovak finance tips, etc.
Supports HTML content for rich formatting and SEO optimization.
"""


class BlogCategory(models.Model):
    """
    Blog categories for organizing content.
    Examples: "Dane 2026", "Kalkulačky návody", "Slovenské financie", "Zmeny zákonov"
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Category name (e.g., 'Dane 2026', 'Calculators')"
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        help_text="URL-friendly slug (auto-generated)"
    )
    description = models.TextField(
        blank=True,
        help_text="Category description for SEO"
    )
    color = models.CharField(
        max_length=7,
        default='#3B82F6',
        help_text="Hex color for UI (e.g., #3B82F6)"
    )
    icon = models.CharField(
        max_length=50,
        default='📰',
        help_text="Emoji icon for category"
    )
    order = models.IntegerField(
        default=0,
        help_text="Display order (lower = first)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Blog Category'
        verbose_name_plural = 'Blog Categories'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class BlogPost(models.Model):
    """
    Blog posts with HTML content support.
    
    Features:
    - Rich HTML content
    - SEO metadata
    - Related calculators
    - Publishing workflow
    """
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    # Basic Info
    title = models.CharField(
        max_length=200,
        help_text="Blog post title (SEO optimized)"
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        help_text="URL slug (auto-generated from title)"
    )
    excerpt = models.TextField(
        max_length=300,
        help_text="Short description for cards and SEO meta description"
    )
    
    # Content
    content_html = models.TextField(
        help_text="Full HTML content of the blog post"
    )
    
    # SEO & Metadata
    meta_keywords = models.CharField(
        max_length=255,
        blank=True,
        help_text="SEO keywords (comma-separated)"
    )
    featured_image_url = models.URLField(
        blank=True,
        help_text="URL to featured image (optional)"
    )
    
    # Categorization
    category = models.ForeignKey(
        BlogCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts',
        help_text="Primary category"
    )
    tags = models.CharField(
        max_length=200,
        blank=True,
        help_text="Comma-separated tags (e.g., 'dane, 2026, progresívne zdanenie')"
    )
    
    # Related Calculator
    related_calculator = models.CharField(
        max_length=50,
        blank=True,
        choices=[
            ('salary', 'Čistá mzda'),
            ('mortgage', 'Hypotéka'),
            ('vat', 'DPH'),
            ('loan', 'Úver'),
            ('bmi', 'BMI'),
        ],
        help_text="Link to a specific calculator (optional)"
    )
    
    # Publishing
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )
    published_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Publication date/time"
    )
    
    # Analytics
    view_count = models.IntegerField(
        default=0,
        help_text="Number of views"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-published_at', '-created_at']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'
        indexes = [
            models.Index(fields=['-published_at']),
            models.Index(fields=['status']),
            models.Index(fields=['slug']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def get_tags_list(self):
        """Return tags as a list"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []


# ============================================================================
# SAVED CALCULATIONS & NOTIFICATIONS MODELS
# ============================================================================

class SavedCalculation(models.Model):
    """
    Saved calculator results with tracking and notification support.
    Supports both anonymous (session-based) and authenticated users (future).
    """
    CALCULATOR_TYPES = [
        ('pregnancy', 'Tehotenstvo'),
        ('vacation', 'Dovolenka'),
        ('mortgage', 'Hypotéka'),
        ('loan', 'Úver'),
        ('salary', 'Čistá mzda'),
        ('vat', 'DPH'),
        ('pension', 'Dôchodok'),
        ('freelancer_tax', 'SZČO dane'),
        ('bmi', 'BMI'),
        ('bmr', 'BMR'),
        ('energy', 'Energia'),
        ('sick_leave', 'Pracovná neschopnosť (PN)'),
        ('parental_benefit', 'Rodičovský príspevok'),
        ('fuel_cost', 'Spotreba paliva'),
        ('percentage', 'Percentá'),
        ('payment', 'Platobná kalkulačka'),
        ('inflation', 'Inflácia'),
        ('roi', 'ROI'),
        ('hours_worked', 'Odpracované hodiny'),
        ('unit_converter', 'Konvertor jednotiek'),
        ('car_leasing', 'Auto lízing'),
        ('area_volume', 'Plocha a objem'),
        ('split_bill', 'Rozdelenie účtu'),
    ]
    
    # Identification (support anonymous users via session_key)
    session_key = models.CharField(
        max_length=100,
        db_index=True,
        help_text="Session key for anonymous users"
    )
    email = models.EmailField(
        null=True,
        blank=True,
        help_text="Optional email for notifications (even without account)"
    )
    
    # Calculation details
    calculator_type = models.CharField(
        max_length=50,
        choices=CALCULATOR_TYPES
    )
    name = models.CharField(
        max_length=200,
        help_text="User-defined name (e.g., 'Moje tehotenstvo - termín júl 2026')"
    )
    params = models.JSONField(
        help_text="Calculator input parameters"
    )
    result = models.JSONField(
        null=True,
        blank=True,
        help_text="Cached calculation result"
    )
    
    # Tracking & notifications
    is_tracking = models.BooleanField(
        default=False,
        help_text="Whether user wants notifications for this calculation"
    )
    is_favorite = models.BooleanField(
        default=False,
        help_text="User-marked favorite for quick access"
    )
    notification_enabled = models.BooleanField(
        default=True,
        help_text="Enable/disable notifications for this calculation"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    last_accessed = models.DateTimeField(auto_now=True)
    access_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-last_accessed', '-created_at']
        verbose_name = 'Saved Calculation'
        verbose_name_plural = 'Saved Calculations'
        indexes = [
            models.Index(fields=['session_key', 'calculator_type']),
            models.Index(fields=['session_key', 'is_tracking']),
            models.Index(fields=['email']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.get_calculator_type_display()})"
    
    def increment_access(self):
        """Increment access counter"""
        self.access_count += 1
        self.save(update_fields=['access_count', 'last_accessed'])


class ScheduledNotification(models.Model):
    """
    Scheduled notifications for tracked calculations.
    Generated based on calculator type and user preferences.
    """
    NOTIFICATION_TYPES = [
        # Pregnancy
        ('pregnancy_week', 'Týždenná aktualizácia tehotenstva'),
        ('pregnancy_milestone', 'Míľnik tehotenstva'),
        ('trimester_change', 'Zmena trimestra'),
        ('prenatal_visit', 'Prenatálna kontrola'),
        ('due_date_approaching', 'Blíži sa termín pôrodu'),
        
        # Vacation
        ('vacation_expiry', 'Dovolenka prepadne'),
        ('vacation_quarterly', 'Štvrťročná kontrola dovolenky'),
        ('birthday_33', 'Prírastok dovolenky (33 rokov)'),
        ('vacation_reminder', 'Pripomienka dovolenky'),
        
        # Mortgage/Loan
        ('payment_due', 'Splátka splatná'),
        ('rate_change', 'Zmena úrokovej sadzby'),
        ('milestone_paid', 'Míľnik splatenia'),
        ('amortization_alert', 'Alert amortizácie'),
        ('extra_payment_tip', 'Tip na nadplatenie'),
        
        # Other
        ('generic_reminder', 'Všeobecná pripomienka'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Nízka'),
        ('medium', 'Stredná'),
        ('high', 'Vysoká'),
        ('urgent', 'Urgentná'),
    ]
    
    # Related calculation
    calculation = models.ForeignKey(
        SavedCalculation,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    
    # Notification details
    notification_type = models.CharField(
        max_length=50,
        choices=NOTIFICATION_TYPES
    )
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='medium'
    )
    
    # Scheduling
    scheduled_date = models.DateField()
    scheduled_time = models.TimeField(default='09:00:00')
    
    # Message content
    title = models.CharField(max_length=200)
    message = models.TextField()
    action_url = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        help_text="URL to navigate on click (e.g., /calculator/pregnancy)"
    )
    
    # Status
    sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(
        null=True,
        blank=True,
        help_text="Error message if sending failed"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['scheduled_date', 'scheduled_time', '-priority']
        verbose_name = 'Scheduled Notification'
        verbose_name_plural = 'Scheduled Notifications'
        indexes = [
            models.Index(fields=['scheduled_date', 'sent']),
            models.Index(fields=['calculation', 'notification_type']),
            models.Index(fields=['sent', 'scheduled_date']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.scheduled_date}"
    
    def mark_sent(self):
        """Mark notification as sent"""
        from datetime import datetime
        self.sent = True
        self.sent_at = datetime.now()
        self.save(update_fields=['sent', 'sent_at'])
    
    def mark_failed(self, error):
        """Mark notification as failed with error message"""
        self.error_message = str(error)
        self.save(update_fields=['error_message'])


# ============================================================================
# MONETIZATION MODELS (lead-gen + affiliate tracking)
# ============================================================================

class Lead(models.Model):
    """
    A qualified lead captured from a calculator (e.g. mortgage broker request,
    solar/heat-pump installer quote, accounting-software enquiry).

    Lead-gen is the single highest-value monetization model for these calculators
    (€3-40 per qualified lead). Each lead stores the calculator context + the
    user's calculation snapshot so it can be sold/routed to a partner with full
    qualifying detail.
    """

    # Which vertical / partner program this lead belongs to. Keep loose (CharField)
    # so new verticals can be added without a migration.
    VERTICAL_CHOICES = [
        ('mortgage', 'Hypotéka — broker'),
        ('solar', 'Fotovoltika — montážna firma'),
        ('heat_pump', 'Tepelné čerpadlo — montážna firma'),
        ('renovation', 'Obnova domu — dotácie/firma'),
        ('insurance_car', 'PZP / havarijné poistenie'),
        ('accounting', 'Účtovný softvér / účtovník (SZČO)'),
        ('pension', 'Dôchodok / sporenie'),
        ('energy', 'Dodávateľ energií'),
        ('loan', 'Spotrebný úver'),
        ('other', 'Iné'),
    ]

    STATUS_CHOICES = [
        ('new', 'Nový'),
        ('contacted', 'Kontaktovaný'),
        ('sold', 'Predaný partnerovi'),
        ('converted', 'Skonvertovaný'),
        ('rejected', 'Zamietnutý / nekvalitný'),
    ]

    vertical = models.CharField(
        max_length=40,
        choices=VERTICAL_CHOICES,
        db_index=True,
        help_text="Lead vertical / partner program",
    )
    calculator_type = models.CharField(
        max_length=50,
        blank=True,
        help_text="Calculator that produced the lead (e.g. 'mortgage')",
    )

    # Contact details
    name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    region = models.CharField(
        max_length=100,
        blank=True,
        help_text="City / region — important for routing to local providers",
    )
    message = models.TextField(blank=True)

    # Qualifying context — the calculation snapshot that makes the lead valuable
    context = models.JSONField(
        null=True,
        blank=True,
        help_text="Calculation inputs/results that qualify the lead (e.g. loan amount, kWp)",
    )

    consent = models.BooleanField(
        default=False,
        help_text="User consented to be contacted (GDPR)",
    )

    # Sales / routing
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='new', db_index=True
    )
    estimated_value = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True,
        help_text="Estimated € value of this lead",
    )
    sold_to = models.CharField(
        max_length=150, blank=True, help_text="Partner the lead was sold/routed to"
    )

    # Attribution / anti-spam
    source_url = models.CharField(max_length=500, blank=True)
    session_key = models.CharField(max_length=100, blank=True, db_index=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=300, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Lead'
        verbose_name_plural = 'Leads'
        indexes = [
            models.Index(fields=['vertical', 'status']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        who = self.name or self.email or self.phone or 'anonym'
        return f"[{self.get_vertical_display()}] {who} ({self.status})"


class AffiliateClick(models.Model):
    """
    Tracks outbound clicks on affiliate/partner CTAs so partner payouts and
    EPC (earnings per click) can be reconciled and the best-performing offers
    surfaced. Lightweight by design — one row per click.
    """
    partner = models.CharField(max_length=100, db_index=True)
    offer_id = models.CharField(
        max_length=100, db_index=True,
        help_text="Identifier of the affiliate offer/placement",
    )
    calculator_type = models.CharField(max_length=50, blank=True, db_index=True)
    target_url = models.URLField(max_length=600)

    session_key = models.CharField(max_length=100, blank=True)
    source_url = models.CharField(max_length=500, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=300, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Affiliate Click'
        verbose_name_plural = 'Affiliate Clicks'
        indexes = [
            models.Index(fields=['partner', '-created_at']),
            models.Index(fields=['offer_id', '-created_at']),
        ]

    def __str__(self):
        return f"{self.partner}/{self.offer_id} @ {self.calculator_type}"

