from django.contrib import auth

from rest_framework import serializers  
from rest_framework import exceptions
from rest_framework_simplejwt.tokens import RefreshToken

from shop.models import Order
from shop.serializers import OrderSerializer, WishListSerializer

from  .models import User, UserAddress


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email' ,'username','reg_no', 'university', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            university = validated_data['university'],
            reg_no = validated_data['reg_no'],
            username = validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def validate_email(self, value):
        checkUser = User.objects.filter(email =value, )
        if checkUser:
            raise serializers.ValidationError("User with this email address already exists.")
        return value
    def validate_reg_no(self, value):
        checkUser = User.objects.filter( reg_no= value, )
        if checkUser:
            raise serializers.ValidationError("User with this registration number already exists.")
        return value

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["email", "password"]
        write_only_fields = ["password"]

    def for_user(self, user: User):
        token = RefreshToken.for_user(user)
        token["vendor_role"] = user.vendor_role
        return token

    def validate(self, attrs):
        email = attrs.get("email", "")
        password = attrs.get("password", "")
        user = auth.authenticate(email=email.lower(), password=password)

        if not user:
            raise exceptions.AuthenticationFailed({"message": "Invalid credentials, try again"})
        if not user.is_active:
            raise exceptions.AuthenticationFailed({"message": "Account disabled, contact admin"})
        if not user.email_verified:
            raise exceptions.AuthenticationFailed({"message": "Email is not verified"})
        return attrs

    def get_token(self, email: str) -> dict:
        # inline imports
        from datetime import datetime

        user: User = User.objects.filter(email=email.lower()).first()
        user.last_login = datetime.now()
        user.save(update_fields=["last_login"])

        token: RefreshToken = self.for_user(user)
        return {
            "token": str(token.access_token),
            "user_info": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "last_login": user.last_login,
            },
        }





class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = ['city', 'state','home', 'phone']


class UserSerializer(serializers.ModelSerializer):
    userorder = OrderSerializer( many= True, read_only = True)
    userwishlist = WishListSerializer()
    user_address = UserAddressSerializer(read_only = True)
    class Meta:
        model = User
        fields = ['id','email','user_address', 'university', 'reg_no', 'userorder', 'userwishlist','vendor_role','username','first_name','last_name']




class UserOrderAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id','user' ]
        # fields = ['id','total_orders','order_token','user', 'completed','userorder' ]
  
