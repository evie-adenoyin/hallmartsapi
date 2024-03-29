# from random import choices
from cgitb import strong
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
import secrets
from PIL import Image
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.forms import CharField, MultipleChoiceField
from user.models import User
from django_countries.fields import CountryField
from django.utils.text import slugify
from django.core.files.storage import default_storage as storage 

from vendor.models import Vendor




class Category(models.Model):
    name =  models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['-id']

    def __str__(self):
        return self.name

class FirstLayerCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE , null = True, blank = True, related_name='firstlayercategories')
    name =  models.CharField(max_length=50,null = True, blank = True)
    
    class Meta:
        verbose_name_plural = 'First layer categories'

    def __str__(self):
        return f'{self.name}'

class SecondLayerSubCategory(models.Model):
    firstlayercategory = models.ForeignKey(FirstLayerCategory, on_delete=models.CASCADE , null = True, blank = True, related_name='secondlayercategories')
    name =  models.CharField(max_length=50,null = True, blank = True)

    class Meta:
        verbose_name_plural = 'Second layer categories'

    def __str__(self):
        return f'{self.name}'



class Size (models.Model):
    size = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.size}'

class Color (models.Model):
    color = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.color}'
    

class Product(models.Model):
    GRADE = (
        ('thrift', 'thrift'),
        ('brand new', 'brand new'),
        ('first grade', 'first grade'),
        ('second grade', 'second grade'),
    )
      
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null = True, blank = True, related_name='products')
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    discount = models.IntegerField(default=0, null = True, blank = True) 
    new_price = models.IntegerField(default=0)
    discount_percentage = models.FloatField(default=0)
    stock = models.IntegerField(default=1)
    image_1 = models.ImageField(upload_to='images/' ,null = True, blank = True)
    image_2 = models.ImageField(upload_to='images/', null = True, blank = True)
    image_3 = models.ImageField(upload_to='images/', null = True, blank = True)
    category= models.ManyToManyField(to=Category, related_name='categories')
    first_category= models.ManyToManyField(to=FirstLayerCategory, related_name='firstlayercategories' )
    second_category= models.ManyToManyField(to=SecondLayerSubCategory, related_name='secondlayercategories')
    description = models.TextField(max_length=500)
    additional_info = models.TextField(max_length=500)
    shipping = models.IntegerField(default=0)
    grade = models.CharField(max_length=20, choices=GRADE, default='thrift')
    tag = models.CharField(max_length=800)
    rating = models.IntegerField(default=0)
    liked = models.BooleanField(default= False)
    product_size = models.ManyToManyField(to=Size, related_name='productsize' )
    product_color = models.ManyToManyField(to=Color, related_name='productcolor' )
    slug = models.SlugField(max_length=255, unique = True)
    approved = models.BooleanField(default= False)
    date_Created = models.DateTimeField(auto_now_add = timezone.now)
    ordered = models.BooleanField(default= False)


    


    class Meta:
        ordering = ['-id']

 
    # @property
    # def ordered_products(self):
    #     ordered_product = self.orderproducts.all()
    #     print("ordered_product:", ordered_product)
    #     return ordered_product

    def save(self, *args, **kwargs):
        vendor = str(slugify(self.vendor))
        if self.discount:
            discount_price = self.discount*100 
            self.new_price = self.price - self.discount
            self.discount_percentage = round(float(discount_price/self.price))
        else:
            self.new_price =  int(self.price)
            self.discount_percentage = 0
        if self.slug:
            self.slug = f'{slugify(self.slug)}-{vendor}'
        self.slug = f'{slugify(self.name)}-{vendor}'
        return super(Product, self).save(*args, **kwargs)
        super(Product, self).save(*args, **kwargs)
         
    def __str__(self):
        return self.name
        



class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE , null = True, blank = True, related_name='userorder')
    date_created = models.DateTimeField(auto_now_add = True)
    date_ordered = models.DateTimeField(auto_now=True, null = True, blank = True)
    completed = models.BooleanField(default = False, null = True, blank = True)
    in_transit = models.BooleanField(default = False, null = True, blank = True)
    transaction_id = models.CharField(null = True, blank = True, max_length = 12)
    order_token = models.CharField( null = True, blank = True, max_length = 30, unique=True)

    class Meta:
        ordering = ['-id']
    @property
    def total_cost_of_product_in_order(self):
        order_product = self.orders.all()
        total = sum([product.total_cost_of_product for product in order_product])
        return int(total)

    @property
    def total_quantity_of_product_in_order(self):
        order_product = self.orders.all()
        total = sum([product.quantity for product in order_product])
        return int(total)  
    @property
    def total_discount_of_product_in_order(self):
        order_product = self.orders.all()
        total = sum([product.product.discount for product in order_product])
        return int(total)  
   
  
    # def save(self,*args, **kwargs):
    #     self.visitor = secrets.token_hex(10)
    #     return super(Order, self).save(*args, **kwargs)
    def save(self,*args, **kwargs):
        self.transaction_id = secrets.token_hex(6)
        return super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return f'Order by {self.user}'
    


class OrderProduct(models.Model):
    order  = models.ForeignKey(Order, on_delete=models.CASCADE, null= True, blank = True, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null= True, blank = True, related_name='orderproducts')
    quantity = models.IntegerField(default = 0)
    color = models.CharField(null = True, blank = True, max_length = 30, default ="None")
    size = models.CharField(null = True, blank = True, max_length = 30, default ="None")
    

    class Meta:
        ordering=['-id']

    @property
    def total_cost_of_product(self):
        total = self.product.new_price * self.quantity
        return int(total)
   
    def __str__(self):
        return f"item order {self.order.user} in cart"
 


    



class ShippingAddress(models.Model):
    user =  models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)
    house_number = models.CharField( max_length=1000)
    street = models.CharField( max_length=1000)
    city = models.CharField( max_length=1000)
    State = models.CharField( max_length=1000)
    zip_code = models.CharField( max_length=1000)
    country = CountryField(multiple = False)
    apartment_address = models.CharField( max_length=1000)
    # country = CountryField(multiple = False)

    def __str__(self):
        return f'{self.user} shipping address'
    
    
class Address(models.Model):
    user =  models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)
    house_number = models.CharField( max_length=1000)
    street = models.CharField( max_length=1000)
    city = models.CharField( max_length=1000)
    State = models.CharField( max_length=1000)
    zip_code = models.CharField( max_length=1000)
    country = CountryField(multiple = False)
    apartment_address = models.CharField( max_length=1000)
    # country = CountryField(multiple = False)

    def __str__(self):
        return f'{self.user} shipping address'
     


class WishList(models.Model):
    address = models.OneToOneField(ShippingAddress,null=True, blank=True, on_delete=models.SET_NULL)
    code = models.CharField( max_length=4, null = True, blank = True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE , null = True, blank = True, related_name='userwishlist')
    products = models.ManyToManyField(Product)
    private  = models.BooleanField(default = False)


    @property
    def new_price_sum_total(self):
        total_products = self.products.all()
        total = sum([product.new_price for product in total_products ])
        return int(total)
    @property
    def price_sum_total(self):
        total_products = self.products.all()
        total = sum([product.price for product in total_products ])
        return int(total)

    def __str__(self):
        return f'{self.user} wishlist'
