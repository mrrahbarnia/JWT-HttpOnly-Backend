from django.urls import path

from . import apis

urlpatterns = [
    path('register/', apis.RegisterApi.as_view(), name='register'),
    path('login/', apis.MyTokenObtainPairView.as_view(), name='login'),
    path('change-password/', apis.ChangePasswordApi.as_view(), name='change_password'),
]