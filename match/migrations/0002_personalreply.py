# Generated by Django 2.1.8 on 2019-10-21 03:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20191018_2206'),
        ('match', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalReply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=500)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reply', to='match.PersonalComment')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postReply', to='match.PersonalMatching')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.FNSUser')),
            ],
        ),
    ]
