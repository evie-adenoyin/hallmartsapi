from django.shortcuts import render

from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    UpdateAPIView,
    GenericAPIView,
    CreateAPIView,
    ListCreateAPIView,
) 

from .models import ProductComment
from .serializers import CommentSerializer



class CommentCreation(CreateAPIView):
    queryset = ProductComment.objects.all()
    serializer_class = CommentSerializer



