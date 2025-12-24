from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.utils import timezone


class HeroSlide(models.Model):
    title = models.CharField(max_length=200)
    subtext = models.TextField()
    cta_text = models.CharField(max_length=50, default="Get Started")
    cta_link = models.CharField(max_length=100, default="#")
    image = models.ImageField(upload_to='hero/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title


class ServiceCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    icon = models.CharField(max_length=50, help_text="FontAwesome icon class", 
                           default="fas fa-cogs")
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        verbose_name_plural = "Service Categories"
        ordering = ['order']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Service(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE,   related_name='services')
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.CharField(max_length=300)
    detailed_description = RichTextField()
    features = models.TextField(help_text="Enter features separated by semicolons")
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    order = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['order']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_features_list(self):
        return [feature.strip() for feature in self.features.split(';') if feature.strip()]
    
    def __str__(self):
        return self.title


# models.py - Add these models
class ServiceHero(models.Model):
    PAGE_TYPE_CHOICES = [
        ('list', 'Services List Page'),
        ('detail', 'Service Detail Page'),
    ]
    
    page_type = models.CharField(max_length=20, choices=PAGE_TYPE_CHOICES, default='list')
    title = models.CharField(max_length=200)
    subtitle = models.TextField()
    background_image = models.ImageField(upload_to='service_hero/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Service Hero Sections"
    
    def __str__(self):
        return f"{self.get_page_type_display()} - {self.title}"
    
    def save(self, *args, **kwargs):
        # Ensure only one active hero per page type
        if self.is_active:
            ServiceHero.objects.filter(page_type=self.page_type, is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)


class ServiceDetailHero(models.Model):
    service = models.OneToOneField(Service, on_delete=models.CASCADE, related_name='hero')
    custom_title = models.CharField(max_length=200, blank=True)
    custom_subtitle = models.TextField(blank=True)
    custom_image = models.ImageField(upload_to='service_detail_hero/', blank=True, null=True)
    show_default = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Service Detail Heroes"
    
    def __str__(self):
        return f"Hero for {self.service.title}"

class ProcessStep(models.Model):
    step_number = models.IntegerField()
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="FontAwesome icon class")
    
    class Meta:
        ordering = ['step_number']
    
    def __str__(self):
        return f"Step {self.step_number}: {self.title}"


# Add this to your existing models.py, before the AboutContent model

class AboutHero(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    background_image = models.ImageField(upload_to='about/hero/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "About Hero Section"
        verbose_name_plural = "About Hero Section"
    
    def __str__(self):
        return self.title


class AboutContent(models.Model):
    title = models.CharField(max_length=200)
    tagline = models.CharField(max_length=300)
    content = RichTextField()
    image = models.ImageField(upload_to='about/', blank=True, null=True)
    
    def __str__(self):
        return self.title


class ContactHero(models.Model):
    title = models.CharField(max_length=200, default="Contact ServiceLink BPO")
    subtitle = models.TextField(default="Get in touch with our expert team. We're here to help you streamline your business operations.")
    background_image = models.ImageField(upload_to='hero_images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Contact Hero Sections"
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Ensure only one active hero at a time
        if self.is_active:
            ContactHero.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)


class ContactInfo(models.Model):
    company_name = models.CharField(max_length=200)
    address = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    whatsapp = models.CharField(max_length=50, blank=True)
    google_map_embed = models.TextField(blank=True, help_text="Google Maps embed code")
    
    class Meta:
        verbose_name_plural = "Contact Information"
    
    def __str__(self):
        return self.company_name
    
# Add these new models to your models.py

class ContactSubmission(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
        ('closed', 'Closed'),
    ]
    
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    company = models.CharField(max_length=200, blank=True)
    service_interest = models.CharField(max_length=100, blank=True)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    submitted_at = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-submitted_at']
        verbose_name_plural = "Contact Submissions"
    
    def __str__(self):
        return f"{self.name} - {self.submitted_at.strftime('%Y-%m-%d %H:%M')}"
    
    def get_service_display(self):
        service_mapping = {
            'customer-service': 'Customer Service Staffing',
            'back-office': 'Back-Office & Administrative Support',
            'finance': 'Finance & Accounting',
            'digital-marketing': 'Digital Marketing Staffing',
            'it-solutions': 'IT & Technology Solutions',
            'data-analytics': 'Data Analytics Services',
            'multiple': 'Multiple Services',
            'custom': 'Custom Solution',
        }
        return service_mapping.get(self.service_interest, self.service_interest)


class ConsultationRequest(models.Model):
    SERVICE_CHOICES = [
        ('customer-service', 'Customer Service Staffing'),
        ('back-office', 'Back-Office & Administrative Support'),
        ('finance', 'Finance & Accounting'),
        ('digital-marketing', 'Digital Marketing Staffing'),
        ('it-solutions', 'IT & Technology Solutions'),
        ('data-analytics', 'Data Analytics Services'),
        ('multiple', 'Multiple Services'),
        ('custom', 'Custom Solution'),
    ]
    
    COMPANY_SIZE_CHOICES = [
        ('1-10', '1-10 employees'),
        ('11-50', '11-50 employees'),
        ('51-200', '51-200 employees'),
        ('201-500', '201-500 employees'),
        ('500+', '500+ employees'),
    ]
    
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    company_name = models.CharField(max_length=200, blank=True)
    company_size = models.CharField(max_length=20, choices=COMPANY_SIZE_CHOICES, blank=True)
    service_interest = models.CharField(max_length=100, choices=SERVICE_CHOICES)
    requirements = models.TextField(blank=True)
    preferred_date = models.DateField(null=True, blank=True)
    preferred_time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, default='new')
    submitted_at = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True, help_text="Internal notes for the sales team")
    
    class Meta:
        ordering = ['-submitted_at']
        verbose_name_plural = "Consultation Requests"
    
    def __str__(self):
        return f"Consultation: {self.name} - {self.service_interest}"
    
    def get_service_display_name(self):
        return dict(self.SERVICE_CHOICES).get(self.service_interest, self.service_interest)
    
    def get_company_size_display_name(self):
        return dict(self.COMPANY_SIZE_CHOICES).get(self.company_size, self.company_size)


class ServiceInquiry(models.Model):
    SERVICE_TYPE_CHOICES = [
        ('single-service', 'Single Service'),
        ('multiple-services', 'Multiple Services'),
        ('custom-solution', 'Custom Solution'),
    ]
    
    TEAM_SIZE_CHOICES = [
        ('1-5', '1-5 team members'),
        ('6-10', '6-10 team members'),
        ('11-20', '11-20 team members'),
        ('20+', '20+ team members'),
    ]
    
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    company = models.CharField(max_length=200, blank=True)
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPE_CHOICES, default='single-service')
    specific_service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    team_size = models.CharField(max_length=20, choices=TEAM_SIZE_CHOICES)
    additional_requirements = models.TextField(blank=True)
    budget_range = models.CharField(max_length=100, blank=True)
    timeline = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, default='new')
    submitted_at = models.DateTimeField(default=timezone.now)
    follow_up_date = models.DateField(null=True, blank=True)
    
    class Meta:
        ordering = ['-submitted_at']
        verbose_name_plural = "Service Inquiries"
    
    def __str__(self):
        service_name = self.specific_service.title if self.specific_service else self.service_type
        return f"Inquiry: {self.name} - {service_name}"


# Add to your existing models.py
class FAQ(models.Model):
    CATEGORY_CHOICES = [
        ('general', 'General'),
        ('services', 'Services'),
        ('pricing', 'Pricing'),
        ('contact', 'Contact'),
        ('technical', 'Technical'),
        ('process', 'Process'),
    ]
    
    question = models.CharField(max_length=500)
    answer = RichTextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='general')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order', 'category']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'
    
    def __str__(self):
        return f"{self.question[:50]}..."
    

