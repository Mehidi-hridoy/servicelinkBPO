from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from .models import (
    HeroSlide, ServiceCategory, Service, 
    ProcessStep, AboutContent, ContactInfo,
    ContactSubmission, ConsultationRequest, ServiceInquiry, FAQ
)

from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.contrib import messages

from .forms import ContactForm, ConsultationForm, ServiceInquiryForm

# Update your HomeView to include ConsultationForm
class HomeView(TemplateView):
    template_name = 'website/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hero_slides'] = HeroSlide.objects.filter(is_active=True)
        context['categories'] = ServiceCategory.objects.all()[:6]
        context['featured_services'] = Service.objects.filter(is_featured=True)
        context['process_steps'] = ProcessStep.objects.all()
        context['about_content'] = AboutContent.objects.first()
        context['contact_info'] = ContactInfo.objects.first()
        context['consultation_form'] = ConsultationForm()
        return context

class AboutView(TemplateView):
    template_name = 'website/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['about_content'] = AboutContent.objects.first()
        context['process_steps'] = ProcessStep.objects.all()
        return context

class ServicesView(ListView):
    model = ServiceCategory
    template_name = 'website/services.html'
    context_object_name = 'categories'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_services'] = Service.objects.all()
        return context


def error_404_view(request, exception):
    return render(request, 'website/error.html', status=404)

def error_500_view(request):
    return render(request, 'website/error.html', status=500)

# Update the form submission views to use forms

def submit_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                # Save the form data
                submission = form.save(commit=False)
                
                # Add additional data
                submission.ip_address = request.META.get('REMOTE_ADDR')
                submission.user_agent = request.META.get('HTTP_USER_AGENT', '')
                submission.save()
                
                # Send email notification
                if hasattr(settings, 'EMAIL_HOST_USER') and settings.EMAIL_HOST_USER:
                    try:
                        send_mail(
                            subject=f'New Contact Form Submission from {submission.name}',
                            message=f"""
New contact form submission:

Name: {submission.name}
Email: {submission.email}
Phone: {submission.phone}
Company: {submission.company}
Service Interest: {submission.get_service_display()}
Message: {submission.message}

Submitted at: {submission.submitted_at}
                            """,
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=[settings.ADMIN_EMAIL],
                            fail_silently=True,
                        )
                    except Exception as e:
                        print(f"Email sending failed: {e}")
                        # Continue even if email fails
                
                return JsonResponse({
                    'success': True,
                    'message': 'Thank you for your message! We will contact you within 2 business hours.'
                })
                
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'message': f'An error occurred: {str(e)}'
                })
        else:
            # Form validation failed
            errors = form.errors.get_json_data()
            return JsonResponse({
                'success': False,
                'message': 'Please correct the errors below.',
                'errors': errors
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    })


def submit_consultation(request):
    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        if form.is_valid():
            try:
                # Save the form data
                consultation = form.save()
                
                # Send email notification
                if hasattr(settings, 'EMAIL_HOST_USER') and settings.EMAIL_HOST_USER:
                    try:
                        send_mail(
                            subject=f'New Consultation Request from {consultation.name}',
                            message=f"""
New consultation request:

Name: {consultation.name}
Email: {consultation.email}
Phone: {consultation.phone}
Company: {consultation.company_name}
Company Size: {consultation.get_company_size_display_name()}
Service Interest: {consultation.get_service_display_name()}
Requirements: {consultation.requirements}
Preferred Date: {consultation.preferred_date}
Preferred Time: {consultation.preferred_time}

Submitted at: {consultation.submitted_at}
                            """,
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=[settings.ADMIN_EMAIL],
                            fail_silently=True,
                        )
                    except Exception as e:
                        print(f"Email sending failed: {e}")
                
                return JsonResponse({
                    'success': True,
                    'message': 'Thank you for your consultation request! Our team will contact you within 24 hours.'
                })
                
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'message': f'An error occurred: {str(e)}'
                })
        else:
            errors = form.errors.get_json_data()
            return JsonResponse({
                'success': False,
                'message': 'Please correct the errors below.',
                'errors': errors
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    })


from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from .models import Service
from .forms import ServiceInquiryForm

def submit_service_inquiry(request, service_slug=None):  # Change parameter to match URL pattern
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    if request.method == 'POST':
        # Get the service - use service_slug parameter
        service = get_object_or_404(Service, slug=service_slug)
        
        # Prepare initial data
        initial_data = {
            'specific_service': service.id,
            'service_type': 'single-service'
        }
        
        form = ServiceInquiryForm(request.POST, initial=initial_data)
        
        if form.is_valid():
            try:
                # Save the form data
                inquiry = form.save()
                
                # Get service name for email
                service_name = inquiry.specific_service.title if inquiry.specific_service else 'Multiple/Custom Services'
                
                # Send email notification
                if hasattr(settings, 'EMAIL_HOST_USER') and settings.EMAIL_HOST_USER:
                    try:
                        send_mail(
                            subject=f'New Service Inquiry for {service_name}',
                            message=f"""
New service inquiry:

Name: {inquiry.name}
Email: {inquiry.email}
Phone: {inquiry.phone}
Company: {inquiry.company}
Service: {service_name}
Team Size: {inquiry.get_team_size_display()}
Budget Range: {inquiry.budget_range}
Timeline: {inquiry.timeline}
Additional Requirements: {inquiry.additional_requirements}

Submitted at: {inquiry.submitted_at}
                            """,
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=[settings.ADMIN_EMAIL],
                            fail_silently=True,
                        )
                    except Exception as e:
                        print(f"Email sending failed: {e}")
                
                # Add Django message
                messages.success(
                    request, 
                    'Thank you for your inquiry! Our sales team will contact you with detailed information.'
                )
                
                if is_ajax:
                    # Build redirect URL
                    redirect_url = reverse('website:service_detail', kwargs={'slug': service_slug})
                    return JsonResponse({
                        'success': True,
                        'message': 'Thank you for your inquiry! Our sales team will contact you with detailed information.',
                        'redirect': True,
                        'redirect_url': redirect_url
                    })
                else:
                    # For non-AJAX submission
                    return redirect('website:service_detail', slug=service_slug)
                
            except Exception as e:
                if is_ajax:
                    return JsonResponse({
                        'success': False,
                        'message': f'An error occurred: {str(e)}'
                    })
                else:
                    messages.error(request, f'An error occurred: {str(e)}')
                    return redirect('website:service_detail', slug=service_slug)
        else:
            if is_ajax:
                errors = form.errors.get_json_data()
                return JsonResponse({
                    'success': False,
                    'message': 'Please correct the errors below.',
                    'errors': errors
                })
            else:
                # For non-AJAX, add errors to messages
                for field, error_list in form.errors.items():
                    for error in error_list:
                        messages.error(request, f"{field}: {error}")
                return redirect('website:service_detail', slug=service_slug)
    
    # GET request
    if is_ajax:
        return JsonResponse({
            'success': False,
            'message': 'Invalid request method'
        })
    return redirect('website:service_detail', slug=service_slug)



# Update your ServiceDetailView to pass the form
class ServiceDetailView(DetailView):
    model = Service
    template_name = 'website/service_detail.html'
    context_object_name = 'service'
    slug_field = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_services'] = Service.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)[:3]
        context['inquiry_form'] = ServiceInquiryForm(
            initial={
                'specific_service': self.object.id,
                'service_type': 'single-service'
            }
        )
        return context


class ContactView(TemplateView):
    template_name = 'website/contact.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_info'] = ContactInfo.objects.first()
        context['contact_form'] = ContactForm()
        context['faqs'] = FAQ.objects.filter(category='contact', is_active=True).order_by('order')
        return context
    
    