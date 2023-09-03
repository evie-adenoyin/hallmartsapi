from django.urls import path, re_path
from .views import (
 ProductListAPIView,
 ProductDetailAPIView,
 ProductSearchAPIView,
 CartAPIView,
 NavbarCategoryAPIView,
 WishListAPIView,
 AddToCartDetailPageViewSet,
 AddressAPIView,
 CartTotalAPIView
)

app_name = 'shop'

urlpatterns = [
   
   # Navbar categories endpoint
   path('categories', NavbarCategoryAPIView.as_view(), name='categories-list'),

   # Product info endpoints
   path('products', ProductListAPIView.as_view(), name='product-list'),
   path('products/search', ProductSearchAPIView.as_view(), name='product-search'),
   path('product/<str:slug>', ProductDetailAPIView.as_view(), name='product-detail'),

   # Cart action endpoints 
   path('add/to/cart/details', AddToCartDetailPageViewSet.as_view(), name='add-to-cart'),
   path('cart', CartAPIView.as_view(), name='cart-update'),
   path('cart/total', CartTotalAPIView.as_view(), name='cart-total'),

   # Wishlist endpoint 
   path('wishlist', WishListAPIView.as_view(), name='wishlist'),

   #Address endpoint
   path('user/address', AddressAPIView.as_view(), name='address')
]
