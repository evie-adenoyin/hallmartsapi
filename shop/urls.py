from django.urls import path, re_path
from .views import (
 ProductListAPIView,
 ProductDetailAPIView,
 ProductSearchAPIView,
 CartUpdateAPIView,
 NavbarCategoryAPIView,
 WishListSearchAPIView,
 AddToCartDetailPageViewSet
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
   path('cart/<str:token>', CartUpdateAPIView.as_view(), name='cart-update'),

   # Wishlist endpoint 
   path('wishlist/<str:code>', WishListSearchAPIView.as_view(), name='wishlist'),
]
