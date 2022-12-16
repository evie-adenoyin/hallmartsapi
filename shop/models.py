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
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null = True, blank = True, related_name='products')
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    discount = models.IntegerField(default=0, null = True, blank = True) 
    new_price = models.IntegerField(default=0)
    discount_percentage = models.FloatField(default=0)
    stock = models.IntegerField(default=1)
    image_1 = models.ImageField(upload_to='product-image')
    image_2 = models.ImageField(upload_to='product-image', null = True, blank = True)
    image_3 = models.ImageField(upload_to='product-image', null = True, blank = True)
    category= models.ManyToManyField(to=Category, related_name='categories')
    first_category= models.ManyToManyField(to=FirstLayerCategory, related_name='firstlayercategories' )
    second_category= models.ManyToManyField(to=SecondLayerSubCategory, related_name='secondlayercategories')
    description = models.TextField(max_length=500)
    additional_info = models.TextField(max_length=500)
    shipping = models.CharField(max_length=1000)
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

    @property
    def display_price(self):
        if self.discount:
            discount_price = self.discount*100 
            percentage = discount_price/self.price
            new_price = self.price - self.discount
            self.new_price = new_price
            self.discount_percentage = round(float(percentage))
        else:
            self.new_price =  self.price
        return int(self.new_price)

    # @property
    # def ordered_products(self):
    #     ordered_product = self.orderproducts.all()
    #     print("ordered_product:", ordered_product)
    #     return ordered_product





    def save(self, *args, **kwargs):
        vendor = str(slugify(self.vendor))
        if self.slug:
            self.slug = f'{slugify(self.slug)}-{vendor}'
        self.slug = f'{slugify(self.name)}-{vendor}'
        return super(Product, self).save(*args, **kwargs)


        # image_read = storage.open(self.image_1, "r")
        # image = Image.open(image_read)
        # if image.height > 800 or image.width > 600:
            # size = 200, 200
        # if self.image_1:
        #     img = Image.open(self.image_1)
        #     if img.height > 800 or img.width > 600:
        #         output_size = img.resize((800, 600))
        #         output_size.thumbnail((800, 600), Image.LANCZOS )
        #         output_size.save(self.image_1 ,optimize=True, quality=70)
        # print( image)
        # if self.image_1:
        #     print(self.image_1.name)
        #     aws_storage = storage.open(self.image_1.name, "r")
        #     print(aws_storage)
        #     # img = Image.open(self.image_1)
        #     # if img.height > 800 or img.width > 600:
        #     #     output_size = img.resize((800, 600))
        #     #     output_size.thumbnail((800, 600), Image.LANCZOS )
        #     #     output_size.save(self.image_1.name ,optimize=True, quality=70)
        super(Product, self).save(*args, **kwargs)
         

    

    def __str__(self):
        return self.name
        



class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE , null = True, blank = True, related_name='userorder')
    date_created = models.DateTimeField(auto_now_add = True)
    date_ordered = models.DateTimeField(auto_now=True, null = True, blank = True)
    completed = models.BooleanField(default = False, null = True, blank = True)
    transaction_id = models.CharField(null = True, blank = True, max_length = 20)
    order_token = models.CharField( null = True, blank = True, max_length = 30)

    
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

    # def save(self,*args, **kwargs):
    #     self.visitor = secrets.token_hex(10)
    #     return super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return f'Order with token {self.order_token}'
    


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
        total = self.product.price * self.quantity
        return int(total)
   
    def __str__(self):
        return f"item order {self.id} in cart"
 


    

class WishList(models.Model):
    code = models.CharField( max_length=4, null = True, blank = True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE , null = True, blank = True, related_name='userwishlist')
    products = models.ManyToManyField(Product)
    private  = models.BooleanField(default = False)

    def __str__(self):
        return f'{self.user} wishlist'



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
    
    
    