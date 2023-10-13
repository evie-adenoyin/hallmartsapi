from dataclasses import fields
from rest_framework.serializers import ModelSerializer, StringRelatedField, IntegerField, ValidationError


from shop.models import Order
from shop.serializers import OrderSerializer, WishListSerializer

from  .models import User, UserAddress, UserProfile
# User Serializers 

class UserRegistrationSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['email' ,'username','reg_no', 'university', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            university = validated_data['university'],
            reg_no = validated_data['reg_no'],
        )

        

        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def validate_email(self, value):
    
        checkUser = User.objects.filter(email =value, )
        if checkUser:
            raise ValidationError("user with this email address already exists.")
        return value
    def validate_reg_no(self, value):
        checkUser = User.objects.filter( reg_no= value, )
        if checkUser:
            raise ValidationError("user with this Registration number already exists.")
        return value


class UserSerializer(ModelSerializer):
    userorder = OrderSerializer( many= True, read_only = True)
    userwishlist = WishListSerializer()
    class Meta:
        model = User
        fields = ['id','email', 'university', 'reg_no', 'userorder', 'userwishlist','vendor_role','username','first_name','last_name']


class UserAddressSerializer(ModelSerializer):
    class Meta:
        model = UserAddress
        fields = ['city', 'state','home', 'phone']


class UserProfileSerializer(ModelSerializer):
    address = UserAddressSerializer(read_only = True)
    user = UserSerializer(read_only = True)
    class Meta:
        model = UserProfile
        fields = ['user', 'address']


class UserOrderAnalyticsSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ['id','user' ]
        # fields = ['id','total_orders','order_token','user', 'completed','userorder' ]
  
