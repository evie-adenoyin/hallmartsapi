# Generated by Django 3.2.9 on 2023-07-06 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0005_vendor_graduate'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='on_campus',
            field=models.BooleanField(default=False),
        ),
    ]
