from django.urls import path, re_path
from .views import (
    UserAPIView, 
    UserRegistrationApiView,
    PasswordChangeAPIView
)

app_name = 'user'

urlpatterns = [
    path('registration', UserRegistrationApiView.as_view(), name = 'user-registration'),
    path('account/profile', UserAPIView.as_view(), name = "user-account"),
    path('change/password', PasswordChangeAPIView.as_view(), name = "change-password"),
]
