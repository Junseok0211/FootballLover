# Generated by Django 2.1.8 on 2019-10-20 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0010_auto_20191020_0006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('comment', 'Comment'), ('applyTeam', 'ApplyTeam'), ('matchConfirm', 'MatchConfirm')], max_length=20),
        ),
    ]
