# Generated by Django 2.1.8 on 2020-04-27 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0059_auto_20200426_2000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('recruitingDenied', 'recruitingDenied'), ('teamApplicationDenied', 'teamApplicationDenied'), ('leagueComment', 'leagueComment'), ('personalApply', 'personalApply'), ('recruitingAccepted', 'recruitingAccepted'), ('leagueReply', 'leagueReply'), ('resultEdit', 'resultEdit'), ('teamAccepted', 'teamAccepted'), ('personalReply', 'personalReply'), ('joinTeam', 'joinTeam'), ('suggestTeamMatching', 'suggestTeamMatching'), ('resultConfirm', 'resultConfirm'), ('prComment', 'prComment'), ('teamComment', 'teamComment'), ('acceptSuggestion', 'acceptSuggestion'), ('denySuggestion', 'denySuggestion'), ('resultInput', 'resultInput'), ('recruitingComment', 'recruitingComment'), ('personalDeny', 'personalDeny'), ('personalAccept', 'personalAccept'), ('teamMatchingApply', 'teamMatchingApply'), ('teamReply', 'teamReply'), ('leaguePersonalApply', 'leaguePersonalApply'), ('recruitingReply', 'recruitingReply'), ('leagueTeamApply', 'leagueTeamApply'), ('recruitingApply', 'recruitingApply')], max_length=30),
        ),
    ]