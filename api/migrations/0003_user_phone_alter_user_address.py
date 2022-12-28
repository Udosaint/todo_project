# Generated by Django 4.1.3 on 2022-12-06 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_user_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Phone Number'),
        ),
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.TextField(blank=True, null=True, verbose_name='Address'),
        ),
    ]
