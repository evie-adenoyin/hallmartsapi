# Generated by Django 3.2.9 on 2022-10-19 22:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_product_yo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='yo',
            new_name='discount',
        ),
    ]
