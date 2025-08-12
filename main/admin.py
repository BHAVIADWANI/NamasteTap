from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile, VisitingCard, DigitalCard, CardAnalytics, CardOrder, CompanyTemplate

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_active', 'created_at')
    list_filter = ('user_type', 'is_active', 'is_staff', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('user_type', 'phone_number', 'date_of_birth', 'profile_picture', 'created_at', 'updated_at')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('email', 'first_name', 'last_name', 'user_type', 'phone_number')
        }),
    )

@admin.register(VisitingCard)
class VisitingCardAdmin(admin.ModelAdmin):
    list_display = ('registration_code', 'card_type', 'status', 'batch_number', 'manufactured_date', 'customer_email')
    list_filter = ('card_type', 'status', 'manufactured_date')
    search_fields = ('registration_code', 'customer_email', 'batch_number')
    readonly_fields = ('card_id', 'registration_code', 'manufactured_date')
    
    fieldsets = (
        ('Card Information', {
            'fields': ('card_id', 'registration_code', 'card_type', 'batch_number')
        }),
        ('Status', {
            'fields': ('status', 'manufactured_date', 'shipped_date', 'delivered_date')
        }),
        ('Customer Information', {
            'fields': ('order_reference', 'customer_email', 'customer_phone')
        }),
    )

@admin.register(DigitalCard)
class DigitalCardAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'user', 'url_slug', 'is_active', 'view_count', 'created_at')
    list_filter = ('is_active', 'created_at', 'visiting_card__card_type')
    search_fields = ('display_name', 'user__username', 'user__email', 'url_slug')
    readonly_fields = ('url_slug', 'view_count', 'created_at', 'updated_at', 'last_viewed')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'visiting_card', 'url_slug', 'card_title', 'is_active')
        }),
        ('Contact Information', {
            'fields': ('display_name', 'job_title', 'company_name', 'email', 'phone', 'bio', 'website', 'location')
        }),
        ('Social Media', {
            'fields': ('linkedin_url', 'twitter_url', 'instagram_url', 'facebook_url')
        }),
        ('Privacy Settings', {
            'fields': ('show_email', 'show_phone', 'show_social_links')
        }),
        ('Analytics', {
            'fields': ('view_count', 'created_at', 'updated_at', 'last_viewed')
        }),
    )

@admin.register(CardAnalytics)
class CardAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('digital_card', 'ip_address', 'country', 'city', 'viewed_at', 'contact_downloaded')
    list_filter = ('viewed_at', 'contact_downloaded', 'country')
    search_fields = ('digital_card__display_name', 'ip_address', 'country', 'city')
    readonly_fields = ('viewed_at',)
    
    fieldsets = (
        ('Card Information', {
            'fields': ('digital_card',)
        }),
        ('Visitor Information', {
            'fields': ('ip_address', 'user_agent', 'referrer', 'country', 'city')
        }),
        ('Interaction Details', {
            'fields': ('viewed_at', 'contact_downloaded', 'links_clicked')
        }),
    )

@admin.register(CardOrder)
class CardOrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'customer_name', 'customer_email', 'status', 'final_amount', 'order_date')
    list_filter = ('status', 'order_date')
    search_fields = ('order_id', 'customer_name', 'customer_email', 'customer_phone')
    readonly_fields = ('order_id', 'order_date')
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_id', 'status', 'order_date')
        }),
        ('Customer Information', {
            'fields': ('customer_name', 'customer_email', 'customer_phone')
        }),
        ('Shipping Address', {
            'fields': ('shipping_address', 'city', 'state', 'pincode')
        }),
        ('Order Items', {
            'fields': ('pvc_cards', 'wood_cards', 'metal_cards', 'pvc_standees', 'wood_standees', 'metal_standees')
        }),
        ('Pricing', {
            'fields': ('total_amount', 'discount_amount', 'final_amount')
        }),
        ('Tracking', {
            'fields': ('shipped_date', 'delivered_date', 'tracking_number', 'notes')
        }),
    )


@admin.register(CompanyTemplate)
class CompanyTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'template_type', 'is_active', 'is_premium', 'created_at')
    list_filter = ('template_type', 'is_active', 'is_premium', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('slug', 'template_folder', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'template_type', 'description')
        }),
        ('Template Configuration', {
            'fields': ('primary_color', 'secondary_color', 'font_family')
        }),
        ('Template Content', {
            'fields': ('html_template', 'css_content', 'js_content'),
            'classes': ('collapse',)
        }),
        ('Settings', {
            'fields': ('is_active', 'is_premium', 'thumbnail')
        }),
        ('System Fields', {
            'fields': ('template_folder', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Create template files when saving
        obj.create_template_files()


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile)
