# Generated by Django 2.1.8 on 2020-04-28 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0061_auto_20200427_1757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('teamApplicationDenied', 'teamApplicationDenied'), ('joinTeam', 'joinTeam'), ('personalAccept', 'personalAccept'), ('leaguePersonalApply', 'leaguePersonalApply'), ('leagueTeamApply', 'leagueTeamApply'), ('acceptSuggestion', 'acceptSuggestion'), ('personalDeny', 'personalDeny'), ('denySuggestion', 'denySuggestion'), ('resultEdit', 'resultEdit'), ('prComment', 'prComment'), ('personalApply', 'personalApply'), ('recruitingDenied', 'recruitingDenied'), ('resultInput', 'resultInput'), ('teamAccepted', 'teamAccepted'), ('resultConfirm', 'resultConfirm'), ('teamReply', 'teamReply'), ('teamMatchingApply', 'teamMatchingApply'), ('leagueComment', 'leagueComment'), ('teamComment', 'teamComment'), ('recruitingComment', 'recruitingComment'), ('recruitingApply', 'recruitingApply'), ('recruitingReply', 'recruitingReply'), ('recruitingAccepted', 'recruitingAccepted'), ('personalReply', 'personalReply'), ('leagueReply', 'leagueReply'), ('suggestTeamMatching', 'suggestTeamMatching')], max_length=30),
        ),
    ]
