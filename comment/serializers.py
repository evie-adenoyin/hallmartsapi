from rest_framework.serializers import (
    ModelSerializer, 
    StringRelatedField, 
    HyperlinkedIdentityField,
    CharField
)


from .models import ProductComment
# from shop.serializers import ProductSerializers



class CommentSerializer(ModelSerializer):
    user = StringRelatedField()
    class Meta:
        model = ProductComment
        fields = '__all__'


