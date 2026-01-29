# messaging/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('direct/<int:user_id>/', views.direct_message, name='direct_message'),
    path('group/<int:conv_id>/', views.group_chat, name='group_chat'),
]