from django.urls import path, re_path
from .views import  CreateComment

app_name = 'comment'

urlpatterns = [
    path('create', CreateComment.as_view(), name='creat_comment'),
]
