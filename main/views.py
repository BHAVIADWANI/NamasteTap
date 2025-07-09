from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import CustomUser, UserProfile
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm, UserUpdateForm

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def contact(request):
    return render(request, 'contact.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username/email or password.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'auth/login.html', {'form': form})

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created successfully! Welcome, {user.first_name}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'auth/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required
def dashboard(request):
    user = request.user
    context = {
        'user': user,
        'total_users': CustomUser.objects.count(),
        'admin_users': CustomUser.objects.filter(user_type='admin').count(),
        'standard_users': CustomUser.objects.filter(user_type='standard').count(),
    }
    
    if user.is_admin_user:
        return render(request, 'dashboard/admin_dashboard.html', context)
    else:
        return render(request, 'dashboard/user_dashboard.html', context)

@login_required
def profile(request):
    user = request.user
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = UserProfileForm(instance=profile)
    
    return render(request, 'dashboard/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'user': user,
        'profile': profile
    })

@login_required
def manage_users(request):
    if not request.user.is_admin_user:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')
    
    users = CustomUser.objects.all().order_by('-created_at')
    paginator = Paginator(users, 10)  # Show 10 users per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'dashboard/manage_users.html', {
        'page_obj': page_obj,
        'total_users': users.count()
    })

@login_required
def user_detail(request, user_id):
    if not request.user.is_admin_user:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')
    
    try:
        user = CustomUser.objects.get(id=user_id)
        profile = user.profile
    except CustomUser.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('manage_users')
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)
    
    return render(request, 'dashboard/user_detail.html', {
        'user_detail': user,
        'profile': profile
    })

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def contact(request):
    return render(request, 'contact.html')
