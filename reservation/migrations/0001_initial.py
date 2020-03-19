# Generated by Django 2.1.8 on 2020-03-04 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PlaygroundList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('playgroundName', models.CharField(max_length=100)),
                ('playgroundLoation', models.CharField(max_length=200)),
                ('playgorundPhoto', models.FileField(upload_to='uploads/')),
                ('playgroundOption1', models.BooleanField()),
                ('playgroundOption2', models.BooleanField()),
                ('playgroundOption3', models.BooleanField()),
                ('playgroundOption4', models.BooleanField()),
                ('playgroundOption5', models.BooleanField()),
                ('playgroundOption6', models.BooleanField()),
                ('playgroundInfo', models.TextField()),
                ('possibleReservation', models.BooleanField()),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
    ]