# Generated by Django 2.1.8 on 2020-03-09 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0038_auto_20200309_1919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('suggestTeamMatching', 'suggestTeamMatching'), ('teamApplicationDenied', 'teamApplicationDenied'), ('recruitingAccepted', 'recruitingAccepted'), ('personalReply', 'personalReply'), ('recruitingReply', 'recruitingReply'), ('resultEdit', 'resultEdit'), ('resultConfirm', 'resultConfirm'), ('joinTeam', 'joinTeam'), ('resultInput', 'resultInput'), ('leagueTeamApply', 'leagueTeamApply'), ('acceptSuggestion', 'acceptSuggestion'), ('denySuggestion', 'denySuggestion'), ('teamAccepted', 'teamAccepted'), ('recruitingComment', 'recruitingComment'), ('recruitingApply', 'recruitingApply'), ('personalApply', 'personalApply'), ('leagueComment', 'leagueComment'), ('teamMatchingApply', 'teamMatchingApply'), ('recruitingDenied', 'recruitingDenied'), ('prComment', 'prComment'), ('teamComment', 'teamComment'), ('teamReply', 'teamReply'), ('leagueReply', 'leagueReply'), ('leaguePersonalApply', 'leaguePersonalApply')], max_length=30),
        ),
    ]