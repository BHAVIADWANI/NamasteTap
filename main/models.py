from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
import secrets
import string
from django.utils import timezone
from django.urls import reverse

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin User'),
        ('standard', 'Standard User'),
    )
    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='standard')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

    @property
    def is_admin_user(self):
        return self.user_type == 'admin'

    @property
    def is_standard_user(self):
        return self.user_type == 'standard'


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    company = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"


class VisitingCard(models.Model):
    """Model for physical visiting cards before registration"""
    CARD_TYPE_CHOICES = (
        ('pvc', 'PVC Card'),
        ('wood', 'Wood Card'),
        ('metal', 'Metal Card'),
    )
    
    STATUS_CHOICES = (
        ('manufactured', 'Manufactured'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('registered', 'Registered'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    
    # Unique identifiers
    card_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    registration_code = models.CharField(max_length=16, unique=True, editable=False)
    
    # Card specifications
    card_type = models.CharField(max_length=10, choices=CARD_TYPE_CHOICES)
    batch_number = models.CharField(max_length=20, blank=True)
    
    # Status tracking
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='manufactured')
    manufactured_date = models.DateTimeField(auto_now_add=True)
    shipped_date = models.DateTimeField(null=True, blank=True)
    delivered_date = models.DateTimeField(null=True, blank=True)
    
    # Order information
    order_reference = models.CharField(max_length=50, blank=True)
    customer_email = models.EmailField(blank=True)
    customer_phone = models.CharField(max_length=15, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.registration_code:
            self.registration_code = self.generate_registration_code()
        super().save(*args, **kwargs)
    
    def generate_registration_code(self):
        """Generate a unique 16-character registration code"""
        while True:
            code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(16))
            if not VisitingCard.objects.filter(registration_code=code).exists():
                return code
    
    def get_registration_url(self):
        """Get the registration URL for this card"""
        return reverse('main:register_card', kwargs={'code': self.registration_code})
    
    def get_absolute_url(self):
        """Get the public profile URL after registration"""
        if hasattr(self, 'digital_card'):
            return self.digital_card.get_absolute_url()
        return None
    
    def __str__(self):
        return f"{self.get_card_type_display()} - {self.registration_code}"


class DigitalCard(models.Model):
    """Digital business card linked to visiting card"""
    # Links
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='digital_cards')
    visiting_card = models.OneToOneField(VisitingCard, on_delete=models.CASCADE, related_name='digital_card')
    
    # Unique URL identifier
    url_slug = models.SlugField(max_length=50, unique=True)
    
    # Card information
    card_title = models.CharField(max_length=100, default="Digital Business Card")
    is_active = models.BooleanField(default=True)
    
    # Contact Information
    display_name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100, blank=True)
    company_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    
    # Additional Information
    bio = models.TextField(max_length=500, blank=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    
    # Social Media Links
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    
    # Custom Links (JSON field for flexibility)
    custom_links = models.JSONField(default=dict, blank=True)
    
    # Profile Image
    profile_image = models.ImageField(upload_to='card_profiles/', blank=True, null=True)
    
    # Settings
    show_email = models.BooleanField(default=True)
    show_phone = models.BooleanField(default=True)
    show_social_links = models.BooleanField(default=True)
    
    # Analytics
    view_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_viewed = models.DateTimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.url_slug:
            self.url_slug = self.generate_unique_slug()
        super().save(*args, **kwargs)
    
    def generate_unique_slug(self):
        """Generate a unique URL slug"""
        base_slug = f"{self.user.username}-{secrets.token_urlsafe(8)}"
        counter = 1
        slug = base_slug
        
        while DigitalCard.objects.filter(url_slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        return slug
    
    def get_absolute_url(self):
        """Get the public URL for this digital card"""
        return reverse('main:view_card', kwargs={'slug': self.url_slug})
    
    def increment_view_count(self):
        """Increment view count and update last viewed"""
        self.view_count += 1
        self.last_viewed = timezone.now()
        self.save(update_fields=['view_count', 'last_viewed'])
    
    def get_social_links(self):
        """Get all social media links"""
        links = []
        if self.linkedin_url:
            links.append({'name': 'LinkedIn', 'url': self.linkedin_url, 'icon': 'fab fa-linkedin'})
        if self.twitter_url:
            links.append({'name': 'Twitter', 'url': self.twitter_url, 'icon': 'fab fa-twitter'})
        if self.instagram_url:
            links.append({'name': 'Instagram', 'url': self.instagram_url, 'icon': 'fab fa-instagram'})
        if self.facebook_url:
            links.append({'name': 'Facebook', 'url': self.facebook_url, 'icon': 'fab fa-facebook'})
        return links
    
    def __str__(self):
        return f"{self.display_name} - {self.url_slug}"


class CardAnalytics(models.Model):
    """Track analytics for digital cards"""
    digital_card = models.ForeignKey(DigitalCard, on_delete=models.CASCADE, related_name='analytics')
    
    # Visitor Information
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    referrer = models.URLField(blank=True)
    
    # Location (can be added later with IP geolocation)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    
    # Interaction Details
    viewed_at = models.DateTimeField(auto_now_add=True)
    contact_downloaded = models.BooleanField(default=False)
    links_clicked = models.JSONField(default=list, blank=True)
    
    def __str__(self):
        return f"{self.digital_card.display_name} - {self.viewed_at.strftime('%Y-%m-%d %H:%M')}"


class CardOrder(models.Model):
    """Track card orders and shipping"""
    ORDER_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('manufacturing', 'Manufacturing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('completed', 'Completed'),
    )
    
    # Order Details
    order_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    customer_email = models.EmailField()
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=15)
    
    # Shipping Information
    shipping_address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    
    # Order Items
    pvc_cards = models.IntegerField(default=0)
    wood_cards = models.IntegerField(default=0)
    metal_cards = models.IntegerField(default=0)
    pvc_standees = models.IntegerField(default=0)
    wood_standees = models.IntegerField(default=0)
    metal_standees = models.IntegerField(default=0)
    
    # Pricing
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    final_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Status
    status = models.CharField(max_length=15, choices=ORDER_STATUS_CHOICES, default='pending')
    order_date = models.DateTimeField(auto_now_add=True)
    shipped_date = models.DateTimeField(null=True, blank=True)
    delivered_date = models.DateTimeField(null=True, blank=True)
    
    # Tracking
    tracking_number = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)
    
    def get_total_cards(self):
        return self.pvc_cards + self.wood_cards + self.metal_cards
    
    def get_total_standees(self):
        return self.pvc_standees + self.wood_standees + self.metal_standees
    
    def __str__(self):
        return f"Order {self.order_id} - {self.customer_name}"
