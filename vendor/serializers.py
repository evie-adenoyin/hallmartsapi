from rest_framework.serializers import (
    ModelSerializer, 
   ValidationError
)


from shop.serializers import VendorSerializer, ProductSerializers
from .models import Vendor


class VendorCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['email','vendor','brand','university','category', 'graduate']


# {
#     "email":"guonnie@gmail.com",
#     "vendor":"Odokuma",
#     "brand":"Daventy",
#     "university":"lanmark University",
#     "category":"We services"
# }


class VendorDashboardSerializer(ModelSerializer):
    products = ProductSerializers(many = True)
    class Meta:
        model = Vendor
        fields = ['user','vendor','email','university','brand','total_stock','expected_revenue','current_sale','products',]

