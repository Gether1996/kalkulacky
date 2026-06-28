from django.contrib import admin
from .models import BlogCategory, BlogPost, Lead, AffiliateClick, DataReport, UserReminder


@admin.register(UserReminder)
class UserReminderAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'category', 'remind_date', 'sent', 'email_enabled']
    list_filter = ['category', 'sent', 'email_enabled', 'remind_date']
    search_fields = ['title', 'note', 'user__email']
    date_hierarchy = 'remind_date'


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon', 'order', 'created_at']
    list_editable = ['order']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    ordering = ['order', 'name']


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'published_at', 'view_count', 'created_at']
    list_filter = ['status', 'category', 'related_calculator', 'published_at']
    search_fields = ['title', 'excerpt', 'content_html', 'tags']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    ordering = ['-published_at', '-created_at']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'slug', 'excerpt', 'category', 'status')
        }),
        ('Content', {
            'fields': ('content_html',)
        }),
        ('SEO & Meta', {
            'fields': ('meta_keywords', 'featured_image_url')
        }),
        ('Classification', {
            'fields': ('tags', 'related_calculator')
        }),
        ('Publishing', {
            'fields': ('published_at',)
        }),
        ('Analytics', {
            'fields': ('view_count',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['view_count']


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'vertical', 'status', 'region', 'email', 'phone',
                    'estimated_value', 'created_at']
    list_filter = ['vertical', 'status', 'calculator_type', 'created_at']
    list_editable = ['status', 'estimated_value']
    search_fields = ['name', 'email', 'phone', 'region', 'sold_to', 'message']
    date_hierarchy = 'created_at'
    readonly_fields = ['session_key', 'ip_address', 'user_agent', 'source_url',
                       'context', 'created_at', 'updated_at']
    fieldsets = (
        ('Lead', {'fields': ('vertical', 'calculator_type', 'status',
                             'estimated_value', 'sold_to')}),
        ('Kontakt', {'fields': ('name', 'email', 'phone', 'region', 'message',
                                'consent')}),
        ('Kontext výpočtu', {'fields': ('context',), 'classes': ('collapse',)}),
        ('Atribúcia', {'fields': ('source_url', 'session_key', 'ip_address',
                                  'user_agent', 'created_at', 'updated_at'),
                       'classes': ('collapse',)}),
    )


@admin.register(AffiliateClick)
class AffiliateClickAdmin(admin.ModelAdmin):
    list_display = ['partner', 'offer_id', 'calculator_type', 'created_at']
    list_filter = ['partner', 'calculator_type', 'created_at']
    search_fields = ['partner', 'offer_id', 'target_url']
    date_hierarchy = 'created_at'
    readonly_fields = [f.name for f in AffiliateClick._meta.fields]


@admin.register(DataReport)
class DataReportAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'calculator_type', 'status', 'emailed',
                    'reporter_email', 'locale', 'created_at']
    list_filter = ['status', 'calculator_type', 'emailed', 'locale', 'created_at']
    list_editable = ['status']
    search_fields = ['message', 'reporter_email', 'page_url', 'calculator_type']
    date_hierarchy = 'created_at'
    readonly_fields = ['calculator_type', 'page_url', 'message', 'reporter_email',
                       'locale', 'emailed', 'session_key', 'ip_address',
                       'user_agent', 'created_at', 'updated_at']
    fieldsets = (
        ('Hlásenie', {'fields': ('calculator_type', 'page_url', 'message',
                                 'reporter_email', 'locale')}),
        ('Stav', {'fields': ('status', 'emailed', 'admin_notes')}),
        ('Atribúcia', {'fields': ('session_key', 'ip_address', 'user_agent',
                                  'created_at', 'updated_at'),
                       'classes': ('collapse',)}),
    )

