# Generated by Django 3.2.9 on 2023-10-23 02:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('university', models.CharField(blank=True, max_length=50, null=True)),
                ('graduate', models.BooleanField(default=False)),
                ('category', models.CharField(default='Fashion', max_length=60)),
                ('brand', models.CharField(max_length=50, unique=True)),
                ('reg_no', models.CharField(blank=True, max_length=50, null=True)),
                ('brand_statement', models.CharField(blank=True, max_length=1500, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('on_campus', models.BooleanField(default=False)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
