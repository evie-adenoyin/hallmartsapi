from django.conf import Settings
from django.db import models
from django.conf import settings
from django.utils import timezone
from shop.models import Product


class ProductComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null= True, blank = True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null= True, blank = True, related_name='comments')
    date_created = models.DateTimeField(auto_now_add = timezone.now)
    text = models.TextField(max_length = 1500, default = 'Comment on product')
    


    def __str__(self):
        return f'Comment by {self.user}'