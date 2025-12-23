from .models import ContactInfo

def global_context(request):
    return {
        'contact_info': ContactInfo.objects.first(),
    }

