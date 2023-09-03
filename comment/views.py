from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status, filters
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from user.models import User
from shop.models import Product
from .models import ProductComment
from .serializers import CommentSerializer



class CreateComment(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        
        product_id = request.data.get('product')  
        text = request.data.get('text')
        try:
            user = User.objects.get(id=request.user.id)
        except ObjectDoesNotExist:
            return Response({'message':"Sign in to comment on product"}, status=status.HTTP_403_FORBIDDEN)
        product = Product.objects.get(id=product_id)
        comment = ProductComment.objects.create(user = user, text=text, product=product)
        serializer = CommentSerializer(comment, data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({'message':f"Comment on {product.name} was successful."}, status=status.HTTP_201_CREATED)
        return Response(serializer.error)
