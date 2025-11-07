# FILE: conversiq_backend/urls.py
from django.urls import path, include

urlpatterns = [
    path('api/', include('chatapp.urls')),
]
