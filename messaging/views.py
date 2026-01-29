# messaging/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Conversation, ConversationParticipant, Message

User = get_user_model()

@login_required
def inbox(request):
    # Get conversations where user is a participant
    participant_entries = ConversationParticipant.objects.filter(
        user=request.user, 
        has_left=False
    ).select_related('conversation')
    
    conversations = [entry.conversation for entry in participant_entries]
    
    # Add unread count
    for conv in conversations:
        conv.unread_count = conv.messages.filter(is_read=False).exclude(sender=request.user).count()
    
    return render(request, 'messaging/inbox.html', {'conversations': conversations})

@login_required
def direct_message(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    
    # Find existing direct conversation between two users
    conversation = Conversation.objects.filter(
        type='direct',
        conversationparticipant__user=request.user
    ).filter(
        conversationparticipant__user=other_user
    ).distinct().first()
    
    # Create if not exists
    if not conversation:
        conversation = Conversation.objects.create(type='direct')
        ConversationParticipant.objects.create(conversation=conversation, user=request.user)
        ConversationParticipant.objects.create(conversation=conversation, user=other_user)
    
    messages = conversation.messages.all().order_by('timestamp')
    
    return render(request, 'messaging/chat.html', {
        'conversation': conversation,
        'other_user': other_user,
        'messages': messages
    })

@login_required
def group_chat(request, conv_id):
    conversation = get_object_or_404(Conversation, id=conv_id, type='group')
    
    # Check if user is member
    if not ConversationParticipant.objects.filter(
        conversation=conversation, 
        user=request.user, 
        has_left=False
    ).exists():
        return redirect('inbox')
    
    messages = conversation.messages.all().order_by('timestamp')
    
    return render(request, 'messaging/chat.html', {
        'conversation': conversation,
        'messages': messages
    })