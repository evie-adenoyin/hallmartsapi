from dataclasses import fields
from rest_framework.serializers import ModelSerializer


from  .models import User, UserAddress, UserProfile

from shop.serializers import OrderSerializer, WishListSerializer

# User Serializers 

class UserRegistrationSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            university = validated_data['username'],
            reg_no = validated_data['reg_no'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user


class UserSerializer(ModelSerializer):
    userorder = OrderSerializer( many= True, read_only = True)
    userwishlist = WishListSerializer()
    class Meta:
        model = User
        fields = ['id','email', 'university', 'reg_no', 'userorder', 'userwishlist']


class UserAddressSerializer(ModelSerializer):
    class Meta:
        model = UserAddress
        fields = ['city', 'state', 'country']


class UserProfileSerializer(ModelSerializer):
    address = UserAddressSerializer(read_only = True)
    user = UserSerializer(read_only = True)
    class Meta:
        model = UserProfile
        fields = ['user', 'address']


