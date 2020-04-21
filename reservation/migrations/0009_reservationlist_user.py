# Generated by Django 2.1.8 on 2020-04-21 16:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_auto_20200407_1319'),
        ('reservation', '0008_auto_20200308_2108'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservationlist',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.FNSUser'),
        ),
    ]
