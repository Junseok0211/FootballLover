# Generated by Django 2.1.8 on 2020-04-28 23:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('decidedMatch', '0002_auto_20191111_2229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='decidedmatch',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='확정경기', to='reservation.PlaygroundList'),
        ),
    ]
