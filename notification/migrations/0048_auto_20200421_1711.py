# Generated by Django 2.1.8 on 2020-04-21 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0047_auto_20200421_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('personalDeny', 'personalDeny'), ('prComment', 'prComment'), ('recruitingReply', 'recruitingReply'), ('personalApply', 'personalApply'), ('joinTeam', 'joinTeam'), ('personalAccept', 'personalAccept'), ('personalReply', 'personalReply'), ('recruitingAccepted', 'recruitingAccepted'), ('resultEdit', 'resultEdit'), ('leagueTeamApply', 'leagueTeamApply'), ('recruitingDenied', 'recruitingDenied'), ('teamAccepted', 'teamAccepted'), ('teamComment', 'teamComment'), ('leaguePersonalApply', 'leaguePersonalApply'), ('resultInput', 'resultInput'), ('recruitingComment', 'recruitingComment'), ('teamApplicationDenied', 'teamApplicationDenied'), ('recruitingApply', 'recruitingApply'), ('leagueComment', 'leagueComment'), ('leagueReply', 'leagueReply'), ('resultConfirm', 'resultConfirm'), ('acceptSuggestion', 'acceptSuggestion'), ('teamMatchingApply', 'teamMatchingApply'), ('denySuggestion', 'denySuggestion'), ('suggestTeamMatching', 'suggestTeamMatching'), ('teamReply', 'teamReply')], max_length=30),
        ),
    ]
