from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import DigitalCard, CompanyTemplate


@login_required
def select_template(request, card_slug):
    """Allow users to select a company template for their card"""
    digital_card = get_object_or_404(DigitalCard, url_slug=card_slug, user=request.user)
    
    if request.method == 'POST':
        template_id = request.POST.get('template_id')
        
        if template_id == 'default':
            digital_card.company_template = None
            digital_card.save()
            messages.success(request, 'Default template selected successfully!')
        else:
            try:
                template = CompanyTemplate.objects.get(id=template_id, is_active=True)
                digital_card.company_template = template
                digital_card.save()
                messages.success(request, f'Template "{template.name}" selected successfully!')
            except CompanyTemplate.DoesNotExist:
                messages.error(request, 'Invalid template selected.')
        
        return redirect('main:card_dashboard')
    
    # Get available templates
    templates = CompanyTemplate.objects.filter(is_active=True).order_by('template_type', 'name')
    
    context = {
        'card': digital_card,
        'templates': templates,
        'current_template': digital_card.company_template,
    }
    
    return render(request, 'cards/select_template.html', context)


@login_required
def preview_template(request, template_id):
    """Preview a template with sample data"""
    template = get_object_or_404(CompanyTemplate, id=template_id, is_active=True)
    
    # Create sample card data for preview
    sample_card = type('SampleCard', (), {
        'display_name': 'John Doe',
        'job_title': 'Senior Developer',
        'company_name': 'Tech Company Inc.',
        'email': 'john.doe@company.com',
        'phone': '+1 (555) 123-4567',
        'website': 'https://company.com',
        'location': 'New York, NY',
        'bio': 'Experienced software developer with expertise in web technologies.',
        'profile_image': None,
        'show_email': True,
        'show_phone': True,
        'show_social_links': True,
        'linkedin_url': 'https://linkedin.com/in/johndoe',
        'twitter_url': 'https://twitter.com/johndoe',
        'company_template': template,
    })()
    
    # Add methods to sample card
    sample_card.get_social_links = lambda: [
        {'name': 'LinkedIn', 'url': 'https://linkedin.com/in/johndoe', 'icon': 'fab fa-linkedin'},
        {'name': 'Twitter', 'url': 'https://twitter.com/johndoe', 'icon': 'fab fa-twitter'},
    ]
    
    context = {
        'card': sample_card,
        'template': template,
        'primary_color': template.primary_color,
        'secondary_color': template.secondary_color,
        'font_family': template.font_family,
        'css_path': template.get_css_path(),
        'js_path': template.get_js_path(),
        'social_links': sample_card.get_social_links(),
        'is_preview': True,
    }
    
    return render(request, template.get_template_path(), context)


def get_template_info(request, template_id):
    """Get template information via AJAX"""
    try:
        template = CompanyTemplate.objects.get(id=template_id, is_active=True)
        return JsonResponse({
            'success': True,
            'template': {
                'id': template.id,
                'name': template.name,
                'description': template.description,
                'template_type': template.get_template_type_display(),
                'is_premium': template.is_premium,
                'primary_color': template.primary_color,
                'secondary_color': template.secondary_color,
                'font_family': template.font_family,
            }
        })
    except CompanyTemplate.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Template not found'
        })


@login_required
def template_gallery(request):
    """Show all available templates"""
    templates = CompanyTemplate.objects.filter(is_active=True).order_by('template_type', 'name')
    
    # Group templates by type
    grouped_templates = {}
    for template in templates:
        template_type = template.get_template_type_display()
        if template_type not in grouped_templates:
            grouped_templates[template_type] = []
        grouped_templates[template_type].append(template)
    
    context = {
        'grouped_templates': grouped_templates,
        'total_templates': templates.count(),
    }
    
    return render(request, 'cards/template_gallery.html', context)
