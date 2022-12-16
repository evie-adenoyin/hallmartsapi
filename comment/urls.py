from django.urls import path, re_path
from .views import  CommentCreation

app_name = 'comment'

urlpatterns = [
    path('', CommentCreation.as_view(), name='creat_comment'),
]