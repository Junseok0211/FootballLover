from django.db import models
from team.models import Team
from match.models import TeamMatching
from account.models import FNSUser
from decidedMatch.models import DecidedMatch
# Create your models here.

class Result(models.Model):
    match = models.OneToOneField(DecidedMatch, on_delete=models.CASCADE, null=True, blank=True)
    myTeam = models.ForeignKey(Team, related_name="myResultTeam", on_delete=models.CASCADE, null=True)
    vsTeam = models.ForeignKey(Team, related_name="vsResultTeam", on_delete=models.CASCADE, null=True)
    myTeamScore = models.IntegerField(default=0)
    vsTeamScore = models.IntegerField(default=0)
    timeFrom = models.DateTimeField(verbose_name='시작시간', null=True)
    myCheck = models.BooleanField(default=True)
    vsCheck = models.BooleanField(default=True)
    confirm = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')
    updated = models.DateTimeField(auto_now=True, verbose_name='수정시간')

class AttendedPlayer(models.Model):
    player = models.ForeignKey(FNSUser, on_delete=models.CASCADE, null=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    match = models.ForeignKey(TeamMatching, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')
    updated = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    
    def __str__(self):
        return self.player.name

class ScoredPlayer(models.Model):
    player = models.ForeignKey(FNSUser, on_delete=models.CASCADE, null = True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    match = models.ForeignKey(TeamMatching, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')
    updated = models.DateTimeField(auto_now=True, verbose_name='수정시간')

    def __str__(self):
        if self.player is None:
            return '자책골'
        else:
            return self.player.name