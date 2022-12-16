from atexit import register
from django.contrib import admin

# Register your models here.
from .models import ProductComment


admin.site.register(ProductComment)