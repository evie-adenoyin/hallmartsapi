# Generated by Django 3.2.9 on 2023-09-03 12:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20230815_1240'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='user_address',
        ),
        migrations.AddField(
            model_name='useraddress',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='address', to='user.userprofile'),
        ),
    ]