from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from .models import (
    HeroSlide, ServiceCategory, Service, 
    ProcessStep, AboutContent, ContactInfo,
    ContactSubmission, ConsultationRequest, ServiceInquiry, FAQ,ServiceDetailHero,ServiceHero
)
# views.py - Update submit_service_inquiry function
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from .forms import ServiceInquiryForm
from .models import Service

# views.py - ContactView with fixed form_invalid method
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import ContactHero, ContactInfo, FAQ
from .forms import ContactForm
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from .models import Service
from .forms import ServiceInquiryForm
from django.views.generic import TemplateView
from .models import AboutHero, AboutContent, ProcessStep  # Add AboutHero import

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
        # Get hero section or create a default one
        hero = AboutHero.objects.filter(is_active=True).first()
        if not hero:
            hero = AboutHero.objects.create(
                title="About ServiceLink BPO",
                subtitle="Your Trusted Partner in Business Process Outsourcing",
                is_active=True
            )
        
        # Get about content or create default
        about_content = AboutContent.objects.first()
        if not about_content:
            about_content = AboutContent.objects.create(
                title="About Our Company",
                tagline="Delivering Excellence in BPO Services",
                content="<p>Your default about content goes here...</p>"
            )
        
        context['hero'] = hero
        context['about_content'] = about_content
        context['process_steps'] = ProcessStep.objects.all().order_by('step_number')
        return context


class ContactView(FormView):
    template_name = 'website/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('website:contact')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get contact hero section or create a default one
        contact_hero = ContactHero.objects.filter(is_active=True).first()
        if not contact_hero:
            contact_hero = ContactHero.objects.create(
                title="Contact ServiceLink BPO",
                subtitle="Your Trusted Partner in Business Process Outsourcing",
                is_active=True
            )
        
        # Get contact info or create default
        contact_info = ContactInfo.objects.first()
        if not contact_info:
            contact_info = ContactInfo.objects.create(
                company_name="ServiceLink BPO",
                address="123 Business Avenue\nSuite 100\nNew York, NY 10001",
                email="info@servicelinkbpo.com",
                phone="+1 (555) 123-4567",
                whatsapp="+1 (555) 123-4567",
                google_map_embed='<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3024.177858804427!2d-73.98784468459436!3d40.70555197933217!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x89c25a315cdf4c9b%3A0x8b934de5cae6f7a!2sWall%20St%2C New York, NY, USA!5e0!3m2!1sen!2s!4v1648158082355!5m2!1sen!2s" width="100%" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>'
            )
        
        context['contact_hero'] = contact_hero
        context['contact_info'] = contact_info
        context['faqs'] = FAQ.objects.filter(category='contact', is_active=True).order_by('order')
        return context
    
    def form_valid(self, form):
        # Save the contact submission
        submission = form.save(commit=False)
        
        # Get user IP and user agent
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        
        submission.ip_address = ip
        submission.user_agent = self.request.META.get('HTTP_USER_AGENT', '')
        submission.save()
        
        messages.success(self.request, 'Thank you for your message! We will get back to you within 24 hours.')
        return super().form_valid(form)
    
    # FIXED METHOD - Remove the extra 'self' argument
    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)  # Only pass 'form'
    


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


# views.py
def submit_service_inquiry(request, service_slug=None):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    if request.method == 'POST':
        # Print debug info
        print("=== DEBUG FORM SUBMISSION ===")
        print(f"Service slug: {service_slug}")
        print(f"POST data: {request.POST}")
        
        service = None
        if service_slug:
            try:
                service = Service.objects.get(slug=service_slug)
                print(f"Found service: {service.title} (ID: {service.id})")
            except Service.DoesNotExist:
                print(f"Service with slug {service_slug} not found")
        
        # Create form with POST data
        form = ServiceInquiryForm(request.POST)
        
        print(f"Form is bound: {form.is_bound}")
        print(f"Form is valid: {form.is_valid()}")
        
        if not form.is_valid():
            print(f"Form errors: {form.errors}")
        
        if form.is_valid():
            try:
                # Save the form data
                inquiry = form.save(commit=False)
                
                # If service is provided, set it
                if service:
                    inquiry.specific_service = service
                    inquiry.service_type = 'single-service'
                    print(f"Set specific_service to: {service.id}")
                    print(f"Set service_type to: single-service")
                else:
                    # If no service slug, check if specific_service is in POST data
                    specific_service_id = request.POST.get('specific_service')
                    if specific_service_id and specific_service_id != '':
                        try:
                            specific_service = Service.objects.get(id=specific_service_id)
                            inquiry.specific_service = specific_service
                            inquiry.service_type = 'single-service'
                            print(f"Set specific_service from POST: {specific_service_id}")
                        except (Service.DoesNotExist, ValueError):
                            pass
                
                # Get user IP and user agent
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0]
                else:
                    ip = request.META.get('REMOTE_ADDR')
                
                inquiry.ip_address = ip
                inquiry.user_agent = request.META.get('HTTP_USER_AGENT', '')
                
                # Save to database
                inquiry.save()
                print(f"Inquiry saved with ID: {inquiry.id}")
                
                # Get service name for email
                if inquiry.specific_service:
                    service_name = inquiry.specific_service.title
                else:
                    service_name = inquiry.get_service_type_display()
                
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
Company: {inquiry.company or 'Not provided'}
Service Type: {inquiry.get_service_type_display()}
Service: {service_name}
Team Size: {inquiry.get_team_size_display()}
Budget Range: {inquiry.budget_range or 'Not specified'}
Timeline: {inquiry.timeline or 'Not specified'}
Additional Requirements: {inquiry.additional_requirements or 'None'}

Submitted at: {inquiry.submitted_at}
IP Address: {ip}
                            """,
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=[settings.ADMIN_EMAIL],
                            fail_silently=True,
                        )
                        print("Email sent successfully")
                    except Exception as e:
                        print(f"Email sending failed: {e}")
                
                # Add Django message
                success_message = 'Thank you for your inquiry! Our sales team will contact you with detailed information.'
                messages.success(request, success_message)
                
                if is_ajax:
                    print("AJAX request detected")
                    # Build redirect URL
                    if service:
                        redirect_url = reverse('website:service_detail', kwargs={'slug': service_slug})
                    else:
                        redirect_url = reverse('website:services')
                        
                    return JsonResponse({
                        'success': True,
                        'message': success_message,
                        'redirect': True,
                        'redirect_url': redirect_url
                    })
                else:
                    print("Non-AJAX request")
                    # For non-AJAX submission
                    if service:
                        return redirect('website:service_detail', slug=service_slug)
                    else:
                        return redirect('website:services')
                
            except Exception as e:
                print(f"Exception during form save: {str(e)}")
                import traceback
                traceback.print_exc()
                
                error_message = f'An error occurred: {str(e)}'
                if is_ajax:
                    return JsonResponse({
                        'success': False,
                        'message': error_message
                    })
                else:
                    messages.error(request, error_message)
                    if service:
                        return redirect('website:service_detail', slug=service_slug)
                    else:
                        return redirect('website:services')
        else:
            print("Form is invalid")
            error_message = 'Please correct the errors below.'
            if is_ajax:
                errors = form.errors.get_json_data()
                return JsonResponse({
                    'success': False,
                    'message': error_message,
                    'errors': errors
                })
            else:
                # For non-AJAX, add errors to messages
                for field, error_list in form.errors.items():
                    for error in error_list:
                        messages.error(request, f"{field}: {error}")
                if service:
                    return redirect('website:service_detail', slug=service_slug)
                else:
                    return redirect('website:services')
    
    # GET request
    if is_ajax:
        return JsonResponse({
            'success': False,
            'message': 'Invalid request method'
        })
    
    # Redirect to appropriate page
    if service_slug:
        return redirect('website:service_detail', slug=service_slug)
    else:
        return redirect('website:services')

# views.py - Update ServicesView
class ServicesView(ListView):
    model = ServiceCategory
    template_name = 'website/services.html'
    context_object_name = 'categories'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get service list hero or create default
        service_hero = ServiceHero.objects.filter(page_type='list', is_active=True).first()
        if not service_hero:
            service_hero = ServiceHero.objects.create(
                page_type='list',
                title="Our BPO Services",
                subtitle="Comprehensive Business Process Outsourcing Solutions to Drive Your Growth",
                is_active=True
            )
        
        # Add ServiceInquiryForm to context
        context['service_inquiry_form'] = ServiceInquiryForm(
            initial={'service_type': 'single-service'}
        )
        context['service_hero'] = service_hero
        context['all_services'] = Service.objects.all()
        return context


# views.py - Update ServiceDetailView
class ServiceDetailView(DetailView):
    model = Service
    template_name = 'website/service_detail.html'
    context_object_name = 'service'
    slug_field = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get or create service detail hero
        service_detail_hero = ServiceDetailHero.objects.filter(service=self.object).first()
        if not service_detail_hero:
            service_detail_hero = ServiceDetailHero.objects.create(
                service=self.object,
                show_default=True
            )
        
        # Use custom hero if available, otherwise use service data
        if service_detail_hero and not service_detail_hero.show_default:
            hero_title = service_detail_hero.custom_title or self.object.title
            hero_subtitle = service_detail_hero.custom_subtitle or self.object.short_description
            hero_image = service_detail_hero.custom_image
        else:
            # Get service detail page hero template
            service_hero_template = ServiceHero.objects.filter(page_type='detail', is_active=True).first()
            if service_hero_template:
                hero_title = self.object.title
                hero_subtitle = service_hero_template.subtitle.replace('{service}', self.object.title)
            else:
                hero_title = self.object.title
                hero_subtitle = self.object.short_description
            hero_image = None
        
        context['service_hero'] = {
            'title': hero_title,
            'subtitle': hero_subtitle,
            'image': hero_image,
            'service': self.object
        }
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
    