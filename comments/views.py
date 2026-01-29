# comments/views.py
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Comment
from posts.models import Post

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content', '')
        parent_id = request.POST.get('parent_id')
        parent = None
        if parent_id:
            parent = get_object_or_404(Comment, id=parent_id)

        comment = Comment.objects.create(
            post=post,
            author=request.user,
            content=content,
            parent=parent
        )
        if 'file' in request.FILES:
            comment.file = request.FILES['file']
            comment.save()
    return redirect('post_detail', post_id)

# ADD THIS FUNCTION — WAS MISSING!
@login_required
def add_reply(request, pk):
    parent_comment = get_object_or_404(Comment, id=pk)
    if request.method == 'POST':
        content = request.POST.get('content', '')
        reply = Comment.objects.create(
            post=parent_comment.post,
            author=request.user,
            content=content,
            parent=parent_comment
        )
        if 'file' in request.FILES:
            reply.file = request.FILES['file']
            reply.save()
    return redirect('post_detail', parent_comment.post.id)