from email.policy import HTTP
import secrets
 


# DRF imports 
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    # RetrieveUpdateAPIView,
    # UpdateAPIView,
    # GenericAPIView
) 
from rest_framework.views import APIView
from rest_framework import status 
from rest_framework.viewsets import ViewSet
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import AllowAny, IsAuthenticated
# 3rd party app filter
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from user.permissions import UserObjectPermission
# from .permissions import WishListObjectPermission
from .filters import ProductFilter
from .pagination import ProductListLimitOffsetPagination

from .models import (
                Color,
                Size,
                Product, 
                Category,
                Order, 
                OrderProduct,
                WishList,
                FirstLayerCategory,
                SecondLayerSubCategory
                )
from .serializers import(
     ProductSerializers,
     OrderSerializer,
     OrderProductSerializer,
     NavbarCategorySerializer,
     WishListSerializer
)

from rest_framework.permissions import IsAuthenticated


# from rest_framework_simplejwt.authentication import JWTStatelessUserAuthentication


class NavbarCategoryAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = NavbarCategorySerializer


class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter
    pagination_class = ProductListLimitOffsetPagination
   


class ProductDetailAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    lookup_field = 'slug'
    # permission_classes = [IsAuthenticated]

     


# Todo: Set permissions 
# Generate toekn from FrontEnd 
class AddToCartDetailPageViewSet(APIView):
    permission_classes = [AllowAny]

    # def get(self,request, *args, **kwargs):
    #     visitor = secrets.token_hex(10)
    #     order, create = Order.objects.get_or_create(completed = False,  visitor = visitor)
    #     serializer = OrderSerializer(order, context={'request': request})
    #     return Response(serializer.data, status = status.HTTP_200_OK)

    def post(self,request, *args, **kwargs):
        data = request.data
        product_id = request.data.get('product')
        slug = request.data.get('slug')
        product_Qt = request.data.get('quantity')
        product_color = request.data.get('color')
        product_size = request.data.get('size')
        order_token = request.data.get('token')
        if order_token:
            order, create = Order.objects.get_or_create(completed = False,  order_token = order_token)
        
        product = Product.objects.get(id =product_id, slug = slug)
        color = Color.objects.get(id= product_color)
        size = Size.objects.get(id= product_size)
        order_product, create = OrderProduct.objects.get_or_create(order= order, product = product)  
        order_product.quantity = product_Qt
        order_product.color = color.color
        order_product.size = size.size
        order_product.save()
        serializer = OrderSerializer(order, context={'request': request}, data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class CartUpdateAPIView(APIView):
    permission_classes = [AllowAny]
   
    def get(self,request, token):
        try:
            order = Order.objects.get( order_token = token, completed = False)
        except ObjectDoesNotExist:
            return Response({"message":"You have no orders, add to cart."}, status = status.HTTP_404_NOT_FOUND)
        if order:
            serializer = OrderSerializer(order, context={'request': request})
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response({"message":"You have no orders, add to cart."}, status = status.HTTP_404_NOT_FOUND)


    def post(self,request, token=None):
        orderproduct_id = request.data.get('orderproduct_id')
        action = request.data.get('action')
        order_token = request.data.get('token')
        order = Order.objects.get( order_token = order_token, completed = False)
        orderproduct = OrderProduct.objects.get(order = order, id = orderproduct_id)
    
        if action =="add":
            orderproduct.quantity +=1
            orderproduct.save()
        if action =="remove":
            orderproduct.quantity -=1
            orderproduct.save()
        if action =="delete" or orderproduct.quantity==0:
            orderproduct.delete()  
        serializer = OrderSerializer(order, context={'request': request})
        return Response(data = serializer.data, status = status.HTTP_200_OK)
      
        
# Generate toekn from FrontEnd 
class WishListSearchAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self,request, code =None):
        code_id = code
        wishlist = WishList.objects.filter(code = code_id)
        if wishlist.exists():
            serializer = WishListSerializer(wishlist, context={'request': request})
            return Response(serializer.data, status = status.HTTP_200_OK) 
        return Response({"message":f"Sorry we couldn't find a wishlist with code '{code}', try again."}, status = status.HTTP_404_NOT_FOUND) 

        
    def post(self,request, code=None):
        data = request.data
        product_id = request.data.get('product')
        slug = request.data.get('slug')
        code_id = request.data.get('code')

        product = Product.objects.get(id =product_id, slug = slug)
        wishlist, create = WishList.objects.get_or_create( code = code_id)
        product_qs =wishlist.products.filter(id = product.id)
        if product_qs.exists():
            return Response({"message":f"{product}, is already in wishlist."}, status = status.HTTP_200_OK)
        wishlist.products.add(product)
        serializer = WishListSerializer(wishlist, data = data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
       

        




