# Generated by Django 2.1.8 on 2020-04-25 22:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0010_auto_20200424_0244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personalmatching',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='personalMatching', to='reservation.PlaygroundList'),
        ),
    ]