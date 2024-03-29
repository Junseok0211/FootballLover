# Generated by Django 2.1.8 on 2019-11-10 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0028_auto_20191110_1659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('leagueTeamApply', 'leagueTeamApply'), ('suggestTeamMatching', 'suggestTeamMatching'), ('personalApply', 'personalApply'), ('teamMatchingApply', 'teamMatchingApply'), ('recruitingDenied', 'recruitingDenied'), ('recruitingReply', 'recruitingReply'), ('acceptSuggestion', 'acceptSuggestion'), ('joinTeam', 'joinTeam'), ('prComment', 'prComment'), ('recruitingApply', 'recruitingApply'), ('leagueReply', 'leagueReply'), ('leagueComment', 'leagueComment'), ('leaguePersonalApply', 'leaguePersonalApply'), ('personalReply', 'personalReply'), ('teamAccepted', 'teamAccepted'), ('recruitingComment', 'recruitingComment'), ('denySuggestion', 'denySuggestion'), ('recruitingAccepted', 'recruitingAccepted'), ('teamApplicationDenied', 'teamApplicationDenied'), ('teamReply', 'teamReply'), ('teamComment', 'teamComment')], max_length=30),
        ),
    ]
