
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from django.core.exceptions import ObjectDoesNotExist
# DRF imports
from rest_framework.response import Response
from rest_framework.generics import (
    RetrieveUpdateAPIView,
    RetrieveDestroyAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    GenericAPIView
)
from rest_framework.views import APIView
from rest_framework import status 
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from shop.serializers import OrderSerializer

from .serializers import (
    UserProfileSerializer,
    UserRegistrationSerializer,
    UserOrderAnalyticsSerializer,
    UserSerializer,
    UserAddressSerializer
                )

from .models import (
               UserProfile,
               UserAddress,
             
                )

from .permissions import UserObjectPermission

User = get_user_model()

# UserAPIView  

class UserRegistrationApiView(APIView):

    def post(self, request):
        data = request.data
        serializer = UserRegistrationSerializer(data = data)
        if serializer.is_valid(raise_exception=True): 
            serializer.save()
            return Response(serializer.data, status =status.HTTP_201_CREATED)
        return Response(serializer.errors)


class UserAPIView(RetrieveUpdateAPIView):
    # permission_classes = [UserObjectPermission]
    # serializer_class = UserProfileSerializer
    # queryset = UserProfile.objects.all()

    def get(self,request):
        user= request.user
        
        try:
            profile = UserProfile.objects.get( user__id=user.id)
        except ObjectDoesNotExist:
            return Response({"message":"No profile found with this user."}, status = status.HTTP_404_NOT_FOUND)
        if profile:
            serializer = UserProfileSerializer(profile, context={'request': request})
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response({"message":"No profile found with this user."}, status = status.HTTP_404_NOT_FOUND)
    
    def post(self,request):
        user = request.user
        data = request.data
        print(user.id)
      
        try:
            user_profile = UserProfile.objects.get( user__id=user.id)
            user_address,create = UserAddress.objects.get_or_create( user=user_profile)
            
            serializer = UserAddressSerializer(user_address, data = data, context={'request': request})
        except ObjectDoesNotExist:
            return Response({"message":"No profile found with this user."}, status = status.HTTP_404_NOT_FOUND)
       
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response({"message":"No profile found with this user."}, status = status.HTTP_404_NOT_FOUND)
    

class PasswordChangeAPIView(APIView):

    def post(self, request):
        data = request.data
        user = User.objects.get(id = request.user.id)
        password = user.check_password(data['oldpassword'])
        if password:
            user.set_password(data['newpassword'])
            user.save()
            return Response({"message":"Password updated."}, status = status.HTTP_200_OK)
        return Response({"message":"Old password is incorrect."}, status = status.HTTP_400_BAD_REQUEST)
    
        
