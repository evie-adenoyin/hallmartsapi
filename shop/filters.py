from django_filters import rest_framework as filters
from .models import Product, WishList, Category, FirstLayerCategory,SecondLayerSubCategory, Color,Size


class ProductFilter(filters.FilterSet):
    category = filters.ModelChoiceFilter(queryset=Category.objects.all())
    first_category = filters.ModelChoiceFilter(queryset=FirstLayerCategory.objects.all())
    second_category = filters.ModelChoiceFilter(queryset=SecondLayerSubCategory.objects.all())
    product_size = filters.ModelChoiceFilter(queryset=Size.objects.all())
    product_color = filters.ModelMultipleChoiceFilter(queryset=Color.objects.all())
    name = filters.CharFilter(field_name ='name')

    class Meta:
        model = Product
        fields =  {
            'name': ['contains'], 
            # 'vendor': ['contains',], 
            # 'university': ['exact',], 
            # 'brand': ['contains',], 
            'price': ['contains',],
            'category': ['exact',],
            'first_category': ['exact',],
            'second_category': ['exact',],
            'description': ['contains',],
            'additional_info': ['contains',],
            'tag': ['exact',],
            'product_size': ['exact',],
            'product_color': ['exact',],
            }

 