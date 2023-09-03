from enum import unique
from pyexpat import model
from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

# from django.conf import settings
from django.db.models.signals import post_save



class CustomUSerManager(BaseUserManager):
    """

    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.

    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.

        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email = email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.

        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True, blank=False, null = False, default='email@hallmarts.com')
    university = models.CharField(max_length=100, unique=False, default='university', blank=True, null = True)
    reg_no = models.CharField(_('Registration number'),max_length=25, unique=True, default='000000', blank=False, null = False)
    vendor_role = models.BooleanField(default = False)
    username = models.CharField(max_length = 150, unique = False)
    first_name = models.CharField(max_length = 50, unique = False)
    last_name = models.CharField(max_length = 50, unique = False)
    
    

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS=  ['username','reg_no', 'university']

    objects =  CustomUSerManager()

    def __str__(self):
        return f'{self.username}'


class UserProfile(models.Model):
    user  = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    bio = models.CharField(max_length=2000, unique=False, blank=True, null = True)

    def __str__(self):
        return f"{self.user.email}'s profile"

def post_save_receiver(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user = instance)
  

post_save.connect(post_save_receiver, sender=User)



class UserAddress(models.Model):
    user  = models.OneToOneField(UserProfile, on_delete=models.CASCADE,  related_name='address')
    home = models.CharField(max_length=1000, unique=False, null=True, blank=True)
    city  = models.CharField(max_length=200, unique=False, null=True, blank=True)
    state  = models.CharField(max_length=200, unique=False, null=True, blank=True)
    country = CountryField(multiple = False)
    phone = models.CharField(max_length=15, unique=False, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'User Address'

    
    def __str__(self):
        return f'Address of  {self.user.user.email}'
