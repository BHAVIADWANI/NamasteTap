"""
TapOne3 Test Suite
Tests for NFC Business Cards Platform
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import CustomUser, UserProfile
from .forms import CustomUserCreationForm, CustomAuthenticationForm

User = get_user_model()


class CustomUserModelTests(TestCase):
    """Test cases for CustomUser model"""
    
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@tapone3.com',
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': '+1234567890',
            'user_type': 'standard'
        }
    
    def test_create_standard_user(self):
        """Test creating a standard user"""
        user = CustomUser.objects.create_user(
            username=self.user_data['username'],
            email=self.user_data['email'],
            password='testpass123'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@tapone3.com')
        self.assertEqual(user.user_type, 'standard')
        self.assertTrue(user.is_standard_user)
        self.assertFalse(user.is_admin_user)
        self.assertTrue(user.is_active)
    
    def test_create_admin_user(self):
        """Test creating an admin user"""
        user = CustomUser.objects.create_user(
            username='adminuser',
            email='admin@tapone3.com',
            password='adminpass123',
            user_type='admin'
        )
        self.assertEqual(user.user_type, 'admin')
        self.assertTrue(user.is_admin_user)
        self.assertFalse(user.is_standard_user)
    
    def test_user_string_representation(self):
        """Test user string representation"""
        user = CustomUser.objects.create_user(
            username='testuser',
            email='test@tapone3.com',
            password='testpass123',
            user_type='admin'
        )
        expected_str = "testuser (Admin User)"
        self.assertEqual(str(user), expected_str)


class UserProfileModelTests(TestCase):
    """Test cases for UserProfile model"""
    
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@tapone3.com',
            password='testpass123'
        )
    
    def test_create_user_profile(self):
        """Test creating a user profile"""
        profile = UserProfile.objects.create(
            user=self.user,
            bio='This is a test bio',
            location='Test City',
            website='https://tapone3.com',
            company='TapOne3 Corp'
        )
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.bio, 'This is a test bio')
        self.assertEqual(profile.location, 'Test City')
        self.assertEqual(str(profile), "testuser's Profile")


class FormsTests(TestCase):
    """Test cases for forms"""
    
    def test_custom_user_creation_form_valid_data(self):
        """Test user creation form with valid data"""
        form_data = {
            'username': 'newuser',
            'email': 'newuser@tapone3.com',
            'first_name': 'New',
            'last_name': 'User',
            'phone_number': '+1234567890',
            'user_type': 'standard',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_custom_user_creation_form_password_mismatch(self):
        """Test user creation form with password mismatch"""
        form_data = {
            'username': 'newuser',
            'email': 'newuser@tapone3.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'complexpass123',
            'password2': 'differentpass123'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_custom_authentication_form(self):
        """Test authentication form"""
        user = CustomUser.objects.create_user(
            username='testuser',
            email='test@tapone3.com',
            password='testpass123'
        )
        
        form_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        form = CustomAuthenticationForm(data=form_data)
        self.assertTrue(form.is_valid())


class ViewsTests(TestCase):
    """Test cases for views"""
    
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@tapone3.com',
            password='testpass123'
        )
        self.admin_user = CustomUser.objects.create_user(
            username='adminuser',
            email='admin@tapone3.com',
            password='adminpass123',
            user_type='admin'
        )
    
    def test_home_page(self):
        """Test home page loads correctly"""
        response = self.client.get(reverse('main:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'TapOne3')
        self.assertContains(response, 'NFC Business Cards')
    
    def test_about_page(self):
        """Test about page loads correctly"""
        response = self.client.get(reverse('main:about'))
        self.assertEqual(response.status_code, 200)
    
    def test_login_view_get(self):
        """Test login page loads correctly"""
        response = self.client.get(reverse('main:login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login')
    
    def test_login_view_post_valid(self):
        """Test login with valid credentials"""
        response = self.client.post(reverse('main:login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login
    
    def test_login_view_post_invalid(self):
        """Test login with invalid credentials"""
        response = self.client.post(reverse('main:login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # Stay on login page
        self.assertContains(response, 'Invalid')
    
    def test_signup_view_get(self):
        """Test signup page loads correctly"""
        response = self.client.get(reverse('main:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sign Up')
    
    def test_dashboard_requires_login(self):
        """Test dashboard requires authentication"""
        response = self.client.get(reverse('main:dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_dashboard_authenticated_user(self):
        """Test dashboard for authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dashboard')
    
    def test_admin_dashboard_for_admin_user(self):
        """Test admin dashboard for admin user"""
        self.client.login(username='adminuser', password='adminpass123')
        response = self.client.get(reverse('main:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Admin Dashboard')
    
    def test_manage_users_requires_admin(self):
        """Test manage users requires admin privileges"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:manage_users'))
        self.assertEqual(response.status_code, 302)  # Redirect due to insufficient privileges
    
    def test_manage_users_admin_access(self):
        """Test manage users for admin user"""
        self.client.login(username='adminuser', password='adminpass123')
        response = self.client.get(reverse('main:manage_users'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Manage Users')
    
    def test_profile_page(self):
        """Test profile page for authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Profile')
    
    def test_logout_view(self):
        """Test logout functionality"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:logout'))
        self.assertEqual(response.status_code, 302)  # Redirect after logout


class IntegrationTests(TestCase):
    """Integration tests for user flows"""
    
    def setUp(self):
        self.client = Client()
    
    def test_complete_signup_login_flow(self):
        """Test complete user signup and login flow"""
        # Test signup
        signup_data = {
            'username': 'integrationuser',
            'email': 'integration@tapone3.com',
            'first_name': 'Integration',
            'last_name': 'User',
            'phone_number': '+1234567890',
            'user_type': 'standard',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        }
        
        signup_response = self.client.post(reverse('main:signup'), signup_data)
        self.assertEqual(signup_response.status_code, 302)  # Redirect after successful signup
        
        # Verify user was created
        user = CustomUser.objects.get(username='integrationuser')
        self.assertEqual(user.email, 'integration@tapone3.com')
        self.assertTrue(user.is_active)
        
        # Verify profile was created
        profile = UserProfile.objects.get(user=user)
        self.assertIsNotNone(profile)
        
        # Test login with new user
        self.client.logout()
        login_response = self.client.post(reverse('main:login'), {
            'username': 'integrationuser',
            'password': 'complexpass123'
        })
        self.assertEqual(login_response.status_code, 302)  # Redirect after successful login
        
        # Test dashboard access
        dashboard_response = self.client.get(reverse('main:dashboard'))
        self.assertEqual(dashboard_response.status_code, 200)
        self.assertContains(dashboard_response, 'Integration')
    
    def test_admin_user_management_flow(self):
        """Test admin user management flow"""
        # Create admin user
        admin_user = CustomUser.objects.create_user(
            username='admintest',
            email='admin@tapone3.com',
            password='adminpass123',
            user_type='admin'
        )
        
        # Create regular user
        regular_user = CustomUser.objects.create_user(
            username='regulartest',
            email='regular@tapone3.com',
            password='regularpass123'
        )
        
        # Login as admin
        self.client.login(username='admintest', password='adminpass123')
        
        # Access manage users page
        manage_response = self.client.get(reverse('main:manage_users'))
        self.assertEqual(manage_response.status_code, 200)
        self.assertContains(manage_response, 'regulartest')
        
        # Access user detail page
        detail_response = self.client.get(reverse('main:user_detail', args=[regular_user.id]))
        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, 'regulartest')
