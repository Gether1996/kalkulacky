from django.contrib import admin
from .models import BlogCategory, BlogPost


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

