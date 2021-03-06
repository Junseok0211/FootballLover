# Generated by Django 2.1.8 on 2019-11-11 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0030_auto_20191111_2223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('leagueReply', 'leagueReply'), ('personalReply', 'personalReply'), ('teamAccepted', 'teamAccepted'), ('resultEdit', 'resultEdit'), ('suggestTeamMatching', 'suggestTeamMatching'), ('teamReply', 'teamReply'), ('recruitingComment', 'recruitingComment'), ('denySuggestion', 'denySuggestion'), ('leagueTeamApply', 'leagueTeamApply'), ('recruitingDenied', 'recruitingDenied'), ('personalApply', 'personalApply'), ('recruitingAccepted', 'recruitingAccepted'), ('leagueComment', 'leagueComment'), ('joinTeam', 'joinTeam'), ('teamMatchingApply', 'teamMatchingApply'), ('recruitingApply', 'recruitingApply'), ('prComment', 'prComment'), ('resultInput', 'resultInput'), ('teamComment', 'teamComment'), ('leaguePersonalApply', 'leaguePersonalApply'), ('teamApplicationDenied', 'teamApplicationDenied'), ('recruitingReply', 'recruitingReply'), ('acceptSuggestion', 'acceptSuggestion'), ('resultConfirm', 'resultConfirm')], max_length=30),
        ),
    ]
