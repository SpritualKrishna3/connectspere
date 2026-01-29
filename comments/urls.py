# comments/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:post_id>/', views.add_comment, name='add_comment'),
    path('reply/<int:pk>/', views.add_reply, name='add_reply'),  # Fixed: <int:pk> not <int:pk>/reply/
]