from django import forms
from django.core.validators import validate_email
from .models import ContactSubmission, ConsultationRequest, ServiceInquiry, Service

class ContactForm(forms.ModelForm):
    name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Name',
            'required': 'required'
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Email',
            'required': 'required'
        })
    )
    
    phone = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Phone Number',
            'required': 'required'
        })
    )
    
    company = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Company Name'
        })
    )
    
    SERVICE_CHOICES = [
        ('', 'Select a service'),
        ('customer-service', 'Customer Service Staffing'),
        ('back-office', 'Back-Office & Administrative Support'),
        ('finance', 'Finance & Accounting'),
        ('digital-marketing', 'Digital Marketing Staffing'),
        ('it-solutions', 'IT & Technology Solutions'),
        ('data-analytics', 'Data Analytics Services'),
        ('multiple', 'Multiple Services'),
        ('custom', 'Custom Solution'),
    ]
    
    service_interest = forms.ChoiceField(
        choices=SERVICE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'required': 'required'
        })
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Your Message',
            'rows': 5,
            'required': 'required'
        })
    )
    
    privacy_policy = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'required': 'required'
        })
    )
    
    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'phone', 'company', 'service_interest', 'message']
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Basic phone validation - you can add more complex validation if needed
        if len(phone) < 8:
            raise forms.ValidationError("Please enter a valid phone number")
        return phone
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        validate_email(email)  # Django's built-in email validator
        return email


class ConsultationForm(forms.ModelForm):
    name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Name',
            'required': 'required'
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Email',
            'required': 'required'
        })
    )
    
    phone = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Phone Number',
            'required': 'required'
        })
    )
    
    company_name = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Company Name'
        })
    )
    
    COMPANY_SIZE_CHOICES = [
        ('', 'Select company size'),
        ('1-10', '1-10 employees'),
        ('11-50', '11-50 employees'),
        ('51-200', '51-200 employees'),
        ('201-500', '201-500 employees'),
        ('500+', '500+ employees'),
    ]
    
    company_size = forms.ChoiceField(
        choices=COMPANY_SIZE_CHOICES,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'required': 'required'
        })
    )
    
    SERVICE_CHOICES = [
        ('', 'Select service interest'),
        ('customer-service', 'Customer Service Staffing'),
        ('back-office', 'Back-Office & Administrative Support'),
        ('finance', 'Finance & Accounting'),
        ('digital-marketing', 'Digital Marketing Staffing'),
        ('it-solutions', 'IT & Technology Solutions'),
        ('data-analytics', 'Data Analytics Services'),
        ('multiple', 'Multiple Services'),
        ('custom', 'Custom Solution'),
    ]
    
    service_interest = forms.ChoiceField(
        choices=SERVICE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'required': 'required'
        })
    )
    
    requirements = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Tell us about your specific requirements...',
            'rows': 3
        })
    )
    
    preferred_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'placeholder': 'Preferred date for consultation'
        })
    )
    
    preferred_time = forms.TimeField(
        required=False,
        widget=forms.TimeInput(attrs={
            'class': 'form-control',
            'type': 'time',
            'placeholder': 'Preferred time'
        })
    )
    
    class Meta:
        model = ConsultationRequest
        fields = ['name', 'email', 'phone', 'company_name', 'company_size', 
                 'service_interest', 'requirements', 'preferred_date', 'preferred_time']
    
    def clean_preferred_date(self):
        date = self.cleaned_data.get('preferred_date')
        if date:
            from datetime import date as datetime_date
            if date < datetime_date.today():
                raise forms.ValidationError("Please select a future date")
        return date


class ServiceInquiryForm(forms.ModelForm):
    SERVICE_TYPE_CHOICES = [
        ('single-service', 'Single Service'),
        ('multiple-services', 'Multiple Services'),
        ('custom-solution', 'Custom Solution'),
    ]
    
    TEAM_SIZE_CHOICES = [
        ('', 'Select team size'),
        ('1-5', '1-5 team members'),
        ('6-10', '6-10 team members'),
        ('11-20', '11-20 team members'),
        ('20+', '20+ team members'),
    ]
    
    name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Name',
            'required': 'required'
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Email',
            'required': 'required'
        })
    )
    
    phone = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Phone Number',
            'required': 'required'
        })
    )
    
    company = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Company (Optional)'
        })
    )
    
    service_type = forms.ChoiceField(
        choices=SERVICE_TYPE_CHOICES,
        initial='single-service',
        widget=forms.HiddenInput()  # Hidden since we'll set it based on context
    )
    
    # Dynamic queryset for services - we'll set this in the view
    specific_service = forms.ModelChoiceField(
        queryset=Service.objects.all(),
        required=False,
        widget=forms.HiddenInput()
    )
    
    team_size = forms.ChoiceField(
        choices=TEAM_SIZE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'required': 'required'
        })
    )
    
    budget_range = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Budget Range (Optional)'
        })
    )
    
    timeline = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Project Timeline (Optional)'
        })
    )
    
    additional_requirements = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Additional requirements...',
            'rows': 3
        })
    )
    
    class Meta:
        model = ServiceInquiry
        fields = ['name', 'email', 'phone', 'company', 'service_type', 
                 'specific_service', 'team_size', 'budget_range', 
                 'timeline', 'additional_requirements']


class NewsletterSubscriptionForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
            'required': 'required'
        })
    )
    
    name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Name (Optional)'
        })
    )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        validate_email(email)
        return email


class QuickQuoteForm(forms.Form):
    name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Name',
            'required': 'required'
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Email',
            'required': 'required'
        })
    )
    
    phone = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Phone',
            'required': 'required'
        })
    )
    
    SERVICE_CHOICES = [
        ('', 'Select Service Needed'),
        ('customer-service', 'Customer Service Staffing'),
        ('back-office', 'Back-Office Support'),
        ('finance', 'Finance & Accounting'),
        ('digital-marketing', 'Digital Marketing'),
        ('it-solutions', 'IT Solutions'),
        ('data-analytics', 'Data Analytics'),
    ]
    
    service = forms.ChoiceField(
        choices=SERVICE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'required': 'required'
        })
    )
    
    team_size = forms.ChoiceField(
        choices=ServiceInquiryForm.TEAM_SIZE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'required': 'required'
        })
    )
    
    timeline = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Expected Timeline',
            'required': 'required'
        })
    )
    
    message = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Additional details...',
            'rows': 3
        })
    )

    