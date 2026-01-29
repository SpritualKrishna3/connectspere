# posts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Post

@login_required
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'posts/list.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content', '')
        post_type = request.POST.get('post_type', 'text')
        
        post = Post.objects.create(
            author=request.user,
            content=content,
            post_type=post_type
        )
        
        if 'image' in request.FILES:
            post.image = request.FILES['image']
        if 'file' in request.FILES:
            post.file = request.FILES['file']
        if request.POST.get('is_important'):
            post.is_important = True
            
        post.save()
        messages.success(request, "Post created!")
        return redirect('post_list')
        
    return render(request, 'posts/create.html')

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'posts/detail.html', {'post': post})

@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
        
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'likes': post.likes.count(), 'liked': liked})
        
    return redirect('post_detail', pk)