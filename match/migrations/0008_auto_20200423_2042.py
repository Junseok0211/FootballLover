# Generated by Django 2.1.8 on 2020-04-23 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0007_auto_20200409_0047'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personalmatching',
            name='wayToBook',
        ),
        migrations.RemoveField(
            model_name='personalmatching',
            name='wayToPay',
        ),
        migrations.AddField(
            model_name='personalmatching',
            name='city',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='지역 시/군/구'),
        ),
        migrations.AddField(
            model_name='personalmatching',
            name='region',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='지역 시/도'),
        ),
    ]