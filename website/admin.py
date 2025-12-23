from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html

from .models import (
    HeroSlide, ServiceCategory, Service,
    ProcessStep, AboutContent, ContactInfo,
    ContactSubmission, ConsultationRequest, ServiceInquiry
)


# =========================
# CORE WEBSITE MODELS
# =========================

@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'icon']
    list_editable = ['order']
    prepopulated_fields = {'slug': ['name']}


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'order', 'is_featured']
    list_filter = ['category', 'is_featured']
    list_editable = ['order', 'is_featured']
    search_fields = ['title', 'short_description']
    prepopulated_fields = {'slug': ['title']}


admin.site.register(ProcessStep)
admin.site.register(AboutContent)
admin.site.register(ContactInfo)


# =========================
# CONTACT & LEAD MODELS
# =========================

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'email', 'phone',
        'service_interest_display', 'status',
        'submitted_at_display'
    ]
    list_filter = ['status', 'submitted_at', 'service_interest']
    search_fields = ['name', 'email', 'phone', 'company', 'message']
    readonly_fields = ['submitted_at', 'ip_address', 'user_agent']
    list_per_page = 20

    def service_interest_display(self, obj):
        return obj.get_service_display()
    service_interest_display.short_description = 'Service Interest'

    def submitted_at_display(self, obj):
        return obj.submitted_at.strftime('%Y-%m-%d %H:%M')
    submitted_at_display.short_description = 'Submitted'

    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-submitted_at')


@admin.register(ConsultationRequest)
class ConsultationRequestAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'email',
        'service_display', 'company_size_display',
        'status', 'submitted_at_display'
    ]
    list_filter = ['status', 'submitted_at', 'service_interest', 'company_size']
    search_fields = ['name', 'email', 'phone', 'company_name']
    readonly_fields = ['submitted_at']
    list_editable = ['status']
    list_per_page = 20

    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'company_name', 'company_size')
        }),
        ('Consultation Details', {
            'fields': ('service_interest', 'requirements', 'preferred_date', 'preferred_time')
        }),
        ('Administration', {
            'fields': ('status', 'notes', 'submitted_at')
        }),
    )

    def service_display(self, obj):
        return obj.get_service_display_name()
    service_display.short_description = 'Service'

    def company_size_display(self, obj):
        return obj.get_company_size_display_name()
    company_size_display.short_description = 'Company Size'

    def submitted_at_display(self, obj):
        return obj.submitted_at.strftime('%Y-%m-%d %H:%M')
    submitted_at_display.short_description = 'Submitted'


@admin.register(ServiceInquiry)
class ServiceInquiryAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'email',
        'service_info', 'team_size',
        'status', 'submitted_at_display'
    ]
    list_filter = ['status', 'service_type', 'team_size', 'submitted_at']
    search_fields = ['name', 'email', 'phone', 'company']
    readonly_fields = ['submitted_at']
    list_editable = ['status']
    list_per_page = 20

    def service_info(self, obj):
        if obj.specific_service:
            return obj.specific_service.title
        return obj.get_service_type_display()
    service_info.short_description = 'Service'

    def submitted_at_display(self, obj):
        return obj.submitted_at.strftime('%Y-%m-%d %H:%M')
    submitted_at_display.short_description = 'Submitted'


# =========================
# ADMIN BRANDING
# =========================

admin.site.site_header = "ServiceLink BPO Admin"
admin.site.site_title = "ServiceLink BPO Admin Portal"
admin.site.index_title = "Welcome to ServiceLink BPO Admin"


from django.contrib import admin
from .models import (
    HeroSlide, ServiceCategory, Service, ProcessStep, 
    AboutContent, ContactInfo, ContactSubmission, 
    ConsultationRequest, ServiceInquiry, FAQ  # Add FAQ
)

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'order', 'is_active']
    list_filter = ['category', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['question', 'answer']
    list_per_page = 20

