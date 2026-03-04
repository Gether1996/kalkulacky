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
    
    def increment_views(self):
        """Increment view counter"""
        self.view_count += 1
        self.save(update_fields=['view_count'])

