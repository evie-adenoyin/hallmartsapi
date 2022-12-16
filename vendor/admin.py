from django.contrib import admin
from .models import Vendor
# Register your models here.


class VendorAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("brand",)}
admin.site.register(Vendor, VendorAdmin)