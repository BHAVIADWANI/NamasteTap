from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    
    # Authentication
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    
    # User dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    
    # Admin views
    path('manage-users/', views.manage_users, name='manage_users'),
    path('user/<int:user_id>/', views.user_detail, name='user_detail'),
    
    # Visiting Card Registration System
    path('register/<str:code>/', views.register_card, name='register_card'),
    path('card/<slug:slug>/', views.view_card, name='view_card'),
    path('card/<slug:slug>/edit/', views.edit_card, name='edit_card'),
    path('card/<slug:slug>/analytics/', views.card_analytics, name='card_analytics'),
    path('card/<slug:slug>/download/', views.download_vcard, name='download_vcard'),
    path('card/<slug:slug>/toggle/', views.toggle_card_status, name='toggle_card_status'),
    
    # Card Management Dashboard
    path('cards/', views.card_dashboard, name='card_dashboard'),
    
    # Admin Visiting Card Management
    path('admin/visiting-cards/', views.manage_visiting_cards, name='manage_visiting_cards'),
    path('admin/visiting-cards/create/', views.create_visiting_cards, name='create_visiting_cards'),
    
    # API Endpoints
    path('api/card/<slug:slug>/', views.api_card_data, name='api_card_data'),
]
