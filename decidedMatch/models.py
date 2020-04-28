from django.db import models
from team.models import Team
from match.models import TeamMatching
from account.models import FNSUser
from reservation.models import PlaygroundList
# Create your models here.

class DecidedMatch(models.Model):
    myTeam = models.ForeignKey(Team, related_name="myDecidedTeam", on_delete=models.CASCADE, null=True)
    vsTeam = models.ForeignKey(Team, related_name="vsDecidedTeam", on_delete=models.CASCADE, null=True)
    match = models.OneToOneField(TeamMatching, related_name="decidedMatch", on_delete=models.CASCADE, null = True)
    timeFrom = models.DateTimeField()
    timeTo = models.DateTimeField()
    location = models.ForeignKey(PlaygroundList, related_name="확정경기", on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')
    updated = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    my_suggest = models.BooleanField(default=False)
    vs_suggest = models.BooleanField(default=False)
    my_confirm = models.BooleanField(default=False)
    vs_confirm = models.BooleanField(default=False)



    def __str__(self):
        return self.myTeam.name + ' VS ' + self.vsTeam.name