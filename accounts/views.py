# accounts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import Profile

User = get_user_model()

# Register
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            messages.success(request, "Welcome to ConnectSphere!")
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

# Login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

# Logout
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')

# Profile View (FIXED)
@login_required
def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = profile_user.posts.all().order_by('-created_at')[:12]
    
    context = {
        'profile_user': profile_user,
        'posts': posts,
        'is_own_profile': request.user == profile_user
    }
    return render(request, 'accounts/profile.html', context)

# Edit Profile
@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        profile.bio = request.POST.get('bio', '')
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
        profile.save()
        messages.success(request, "Profile updated!")
        return redirect('profile', request.user.username)
    return render(request, 'accounts/edit_profile.html', {'profile': profile})


@login_required
def edit_profile(request):
    profile = request.user.profile
    
    if request.method == 'POST':
        profile.bio = request.POST.get('bio', '')
        profile.domain = request.POST.get('domain', '')
        profile.github = request.POST.get('github', '')
        profile.linkedin = request.POST.get('linkedin', '')
        
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
            
        profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('profile', request.user.username)
    
    return render(request, 'accounts/edit_profile.html')