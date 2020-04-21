# Generated by Django 2.1.8 on 2020-04-21 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0046_auto_20200409_0047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('teamApplicationDenied', 'teamApplicationDenied'), ('personalApply', 'personalApply'), ('joinTeam', 'joinTeam'), ('personalDeny', 'personalDeny'), ('suggestTeamMatching', 'suggestTeamMatching'), ('recruitingApply', 'recruitingApply'), ('personalAccept', 'personalAccept'), ('leaguePersonalApply', 'leaguePersonalApply'), ('resultConfirm', 'resultConfirm'), ('prComment', 'prComment'), ('leagueComment', 'leagueComment'), ('recruitingReply', 'recruitingReply'), ('acceptSuggestion', 'acceptSuggestion'), ('teamReply', 'teamReply'), ('leagueReply', 'leagueReply'), ('recruitingComment', 'recruitingComment'), ('recruitingDenied', 'recruitingDenied'), ('resultEdit', 'resultEdit'), ('resultInput', 'resultInput'), ('teamMatchingApply', 'teamMatchingApply'), ('personalReply', 'personalReply'), ('teamComment', 'teamComment'), ('leagueTeamApply', 'leagueTeamApply'), ('denySuggestion', 'denySuggestion'), ('teamAccepted', 'teamAccepted'), ('recruitingAccepted', 'recruitingAccepted')], max_length=30),
        ),
    ]
