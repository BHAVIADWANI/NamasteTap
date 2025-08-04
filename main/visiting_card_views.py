# ===== VISITING CARD SYSTEM VIEWS =====

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
import json
from .models import CustomUser, UserProfile, VisitingCard, DigitalCard, CardAnalytics, CardOrder


def register_card(request, code):
    """Register a visiting card with a registration code"""
    try:
        visiting_card = VisitingCard.objects.get(registration_code=code, status__in=['delivered', 'manufactured'])
    except VisitingCard.DoesNotExist:
        messages.error(request, 'Invalid registration code or card already registered.')
        return render(request, 'cards/register_error.html', {'code': code})
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Please log in to register your card.')
            return redirect('main:login')
        
        # Create digital card
        digital_card = DigitalCard.objects.create(
            user=request.user,
            visiting_card=visiting_card,
            display_name=request.user.get_full_name() or request.user.username,
            email=request.user.email,
        )
        
        # Update visiting card status
        visiting_card.status = 'registered'
        visiting_card.save()
        
        messages.success(request, f'Card registered successfully! Your card URL: {digital_card.get_absolute_url()}')
        return redirect('main:edit_card', slug=digital_card.url_slug)
    
    return render(request, 'cards/register_card.html', {
        'visiting_card': visiting_card,
        'registration_url': request.build_absolute_uri()
    })


def view_card(request, slug):
    """Public view for digital business card"""
    digital_card = get_object_or_404(DigitalCard, url_slug=slug, is_active=True)
    
    # Track analytics
    if request.method == 'GET':
        CardAnalytics.objects.create(
            digital_card=digital_card,
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            referrer=request.META.get('HTTP_REFERER', ''),
        )
        digital_card.increment_view_count()
    
    context = {
        'card': digital_card,
        'social_links': digital_card.get_social_links(),
        'custom_links': digital_card.custom_links,
    }
    
    return render(request, 'cards/view_card.html', context)


@login_required
def edit_card(request, slug):
    """Edit digital business card"""
    digital_card = get_object_or_404(DigitalCard, url_slug=slug, user=request.user)
    
    if request.method == 'POST':
        # Update card information
        digital_card.display_name = request.POST.get('display_name', digital_card.display_name)
        digital_card.job_title = request.POST.get('job_title', '')
        digital_card.company_name = request.POST.get('company_name', '')
        digital_card.email = request.POST.get('email', digital_card.email)
        digital_card.phone = request.POST.get('phone', '')
        digital_card.bio = request.POST.get('bio', '')
        digital_card.website = request.POST.get('website', '')
        digital_card.location = request.POST.get('location', '')
        
        # Social media links
        digital_card.linkedin_url = request.POST.get('linkedin_url', '')
        digital_card.twitter_url = request.POST.get('twitter_url', '')
        digital_card.instagram_url = request.POST.get('instagram_url', '')
        digital_card.facebook_url = request.POST.get('facebook_url', '')
        
        # Privacy settings
        digital_card.show_email = request.POST.get('show_email') == 'on'
        digital_card.show_phone = request.POST.get('show_phone') == 'on'
        digital_card.show_social_links = request.POST.get('show_social_links') == 'on'
        
        # Handle custom links (JSON format)
        custom_links_json = request.POST.get('custom_links', '{}')
        try:
            digital_card.custom_links = json.loads(custom_links_json)
        except json.JSONDecodeError:
            digital_card.custom_links = {}
        
        # Handle profile image upload
        if 'profile_image' in request.FILES:
            digital_card.profile_image = request.FILES['profile_image']
        
        digital_card.save()
        messages.success(request, 'Card updated successfully!')
        return redirect('main:card_dashboard')
    
    return render(request, 'cards/edit_card.html', {
        'card': digital_card,
        'custom_links_json': json.dumps(digital_card.custom_links, indent=2)
    })


@login_required
def card_dashboard(request):
    """Dashboard showing all user's digital cards"""
    user_cards = DigitalCard.objects.filter(user=request.user).order_by('-created_at')
    
    # Calculate total analytics
    total_views = sum(card.view_count for card in user_cards)
    
    context = {
        'cards': user_cards,
        'total_views': total_views,
        'total_cards': user_cards.count(),
    }
    
    return render(request, 'cards/card_dashboard.html', context)


@login_required
def card_analytics(request, slug):
    """Detailed analytics for a specific card"""
    digital_card = get_object_or_404(DigitalCard, url_slug=slug, user=request.user)
    
    # Get analytics data
    analytics = CardAnalytics.objects.filter(digital_card=digital_card).order_by('-viewed_at')[:100]
    
    # Group analytics by date for chart
    from django.db.models import Count
    
    daily_views = (
        CardAnalytics.objects
        .filter(digital_card=digital_card)
        .extra({'date': "date(viewed_at)"})
        .values('date')
        .annotate(views=Count('id'))
        .order_by('date')
    )
    
    context = {
        'card': digital_card,
        'analytics': analytics,
        'daily_views': daily_views,
        'total_views': digital_card.view_count,
        'last_viewed': digital_card.last_viewed,
    }
    
    return render(request, 'cards/card_analytics.html', context)


def download_vcard(request, slug):
    """Download vCard (.vcf) file for contact"""
    digital_card = get_object_or_404(DigitalCard, url_slug=slug, is_active=True)
    
    # Track download
    try:
        analytics = CardAnalytics.objects.filter(
            digital_card=digital_card,
            ip_address=get_client_ip(request)
        ).latest('viewed_at')
        analytics.contact_downloaded = True
        analytics.save()
    except CardAnalytics.DoesNotExist:
        pass
    
    # Create vCard content manually
    vcard_content = f"""BEGIN:VCARD
VERSION:3.0
FN:{digital_card.display_name}
ORG:{digital_card.company_name}
TITLE:{digital_card.job_title}
EMAIL:{digital_card.email}
TEL:{digital_card.phone}
URL:{digital_card.website}
NOTE:{digital_card.bio}
END:VCARD"""
    
    response = HttpResponse(vcard_content, content_type='text/vcard')
    response['Content-Disposition'] = f'attachment; filename="{digital_card.display_name}.vcf"'
    
    return response


@login_required
def manage_visiting_cards(request):
    """Admin view to manage visiting cards"""
    if not request.user.is_admin_user:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('main:dashboard')
    
    cards = VisitingCard.objects.all().order_by('-manufactured_date')
    
    # Filter options
    status_filter = request.GET.get('status')
    card_type_filter = request.GET.get('card_type')
    
    if status_filter:
        cards = cards.filter(status=status_filter)
    if card_type_filter:
        cards = cards.filter(card_type=card_type_filter)
    
    paginator = Paginator(cards, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'total_cards': cards.count(),
        'status_choices': VisitingCard.STATUS_CHOICES,
        'card_type_choices': VisitingCard.CARD_TYPE_CHOICES,
        'current_status': status_filter,
        'current_type': card_type_filter,
    }
    
    return render(request, 'cards/manage_visiting_cards.html', context)


@login_required
def create_visiting_cards(request):
    """Admin view to create new visiting cards"""
    if not request.user.is_admin_user:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('main:dashboard')
    
    if request.method == 'POST':
        card_type = request.POST.get('card_type')
        quantity = int(request.POST.get('quantity', 1))
        batch_number = request.POST.get('batch_number', '')
        
        created_cards = []
        for _ in range(quantity):
            card = VisitingCard.objects.create(
                card_type=card_type,
                batch_number=batch_number,
            )
            created_cards.append(card)
        
        messages.success(request, f'Successfully created {quantity} {card_type} cards.')
        return redirect('main:manage_visiting_cards')
    
    return render(request, 'cards/create_visiting_cards.html', {
        'card_type_choices': VisitingCard.CARD_TYPE_CHOICES
    })


def get_client_ip(request):
    """Get client IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# ===== API ENDPOINTS =====

def api_card_data(request, slug):
    """API endpoint to get card data as JSON"""
    digital_card = get_object_or_404(DigitalCard, url_slug=slug, is_active=True)
    
    data = {
        'name': digital_card.display_name,
        'title': digital_card.job_title,
        'company': digital_card.company_name,
        'email': digital_card.email if digital_card.show_email else None,
        'phone': digital_card.phone if digital_card.show_phone else None,
        'website': digital_card.website,
        'bio': digital_card.bio,
        'location': digital_card.location,
        'social_links': digital_card.get_social_links() if digital_card.show_social_links else [],
        'custom_links': digital_card.custom_links,
        'profile_image': digital_card.profile_image.url if digital_card.profile_image else None,
    }
    
    return JsonResponse(data)


@login_required
def toggle_card_status(request, slug):
    """Toggle card active/inactive status"""
    digital_card = get_object_or_404(DigitalCard, url_slug=slug, user=request.user)
    
    if request.method == 'POST':
        digital_card.is_active = not digital_card.is_active
        digital_card.save()
        
        status = 'activated' if digital_card.is_active else 'deactivated'
        messages.success(request, f'Card {status} successfully!')
    
    return redirect('main:card_dashboard')
