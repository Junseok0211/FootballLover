from django.contrib import admin
from .models import PersonalMatching, TeamMatching, Recruiting, League, PersonalComment, PersonalReply, TMComment, REComment, LGComment, TmAppliedTeam, LgPlayerAttendance, LgTeamAttendance, TeamReply, RecruitingReply, LeagueReply
# Register your models here.
admin.site.register(PersonalMatching)
admin.site.register(PersonalComment)
admin.site.register(PersonalReply)
admin.site.register(TeamMatching)
admin.site.register(TMComment)
admin.site.register(TeamReply)
admin.site.register(Recruiting)
admin.site.register(REComment)
admin.site.register(RecruitingReply)
admin.site.register(League)
admin.site.register(LGComment)
admin.site.register(LeagueReply)
admin.site.register(TmAppliedTeam)
admin.site.register(LgPlayerAttendance)
admin.site.register(LgTeamAttendance)