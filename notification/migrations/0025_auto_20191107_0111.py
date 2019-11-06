# Generated by Django 2.1.8 on 2019-11-07 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0024_auto_20191104_2119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('teamApplicationDenied', 'teamApplicationDenied'), ('joinTeam', 'joinTeam'), ('teamReply', 'teamReply'), ('suggestTeamMatching', 'suggestTeamMatching'), ('recruitingComment', 'recruitingComment'), ('recruitingDenied', 'recruitingDenied'), ('recruitingAccepted', 'recruitingAccepted'), ('teamMatchingApply', 'teamMatchingApply'), ('recruitingReply', 'recruitingReply'), ('acceptSuggestion', 'acceptSuggestion'), ('prComment', 'prComment'), ('leagueComment', 'leagueComment'), ('leaguePersonalApply', 'leaguePersonalApply'), ('recruitingApply', 'recruitingApply'), ('personalReply', 'personalReply'), ('teamAccepted', 'teamAccepted'), ('leagueReply', 'leagueReply'), ('personalApply', 'personalApply'), ('teamComment', 'teamComment'), ('leagueTeamApply', 'leagueTeamApply')], max_length=30),
        ),
    ]
