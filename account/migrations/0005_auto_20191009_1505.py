# Generated by Django 2.1.8 on 2019-10-09 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20191009_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fnsuser',
            name='name',
            field=models.CharField(max_length=10, verbose_name='이름'),
        ),
    ]
