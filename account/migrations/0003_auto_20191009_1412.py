# Generated by Django 2.1.8 on 2019-10-09 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_fnsuser_teamname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fnsuser',
            name='name',
            field=models.CharField(max_length=15, verbose_name='이름'),
        ),
    ]
