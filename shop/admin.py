from django.contrib import admin

from .models import Category, Product, Order, OrderProduct, WishList, ShippingAddress,FirstLayerCategory , SecondLayerSubCategory,Size ,Color



class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name","description")}

admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(Category)
admin.site.register(WishList)
admin.site.register(ShippingAddress)
admin.site.register(FirstLayerCategory)
admin.site.register(SecondLayerSubCategory)
admin.site.register(Size)
admin.site.register(Color)