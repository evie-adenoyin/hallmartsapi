from django.urls import path, re_path
from .views import (
    UserAPIView, 
    UserRegistrationApiView
)

app_name = 'user'

urlpatterns = [
    path('registration', UserRegistrationApiView.as_view(), name = 'user_registration'),
    path('account/profile/<int:pk>/', UserAPIView.as_view(), name = "user_account"),
]