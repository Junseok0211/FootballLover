# Generated by Django 2.1.8 on 2020-04-01 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0043_auto_20200320_0048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('acceptSuggestion', 'acceptSuggestion'), ('joinTeam', 'joinTeam'), ('teamAccepted', 'teamAccepted'), ('leagueComment', 'leagueComment'), ('personalApply', 'personalApply'), ('teamReply', 'teamReply'), ('resultEdit', 'resultEdit'), ('personalReply', 'personalReply'), ('leagueTeamApply', 'leagueTeamApply'), ('teamApplicationDenied', 'teamApplicationDenied'), ('recruitingApply', 'recruitingApply'), ('teamMatchingApply', 'teamMatchingApply'), ('recruitingComment', 'recruitingComment'), ('recruitingAccepted', 'recruitingAccepted'), ('resultInput', 'resultInput'), ('resultConfirm', 'resultConfirm'), ('teamComment', 'teamComment'), ('prComment', 'prComment'), ('recruitingDenied', 'recruitingDenied'), ('recruitingReply', 'recruitingReply'), ('suggestTeamMatching', 'suggestTeamMatching'), ('denySuggestion', 'denySuggestion'), ('leagueReply', 'leagueReply'), ('leaguePersonalApply', 'leaguePersonalApply')], max_length=30),
        ),
    ]