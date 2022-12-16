from django.urls import path, re_path
from .views import VendorDashboardApiView, VendorCreateApiView, VendorOrderApiView

app_name = 'vendor'

urlpatterns = [
    path('registration', VendorCreateApiView.as_view(), name='vendor_registration'),
    path('dashboard', VendorDashboardApiView.as_view(), name='vendor'),
    path('order/items', VendorOrderApiView.as_view(), name='vendor_order'),
]