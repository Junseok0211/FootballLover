# Generated by Django 2.1.8 on 2020-04-07 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0044_auto_20200401_1743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('resultConfirm', 'resultConfirm'), ('prComment', 'prComment'), ('acceptSuggestion', 'acceptSuggestion'), ('joinTeam', 'joinTeam'), ('teamApplicationDenied', 'teamApplicationDenied'), ('recruitingReply', 'recruitingReply'), ('resultInput', 'resultInput'), ('leagueTeamApply', 'leagueTeamApply'), ('denySuggestion', 'denySuggestion'), ('recruitingComment', 'recruitingComment'), ('leagueComment', 'leagueComment'), ('leagueReply', 'leagueReply'), ('recruitingAccepted', 'recruitingAccepted'), ('teamAccepted', 'teamAccepted'), ('teamComment', 'teamComment'), ('teamMatchingApply', 'teamMatchingApply'), ('recruitingApply', 'recruitingApply'), ('personalApply', 'personalApply'), ('recruitingDenied', 'recruitingDenied'), ('leaguePersonalApply', 'leaguePersonalApply'), ('personalReply', 'personalReply'), ('resultEdit', 'resultEdit'), ('teamReply', 'teamReply'), ('suggestTeamMatching', 'suggestTeamMatching')], max_length=30),
        ),
    ]