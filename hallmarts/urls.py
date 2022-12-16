
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('shop/', include('shop.urls'), name='shop'),
    path('user/', include('user.urls'),name='user'),
    path('vendor/', include('vendor.urls'),name='vendor'),
    path('comments/', include('comment.urls'),name='comments'),



    # JWT Authentication 
    path('auth/api/acss', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/api/ref', TokenRefreshView.as_view(), name='token_refresh'),

]


if settings.DEBUG:
    urlpatterns += static (settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)