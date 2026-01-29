from django.shortcuts import render

# Create your views here.
# communities/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Community

@login_required
def community_list(request):
    communities = Community.objects.all()
    return render(request, 'communities/list.html', {'communities': communities})

@login_required
def create_community(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        community = Community.objects.create(
            name=name,
            description=description,
            creator=request.user,
            domain="General"
        )
        community.members.add(request.user)
        return redirect('community_detail', community.id)
    return render(request, 'communities/create.html')

@login_required
def community_detail(request, pk):
    community = get_object_or_404(Community, pk=pk)
    return render(request, 'communities/detail.html', {'community': community})

@login_required
def join_community(request, pk):
    community = get_object_or_404(Community, pk=pk)
    community.members.add(request.user)
    return redirect('community_detail', pk)