# Generated by Django 2.1.8 on 2020-04-09 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_auto_20200407_1319'),
        ('match', '0006_auto_20200301_2031'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personalmatching',
            name='attendance',
        ),
        migrations.RemoveField(
            model_name='personalmatching',
            name='title',
        ),
        migrations.AddField(
            model_name='personalmatching',
            name='appliedPlayer',
            field=models.ManyToManyField(blank=True, default=None, related_name='appliedPersonal', to='account.FNSUser'),
        ),
        migrations.AddField(
            model_name='personalmatching',
            name='attendedPlayer',
            field=models.ManyToManyField(blank=True, default=None, related_name='attendedPersonal', to='account.FNSUser'),
        ),
        migrations.AddField(
            model_name='personalmatching',
            name='joinFee',
            field=models.IntegerField(blank=True, null=True, verbose_name='참가비'),
        ),
        migrations.AddField(
            model_name='personalmatching',
            name='wayToBook',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='대관방법'),
        ),
        migrations.AddField(
            model_name='personalmatching',
            name='wayToPay',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='지불방법'),
        ),
    ]