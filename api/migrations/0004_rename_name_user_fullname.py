# Generated by Django 4.1.3 on 2022-12-06 16:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_user_phone_alter_user_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='name',
            new_name='fullname',
        ),
    ]