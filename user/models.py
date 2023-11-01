from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

# from django.conf import settings
from django.db.models.signals import post_save

from .customs.customUserManager.customUserManager import CustomUSerManager



class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True, blank=False, null = False, default='email@hallmarts.com')
    university = models.CharField(max_length=100, unique=False, default='university', blank=True, null = True)
    reg_no = models.CharField(_('Registration number'),max_length=25, unique=True, default='000000', blank=False, null = False)
    vendor_role = models.BooleanField(default = False)
    username = models.CharField(max_length = 150, unique = False)
    first_name = models.CharField(max_length = 50, unique = False)
    last_name = models.CharField(max_length = 50, unique = False)
    email_verified = models.BooleanField(default = False)
    on_campus =  models.BooleanField(default = False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS=  ['username','reg_no', 'university']

    objects =  CustomUSerManager()

    def __str__(self):
        return f'{self.email}'



class UserAddress(models.Model):
    user  = models.OneToOneField(User, on_delete=models.CASCADE,  related_name='user_address')
    home = models.CharField(max_length=1000, unique=False, null=True, blank=True)
    city  = models.CharField(max_length=200, unique=False, null=True, blank=True)
    state  = models.CharField(max_length=200, unique=False, null=True, blank=True)
    country = CountryField(multiple = False)
    phone = models.CharField(max_length=15, unique=False, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'User Address'

    
    def __str__(self):
        return f'Address of  {self.user.user.email}'
