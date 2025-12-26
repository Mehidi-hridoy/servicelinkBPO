from django import template
from django.urls import reverse

register = template.Library()

@register.filter
def resolve_url(value):
    """Convert URL patterns to actual Django URLs"""
    url_mapping = {
        '/': 'website:home',
        '/services/': 'website:services',
        '/contact/': 'website:contact',
        '/about/': 'website:about',
    }
    
    if value in url_mapping:
        return reverse(url_mapping[value])
    return value

@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except Exception:
        return ''
