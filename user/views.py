
import jwt
from django.urls import reverse
from django.http import  HttpResponseRedirect


from django.core import exceptions
# DRF imports
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import (
    RetrieveUpdateAPIView,
    RetrieveDestroyAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    GenericAPIView
)
from django.core.mail import send_mail


from rest_framework.views import APIView
from rest_framework import status 
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.contrib.sites.shortcuts import get_current_site
from shop.serializers import OrderSerializer

from .serializers import (
    UserRegistrationSerializer,
    UserSerializer,
    LoginSerializer
                )

from .models import (
               User,
               UserAddress,
             
                )

from .permissions import UserObjectPermission


# UserAPIView  

class UserRegistrationApiView(APIView):

    def post(self, request):
        data = request.data
        serializer = UserRegistrationSerializer(data = data)
        
        
        if serializer.is_valid(raise_exception=True): 
            serializer.save()
            
            # getting tokens
            valid_user_info = serializer.data
            user_id = User.objects.get(id=valid_user_info['id'])
            token = RefreshToken.for_user(user_id).access_token

             # send email for user verification
            current_site = get_current_site(request).domain
            
            print("token :", token)
            relative_link = reverse('user:verify-email')
            absurl = 'http://'+current_site+relative_link+"?token="+str(token)
            print("url link: ", absurl)
            email_body = 'Hi '+valid_user_info['username'] + \
                ' Use the link below to verify your email \n' + absurl
            email_data = {'email_body': email_body, 'to_email': valid_user_info['email'],
                    'email_subject': 'Verify your email'}
            
            send_mail(
                "Email verification",
                email_body,
                "admin@hallmarts.com",
                [valid_user_info['email']],
                fail_silently=False,
)
            
            return Response(serializer.data, status =status.HTTP_201_CREATED)

        return Response(serializer.errors)
  
    
class UserEmailVerificationAPIView(APIView):
     
     def get(self, request):
        token = request.GET.get('token')
        decode_token = jwt.decode(token, algorithms='HS256', options={"verify_signature": False})
        try:
            user = User.objects.get(id = decode_token['user_id'])
        except exceptions.ObjectDoesNotExist:
             return Response({"message": f"No user found with email {user.email}."}, status =status.HTTP_201_CREATED)
        user.email_verified = True
        user.save()
        return Response({"message": f"Your email {user.email} has been verified"}, status =status.HTTP_201_CREATED)
     

class LoginAPIView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.get_token(email=serializer.validated_data.get("email"))
        return Response(data=token, status=status.HTTP_200_OK)


class UserAPIView(RetrieveUpdateAPIView):
    # permission_classes = [UserObjectPermission]
    # serializer_class = UserProfileSerializer
    # queryset = UserProfile.objects.all()

    def get(self,request):
        user_req= request.user
        
        try:
            user = User.objects.get( id=user_req.id)
        except exceptions.ObjectDoesNotExist:
            return Response({"message":"No user found with this user."}, status = status.HTTP_404_NOT_FOUND)
        if user:
            serializer = UserSerializer(user, context={'request': request})
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response({"message":"No user found with this user."}, status = status.HTTP_404_NOT_FOUND)
    
    def post(self,request):
        user = request.user
        data = request.data
        print(user.id)
      
        try:
            user = User.objects.get( id=user.id)
            serializer = UserSerializer(user, data = data, context={'request': request})
        except exceptions.ObjectDoesNotExist:
            return Response({"message":"No user found."}, status = status.HTTP_404_NOT_FOUND)
       
        if serializer.is_valid(raise_exception=True):
            serializer.save() 
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response({"message":"No user found."}, status = status.HTTP_404_NOT_FOUND)
    

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
    
        
