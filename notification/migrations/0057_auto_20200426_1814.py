# Generated by Django 2.1.8 on 2020-04-26 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0056_auto_20200425_2306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('leagueComment', 'leagueComment'), ('personalAccept', 'personalAccept'), ('personalDeny', 'personalDeny'), ('teamMatchingApply', 'teamMatchingApply'), ('leaguePersonalApply', 'leaguePersonalApply'), ('recruitingReply', 'recruitingReply'), ('resultInput', 'resultInput'), ('recruitingApply', 'recruitingApply'), ('leagueTeamApply', 'leagueTeamApply'), ('recruitingComment', 'recruitingComment'), ('joinTeam', 'joinTeam'), ('denySuggestion', 'denySuggestion'), ('personalReply', 'personalReply'), ('personalApply', 'personalApply'), ('suggestTeamMatching', 'suggestTeamMatching'), ('acceptSuggestion', 'acceptSuggestion'), ('teamAccepted', 'teamAccepted'), ('recruitingAccepted', 'recruitingAccepted'), ('prComment', 'prComment'), ('teamApplicationDenied', 'teamApplicationDenied'), ('resultEdit', 'resultEdit'), ('resultConfirm', 'resultConfirm'), ('teamReply', 'teamReply'), ('recruitingDenied', 'recruitingDenied'), ('leagueReply', 'leagueReply'), ('teamComment', 'teamComment')], max_length=30),
        ),
    ]
