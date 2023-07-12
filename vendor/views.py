from rest_framework.response import Response
# from rest_framework.generics import (
#     ListAPIView,
#     RetrieveAPIView,
#     RetrieveUpdateAPIView,
#     UpdateAPIView,
#     GenericAPIView
# ) 
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    # RetrieveUpdateAPIView,
    # UpdateAPIView,
    # GenericAPIView
) 
from shop.serializers import ProductSerializers, OrderProductSerializer
from shop.models import OrderProduct, Order, Product
from .models import Vendor
from .serializers import VendorDashboardSerializer, VendorCreateUpdateSerializer, VendorListSerializer
from .emailServer import VendorRegistrationEmail


class VendorCreateApiView(APIView):
    
    def post(self, request):
        data = request.data
        print(data)
        serializer = VendorCreateUpdateSerializer(data=data)
        if serializer.is_valid():
            if serializer.validated_data['graduate']=="True" or serializer.validated_data['graduate']=="true":
                serializer(graduate = True)
            serializer.save()
            VendorRegistrationEmail(email = serializer.data['email'],vendor =serializer.data['vendor'],brand = serializer.data['brand'])
            return Response({"message":"You have been added to our waitlist!"}, status = status.HTTP_201_CREATED)     
        return Response(serializer.errors)

class VendorListApiView(ListAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorListSerializer

    
class VendorDashboardApiView(APIView):

    def get(self,request):
        user = request.user
        vendor_dashboard = Vendor.objects.get(user = user)
        serializer = VendorDashboardSerializer(vendor_dashboard, context={'request': request})
        return Response(serializer.data, status = status.HTTP_200_OK )

    def post(self,request):
        data =request.data
        serializer = ProductSerializers(data = data)
        if serializer.valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK )
        return Response(serializer.error, status = status.HTTP_403_FORBBIDEN)


class VendorOrderApiView(APIView):

    def get(self,request):
        vendor_id = 2
        vendor = Vendor.objects.get(user = vendor_id)
        order_products = OrderProduct.objects.filter(product__vendor = vendor)
        print("products :", order_products)
        serializer = OrderProductSerializer(order_products, context={'request': request}, many = True)
        print(serializer.data)
        return Response(serializer.data, status = status.HTTP_200_OK )

    # def post(self,request):
    #     data =request.data
    #     serializer = ProductSerializers(data = data)
    #     if serializer.valid():
    #         serializer.save()
    #         return Response(serializer.data, status = status.HTTP_200_OK )
    #     return Response(serializer.error, status = status.HTTP_403_FORBBIDEN)
