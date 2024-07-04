from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView
)

from . import apis

urlpatterns = [
    path('register/', apis.RegisterApi.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh')
]