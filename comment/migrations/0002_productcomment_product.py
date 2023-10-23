# Generated by Django 3.2.9 on 2023-10-23 02:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0001_initial'),
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcomment',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='shop.product'),
        ),
    ]
