from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('services/', views.ServicesView.as_view(), name='services'),
    path('services/<slug:slug>/', views.ServiceDetailView.as_view(), name='service_detail'),
    
    path('contact/', views.ContactView.as_view(), name='contact'),
    
    # Form submission endpoints
    path('submit-contact/', views.submit_contact, name='submit_contact'),
    path('submit-consultation/', views.submit_consultation, name='submit_consultation'),
    path('submit-inquiry/', views.submit_service_inquiry, name='submit_inquiry'),
    path('submit-inquiry/<slug:service_slug>/', views.submit_service_inquiry, name='submit_service_inquiry'),
]

