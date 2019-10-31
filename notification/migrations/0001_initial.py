# Generated by Django 2.1.8 on 2019-10-19 03:33

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('match', '0001_initial'),
        ('account', '0008_auto_20191018_2206'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('notification_type', models.CharField(choices=[('like', 'Like'), ('follow', 'Follow'), ('comment', 'Comment')], max_length=20)),
                ('PersonalMatching', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='match.PersonalMatching')),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='creator', to='account.FNSUser')),
                ('to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='to', to='account.FNSUser')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
