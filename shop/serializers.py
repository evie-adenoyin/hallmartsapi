from cProfile import label
from dataclasses import fields
from itertools import product
from unicodedata import category

from django.forms import IntegerField
from rest_framework.serializers import (
    ModelSerializer, 
    StringRelatedField, 
    HyperlinkedIdentityField,
    CharField,
    IntegerField
)

from comment.serializers import CommentSerializer
# from comment.serializers import CommentSerializer
from vendor.models import Vendor
from .models import (
    Product, 
    Order,
    OrderProduct,
    Category,
    FirstLayerCategory,
    SecondLayerSubCategory,
    WishList,
    Size,
    Color
    )



class VendorSerializer(ModelSerializer):
    class Meta:
        model = Vendor
        fields = "__all__"



# Category API Serializer

class ProductSizeSerializer(ModelSerializer):
    class Meta:
        model = Size
        fields = ['id','size']

class ProductColorSerializer(ModelSerializer):
    class Meta:
        model = Color
        fields = ['id','color']

class SecondLayerCategorySerializer(ModelSerializer):
    class Meta:
        model = SecondLayerSubCategory
        fields = ['id','name']

class FirstLayerCategorySerializer(ModelSerializer):
    class Meta:
        model = FirstLayerCategory
        fields = ['id','name']

class CategorySerializer(ModelSerializer):
    # firstlayercategories = FirstLayerCategorySerializer(many=True, read_only=True)
    class Meta:
       model = Category
       fields = ['id','name']


# Navbar API serializer

class SubCategorySerializer(ModelSerializer):
    secondlayercategories = SecondLayerCategorySerializer(many = True, read_only = True)
    class Meta:
        model = Category
        fields = ['id','name', 'secondlayercategories']

class NavbarCategorySerializer(ModelSerializer):
    firstlayercategories = SubCategorySerializer(many = True, read_only = True)
    class Meta:
        model = Category
        fields = ['id','name', 'firstlayercategories']
   

# Product API Serializer 

# product comment API Serializer

class ProductSerializers(ModelSerializer):
    detail_link = HyperlinkedIdentityField(view_name='shop:product-detail', lookup_field = 'slug')
    category = CategorySerializer(many=True,read_only=True)
    first_category=FirstLayerCategorySerializer(many=True,read_only=True)
    second_category=SecondLayerCategorySerializer(many=True,read_only=True)
    product_size =ProductSizeSerializer(many=True,read_only=True)
    product_color =ProductColorSerializer(many=True,read_only=True)
    vendor =VendorSerializer(read_only=True)
    comments = CommentSerializer(read_only = True, many= True)
    class Meta:
        model = Product
        fields = ['vendor','id','name','slug','detail_link','price','discount','grade',
                  'discount_percentage','new_price','stock','image_1','image_2','image_3','product_size','product_color','category','first_category','second_category','description','additional_info','shipping','tag','rating','liked','comments']




# Order Products API Serializer 

class OrderProductSerializer(ModelSerializer):
    product = ProductSerializers(read_only=True)
    class Meta:
        model = OrderProduct
        fields =['id','product', 'quantity', 'total_cost_of_product', 'color', 'size', ]


class OrderSerializer(ModelSerializer):
    user = StringRelatedField(read_only = True)
    orders = OrderProductSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id','transaction_id','order_token','user','in_transit', 'completed','total_quantity_of_product_in_order','date_created', 'total_cost_of_product_in_order','total_discount_of_product_in_order', 'orders','date_ordered' ]
  



class WishListSerializer(ModelSerializer):
    products = ProductSerializers(many =True, read_only = True)
    user = CharField(max_length=2000, read_only = True)
    class Meta:
        model = WishList
        fields = ['code','user','products', 'new_price_sum_total','price_sum_total','private']
