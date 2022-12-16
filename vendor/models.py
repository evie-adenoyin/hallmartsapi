from email.policy import default
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from user.models import User
from django.db.models.signals import post_save


class Vendor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null = True, blank = True)
    vendor = models.CharField(max_length=50,null = True, blank = True)
    email = models.EmailField(unique = True)
    university = models.CharField(max_length=50, null = True, blank = True)
    graduate = models.BooleanField(default = False)
    category = models.CharField(max_length=60, default = "Fashion")
    brand = models.CharField(max_length=50, unique = True)
    reg_no = models.CharField(max_length=50, null = True, blank = True)
    brand_statement = models.CharField(max_length=1500, null = True, blank = True)
    date_created = models.DateTimeField(auto_now_add = timezone.now)
    slug = models.SlugField(max_length=255, unique = True)


    @property
    def total_stock(self):
        products = self.products.all()
        stock = sum([stock.stock for stock in products])
        return int(stock)

    @property
    def expected_revenue(self):
        products = self.products.all()
        revenue = sum([revenue.display_price*revenue.stock for revenue in products])
        return int(revenue)

    @property     
    def current_sale(self):
        products = self.products.all()
        sales = sum([sales.display_price for sales in products if sales.ordered])
        return int(sales)


    def __str__(self):
        return f'{self.brand}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.brand)
            super(Vendor,self).save(*args, **kwargs)

