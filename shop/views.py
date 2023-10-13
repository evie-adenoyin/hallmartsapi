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
from rest_framework import status, filters
from rest_framework.viewsets import ViewSet
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import AllowAny, IsAuthenticated
# 3rd party app filter
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from user.models import User
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
                SecondLayerSubCategory,
                Address,
                ShippingAddress
                )
from .serializers import(
     ProductSerializers,
     OrderSerializer,
     OrderProductSerializer,
     NavbarCategorySerializer,
     WishListSerializer,
     AddressSerializer,
     ShippingAddressSerializer,
     CartTotalSerializer
)

from rest_framework.permissions import IsAuthenticated




# from rest_framework_simplejwt.authentication import JWTStatelessUserAuthentication



# DONE : ALl category API
class NavbarCategoryAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = NavbarCategorySerializer


# All products API 
class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter
    pagination_class = ProductListLimitOffsetPagination
   

# DONE :  Search items API 
class ProductSearchAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    filter_backends = [filters.SearchFilter]
    search_fields = ['name',"price", "tag",  "product_size__size","product_color__color", "category__name", "first_category__name","second_category__name",'vendor__university', 'vendor__vendor']

# DONE: Product Detail API
class ProductDetailAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    lookup_field = 'slug'

     


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
        user_id = request.user.id
        
        product_id = request.data.get('product_id')
        slug = request.data.get('slug')
        product_Qt = request.data.get('quantity')
        product_color = request.data.get('color')
    
        product_size = request.data.get('size')
       
        user = User.objects.get(id=user_id)
        try:
            order = Order.objects.get(user=user, completed = False )
            print("color ",product_color)
        except ObjectDoesNotExist:
            order = Order.objects.create(completed = False, user=user)
            print("color ",product_color)
        
        product = Product.objects.get(id =product_id, slug = slug)
        color = Color.objects.get(id= product_color)
        size = Size.objects.get(id= product_size)
        try:
            order_product=  OrderProduct.objects.get(order= order, product = product) 
            return Response({'message':'Item already in cart'}, status = status.HTTP_200_OK)
        except ObjectDoesNotExist:
            order_product = OrderProduct.objects.create(order= order, product = product) 
            order_product.quantity = product_Qt
            order_product.color = color.color
            order_product.size = size.size
            order_product.save()
            order.save()
            serializer = OrderSerializer(order, context={'request': request}, data = data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class CartAPIView(APIView):
    permission_classes = [AllowAny]
   
    def get(self,request):
        user=request.user.id
        try:
            order = Order.objects.get( user= user , completed = False)
        except ObjectDoesNotExist:
            return Response({"message":"You have no orders, add to cart."}, status = status.HTTP_200_OK)
        if order:
            serializer = OrderSerializer(order, context={'request': request})
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response({"message":"You have no orders, add to cart."}, status = status.HTTP_200_OK)


    def post(self,request,):
        orderproduct_id = request.data.get('orderproduct_id')
        action = request.data.get('action')
        transaction_id = request.data.get('transaction_id')
        order = Order.objects.get( completed = False, transaction_id = transaction_id)
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
        return Response(serializer.data, status = status.HTTP_200_OK)
      
class CartTotalAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        
        user = request.user.id
       
        try:
            cart_total = Order.objects.get(user=user, completed = False)
            serializer = CartTotalSerializer(cart_total, context={'request': request})
            return Response(serializer.data, status = status.HTTP_200_OK)
        except ObjectDoesNotExist:
            print("Cart total ", request.user)
            return Response({"data":0}, status = status.HTTP_200_OK)

       

# Generate token from FrontEnd 
class WishListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self,request, code =None):
        wishlist = WishList.objects.filter(code = code)
        if wishlist.exists():
            serializer = WishListSerializer(wishlist, context={'request': request})
            return Response(serializer.data, status = status.HTTP_200_OK) 
        return Response({"message":f"Sorry we couldn't find a wishlist with code '{code}', try again."}, status = status.HTTP_404_NOT_FOUND) 

        
    def post(self,request):
        data =request.data
        user = User.objects.get(id =request.user.id )
        product_id = request.data.get('product')
        slug = request.data.get('slug')
        code_id = request.data.get('code')
        action = request.data.get('action')

        product = Product.objects.get(id =product_id, slug = slug)
        wishlist, create = WishList.objects.get_or_create( user= user, code = code_id)
        product_qs =wishlist.products.filter(id = product.id)
        if action == 'remove':
            wishlist.products.remove(product)

        elif action =='add':
            if product_qs.exists():
                return Response({"message":f"{product}, is already in wishlist."}, status = status.HTTP_200_OK)
            wishlist.products.add(product)
            return Response({"message":f"{product}, added to wishlist."}, status = status.HTTP_200_OK)
      
        serializer = WishListSerializer(wishlist, data = data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
       

class AddressAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self,request):
        user = request.user.id
        try:
            address = Address.objects.get(user = user)
        except ObjectDoesNotExist:
            return Response({'message':'No address found for this user'}, status = status.HTTP_404_NOT_FOUND)
        if address:
            serializer = AddressSerializer(address,context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)

class ShippingAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self,request):
        user = request.user.id
        try:
            shipping_address = ShippingAddress.objects.get(user = user)
        except ObjectDoesNotExist:
            return Response({'message':'No shipping address found for this user'}, status = status.HTTP_404_NOT_FOUND)
        if shipping_address:
            serializer = ShippingAddressSerializer(shipping_address,context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
