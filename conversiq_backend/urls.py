from django.http import JsonResponse
from django.urls import path, include

def health_check(request):
    return JsonResponse({"message": "ConversIQ backend running OK"})

urlpatterns = [
    path("", health_check),
    path("api/", include("chatapp.urls")),
]
