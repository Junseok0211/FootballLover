# Generated by Django 2.1.8 on 2020-04-22 00:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0011_auto_20200421_1728'),
    ]

    operations = [
        migrations.RenameField(
            model_name='playgroundlist',
            old_name='playgorundPhoto',
            new_name='playgroundPhoto',
        ),
    ]
