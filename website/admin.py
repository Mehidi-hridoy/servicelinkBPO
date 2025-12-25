from django.contrib import admin
from django.utils import timezone

from .models import (
    HeroSlide,
    ServiceCategory,
    Service,
    ServiceHero,
    ServiceDetailHero,
    ProcessStep,
    AboutHero,
    AboutContent,
    ContactHero,
    ContactInfo,
    ContactSubmission,
    ConsultationRequest,
    ServiceInquiry,
    FAQ,
)

from django.utils.html import format_html
# =========================
# HERO & CORE SECTIONS
# =========================


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'image_preview', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    ordering = ('order',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 80px; height:auto; border-radius:4px;" />', obj.image.url)
        return "-"
    image_preview.short_description = 'Image'


@admin.register(ServiceHero)
class ServiceHeroAdmin(admin.ModelAdmin):
    list_display = ('title', 'page_type', 'is_active', 'updated_at')
    list_filter = ('page_type', 'is_active')
    search_fields = ('title', 'subtitle')


@admin.register(ServiceDetailHero)
class ServiceDetailHeroAdmin(admin.ModelAdmin):
    list_display = ('service', 'show_default')
    search_fields = ('service__title',)


@admin.register(AboutHero)
class AboutHeroAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')
    list_filter = ('is_active',)


@admin.register(ContactHero)
class ContactHeroAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'updated_at')
    list_filter = ('is_active',)


# =========================
# SERVICES
# =========================

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'icon')
    list_editable = ('order',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'order','image', 'is_featured')
    list_filter = ('category', 'is_featured')
    list_editable = ('order', 'is_featured')
    search_fields = ('title', 'short_description')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('order',)


# =========================
# PROCESS & ABOUT
# =========================

@admin.register(ProcessStep)
class ProcessStepAdmin(admin.ModelAdmin):
    list_display = ('step_number', 'title')
    ordering = ('step_number',)


@admin.register(AboutContent)
class AboutContentAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


# =========================
# CONTACT INFO
# =========================

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'email', 'phone')


# =========================
# CONTACT & LEADS
# =========================

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'email', 'phone',
        'service_interest_display', 'status',
        'submitted_at_display'
    )
    list_filter = ('status', 'submitted_at', 'service_interest')
    search_fields = ('name', 'email', 'phone', 'company', 'message')
    readonly_fields = ('submitted_at', 'ip_address', 'user_agent')
    list_per_page = 20

    def service_interest_display(self, obj):
        return obj.get_service_display()
    service_interest_display.short_description = 'Service Interest'

    def submitted_at_display(self, obj):
        return obj.submitted_at.strftime('%Y-%m-%d %H:%M')
    submitted_at_display.short_description = 'Submitted'


@admin.register(ConsultationRequest)
class ConsultationRequestAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'email',
        'service_display', 'company_size_display',
        'status', 'submitted_at_display'
    )
    list_filter = ('status', 'submitted_at', 'service_interest', 'company_size')
    search_fields = ('name', 'email', 'phone', 'company_name')
    readonly_fields = ('submitted_at',)
    list_editable = ('status',)
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
    list_display = (
        'name', 'email',
        'service_info', 'team_size',
        'status', 'submitted_at_display'
    )
    list_filter = ('status', 'service_type', 'team_size', 'submitted_at')
    search_fields = ('name', 'email', 'phone', 'company')
    readonly_fields = ('submitted_at',)
    list_editable = ('status',)
    list_per_page = 20

    def service_info(self, obj):
        return obj.specific_service.title if obj.specific_service else obj.get_service_type_display()
    service_info.short_description = 'Service'

    def submitted_at_display(self, obj):
        return obj.submitted_at.strftime('%Y-%m-%d %H:%M')
    submitted_at_display.short_description = 'Submitted'


# =========================
# FAQ
# =========================

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'order', 'is_active')
    list_filter = ('category', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('question', 'answer')
    ordering = ('order',)
    list_per_page = 20


# =========================
# ADMIN BRANDING
# =========================

admin.site.site_header = "ServiceLink BPO Admin"
admin.site.site_title = "ServiceLink BPO Admin Portal"
admin.site.index_title = "Welcome to ServiceLink BPO Admin"

