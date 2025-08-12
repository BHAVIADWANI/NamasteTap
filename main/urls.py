from django.urls import path
from . import views
from . import visiting_card_views
from . import template_views

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
    path('register/<str:code>/', visiting_card_views.register_card, name='register_card'),
    path('card/<slug:slug>/', visiting_card_views.view_card, name='view_card'),
    path('card/<slug:slug>/edit/', visiting_card_views.edit_card, name='edit_card'),
    path('card/<slug:slug>/analytics/', visiting_card_views.card_analytics, name='card_analytics'),
    path('card/<slug:slug>/download/', visiting_card_views.download_vcard, name='download_vcard'),
    path('card/<slug:slug>/toggle/', visiting_card_views.toggle_card_status, name='toggle_card_status'),
    
    # Card Management Dashboard
    path('cards/', visiting_card_views.card_dashboard, name='card_dashboard'),
    
    # Template Management
    path('card/<slug:card_slug>/select-template/', template_views.select_template, name='select_template'),
    path('templates/preview/<int:template_id>/', template_views.preview_template, name='preview_template'),
    path('templates/gallery/', template_views.template_gallery, name='template_gallery'),
    path('api/template/<int:template_id>/', template_views.get_template_info, name='template_info'),
    
    # Admin Visiting Card Management
    path('admin/visiting-cards/', visiting_card_views.manage_visiting_cards, name='manage_visiting_cards'),
    path('admin/visiting-cards/create/', visiting_card_views.create_visiting_cards, name='create_visiting_cards'),
    
    # API Endpoints
    path('api/card/<slug:slug>/', visiting_card_views.api_card_data, name='api_card_data'),
]
