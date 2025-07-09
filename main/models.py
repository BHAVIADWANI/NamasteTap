from django.contrib.auth.models import AbstractUser
from django.db import models

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
