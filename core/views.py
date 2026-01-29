from django.shortcuts import render

# Create your views here.
# core/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from posts.models import Post

# @login_required
# def dashboard(request):
#     posts = Post.objects.all().order_by('-created_at')[:20]
#     return render(request, 'core/dashboard.html', {'posts': posts})


# core/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model  # ← THIS WAS MISSING!
from posts.models import Post

User = get_user_model()  # ← NOW IT WORKS!

@login_required
def dashboard(request):
    # Get recent posts
    posts = Post.objects.all().order_by('-created_at')[:20]
    
    # Get online users (who have is_online=True)
    active_users = User.objects.filter(
        profile__is_online=True
    ).exclude(id=request.user.id)[:15]
    
    context = {
        'posts': posts,
        'active_users': active_users,
    }
    return render(request, 'core/dashboard.html', context)