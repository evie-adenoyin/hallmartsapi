from django_filters import rest_framework as filters
from .models import Product, WishList, Category, FirstLayerCategory,SecondLayerSubCategory, Color,Size

from vendor.models import Vendor
class ProductFilter(filters.FilterSet):
    category = filters.ModelChoiceFilter(queryset=Category.objects.all())
    first_category = filters.ModelChoiceFilter(queryset=FirstLayerCategory.objects.all())
    second_category = filters.ModelChoiceFilter(queryset=SecondLayerSubCategory.objects.all())
    product_size = filters.ModelChoiceFilter(queryset=Size.objects.all())
    product_color = filters.ModelMultipleChoiceFilter(queryset=Color.objects.all())
    name = filters.CharFilter(field_name ='name')
    # university = filters.ModelChoiceFilter(queryset=Vendor.objects.all())

    # def filter_by_vendor_university(self, queryset, name, value):
    #     return queryset.filter(vendor__university__icontains=value)

    class Meta:
        model = Product
        fields =  {
            'name': ['contains'], 
            'grade': ['contains'], 
            'vendor': ['exact',], 
            'vendor__university': ['contains',], 
            'vendor__brand': ['contains',], 
            'discount_percentage': ['contains',], 
            'price': ['contains',],
            'category': ['exact',],
            'first_category': ['exact',],
            'second_category': ['exact',],
            'description': ['contains',],
            'additional_info': ['contains',],
            'tag': ['contains',],
            'product_size': ['exact',],
            'product_color': ['exact',],
            }

 