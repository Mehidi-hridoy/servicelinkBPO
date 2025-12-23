from django.core.management.base import BaseCommand
from website.models import FAQ

class Command(BaseCommand):
    help = 'Load initial FAQ data'
    
    def handle(self, *args, **kwargs):
        faqs = [
            {
                'question': 'What information should I include in my inquiry?',
                'answer': 'Please include your company name, specific service requirements, team size needed, timeline for implementation, and any specific challenges you\'re facing. The more details you provide, the better we can tailor our response to your needs.',
                'category': 'contact',
                'order': 1,
                'is_active': True
            },
            {
                'question': 'How quickly will I get a response?',
                'answer': f'We typically respond to all inquiries within 2 business hours during office hours. For urgent matters, please call us directly.',
                'category': 'contact',
                'order': 2,
                'is_active': True
            },
            {
                'question': 'Do you offer free consultations?',
                'answer': 'Yes! We offer a free 30-minute initial consultation to discuss your needs and how we can help. This consultation includes a basic assessment of your requirements and an overview of potential solutions.',
                'category': 'contact',
                'order': 3,
                'is_active': True
            },
            {
                'question': 'What are your business hours?',
                'answer': 'Our main office in Dhaka is open Monday-Friday from 9:00 AM to 6:00 PM and Saturday from 10:00 AM to 4:00 PM (Bangladesh Standard Time). However, our client support teams operate 24/7 to serve our global clients.',
                'category': 'contact',
                'order': 4,
                'is_active': True
            },
            {
                'question': 'What makes ServiceLink BPO different from other BPO providers?',
                'answer': 'We focus on building partnerships rather than just providing services. Our distinctively different approach involves deep integration with your business culture, customized solutions, and ongoing performance optimization.',
                'category': 'general',
                'order': 1,
                'is_active': True
            },
            {
                'question': 'How quickly can you scale my team up or down?',
                'answer': 'We maintain a talent pool of pre-vetted professionals ready for deployment. Typically, we can scale your team within 2-4 weeks, depending on role complexity. For emergency scaling, we can deploy resources within 7-10 days.',
                'category': 'general',
                'order': 2,
                'is_active': True
            },
            {
                'question': 'What industries do you specialize in?',
                'answer': 'We serve a wide range of industries including e-commerce, healthcare, finance, technology, retail, education, and manufacturing. Our teams are trained in industry-specific protocols and compliance requirements.',
                'category': 'general',
                'order': 3,
                'is_active': True
            },
            {
                'question': 'How do you ensure data security and compliance?',
                'answer': 'We implement enterprise-grade security measures including encrypted communications, secure VPN access, regular security audits, and compliance with GDPR, HIPAA, and other relevant regulations. All team members sign strict confidentiality agreements.',
                'category': 'general',
                'order': 4,
                'is_active': True
            },
        ]
        
        for faq_data in faqs:
            FAQ.objects.create(**faq_data)
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded FAQ data!'))