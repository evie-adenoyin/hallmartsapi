from django.urls import path, re_path
from .views import (
    UserAPIView, 
    UserRegistrationApiView,
    UserEmailVerificationAPIView,
    LoginAPIView,
    PasswordChangeAPIView,
)

app_name = 'user'

urlpatterns = [
    path('registration', UserRegistrationApiView.as_view(), name = 'user-registration'),
    path('verify-email', UserEmailVerificationAPIView.as_view(), name = 'verify-email'),
    path('login', LoginAPIView.as_view(), name = 'login'),
    path('account/profile', UserAPIView.as_view(), name = "user-account"),
    path('change/password', PasswordChangeAPIView.as_view(), name = "change-password"),
]
