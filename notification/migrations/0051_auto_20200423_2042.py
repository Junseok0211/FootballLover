# Generated by Django 2.1.8 on 2020-04-23 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0050_auto_20200422_0021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('personalReply', 'personalReply'), ('personalDeny', 'personalDeny'), ('denySuggestion', 'denySuggestion'), ('resultInput', 'resultInput'), ('recruitingReply', 'recruitingReply'), ('joinTeam', 'joinTeam'), ('teamAccepted', 'teamAccepted'), ('leagueReply', 'leagueReply'), ('leaguePersonalApply', 'leaguePersonalApply'), ('recruitingAccepted', 'recruitingAccepted'), ('teamApplicationDenied', 'teamApplicationDenied'), ('leagueTeamApply', 'leagueTeamApply'), ('recruitingComment', 'recruitingComment'), ('resultConfirm', 'resultConfirm'), ('suggestTeamMatching', 'suggestTeamMatching'), ('prComment', 'prComment'), ('teamComment', 'teamComment'), ('teamReply', 'teamReply'), ('leagueComment', 'leagueComment'), ('personalAccept', 'personalAccept'), ('personalApply', 'personalApply'), ('recruitingDenied', 'recruitingDenied'), ('resultEdit', 'resultEdit'), ('teamMatchingApply', 'teamMatchingApply'), ('acceptSuggestion', 'acceptSuggestion'), ('recruitingApply', 'recruitingApply')], max_length=30),
        ),
    ]