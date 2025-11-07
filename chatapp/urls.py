# FILE: chatapp/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, search_messages
from .views import recall_context

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

urlpatterns = [
    path('', include(router.urls)),
    path('search/', search_messages, name='semantic-search'),
     path("recall/", recall_context, name="recall-context"),
]
