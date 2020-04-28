"""FNSproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import match.views
import team.views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', match.views.home, name = "home"),
    path('about', match.views.about, name = "about"),
    path('play', match.views.play, name = "play"),
    path('personal', match.views.personal, name = "personal"),
    path('personalDay', match.views.personalDay, name = "personalDay"),
    path('personalDetail/<int:personal_id>', match.views.personalDetail, name = "personalDetail"),
    path('personalNew', match.views.personalNew, name="personalNew"),
    path('personalCreate', match.views.personalCreate, name = "personalCreate"),
    path('personalResult/<int:personalId>', match.views.personalResult, name = "personalResult"),
    path('personalEdit/<int:personalId>', match.views.personalEdit, name = "personalEdit"),
    path('personalDelete/<int:personal_id>', match.views.personalDelete, name="personalDelete"),
    path('personal_attendance/', match.views.personal_attendance, name="personal_attendance"),
    path('personalApply/<int:personalId>', match.views.personalApply, name="personalApply"),
    path('appliedPlayer/<int:personalId>', match.views.appliedPlayer, name="appliedPlayer"),
    path('personalAccept/<int:userId>/<int:personalId>', match.views.personalAccept, name="personalAccept"),
    path('personalAcceptAll/<int:personalId>', match.views.personalAcceptAll, name="personalAcceptAll"),
    path('personalDeny/<int:userId>/<int:personalId>', match.views.personalDeny, name="personalDeny"),
    path('personalAttendanceCancel/<int:personalId>', match.views.personalAttendanceCancel, name="personalAttendanceCancel"),

    path('pCheckReservation', match.views.pCheckReservation, name = "pCheckReservation"),
    path('pIsReserved', match.views.pIsReserved, name = "pIsReserved"),
    path('selectCity', match.views.selectCity, name = "selectCity"),

    path('personalComment/<int:personalId>', match.views.personalComment, name="personalComment"),
    path('personalcm_write/', match.views.personalcm_write, name = "personalcm_write"),
    path('deletePC/<int:personalComment_id>', match.views.deletePC, name='deletePC'),
    path('editPC/<int:personalComment_id>', match.views.editPC, name='editPC'),
    path('personalReply_write/', match.views.personalReply_write, name = "personalReply_write"),
    path('deletePersonalReply/<int:reply_id>', match.views.deletePersonalReply, name = "deletePersonalReply"),
    path('editPersonalReply/<int:reply_id>', match.views.editPersonalReply, name = "editPersonalReply"),

    path('teamMatching', match.views.teamMatching, name = "teamMatching"),
    path('teamDay', match.views.teamDay, name = "teamDay"),
    path('teamMatchingNew', match.views.teamMatchingNew, name = "teamMatchingNew"),
    path('tCheckReservation', match.views.tCheckReservation, name = "tCheckReservation"),
    path('tIsReserved', match.views.tIsReserved, name = "tIsReserved"),
    path('tPartnerNew', match.views.tPartnerNew, name = "tPartnerNew"),
    path('tPartnerCreate', match.views.tPartnerCreate, name = "tPartnerCreate"),
    path('tNonPartnerNew', match.views.tNonPartnerNew, name = "tNonPartnerNew"),
    path('tNonPartnerCreate', match.views.tNonPartnerCreate, name = "tNonPartnerCreate"),
    path('tChoice', match.views.tChoice, name = "tChoice"),
    path('tMatchingFirst', match.views.tMatchingFirst, name = "tMatchingFirst"),
    path('tSelectTime', match.views.tSelectTime, name = "tSelectTime"),
    path('tMatchingCreate', match.views.tMatchingCreate, name = "tMatchingCreate"),
    path('tBookingFirst', match.views.tBookingFirst, name = "tBookingFirst"),
    path('tBookingTime', match.views.tBookingTime, name = "tBookingTime"),
    path('tTryReservation', match.views.tTryReservation, name = "tTryReservation"),
    path('tResultReservation', match.views.tResultReservation, name = "tResultReservation"),
    path('teamMatchingDetail/<int:teamMatchingId>', match.views.teamMatchingDetail, name = "teamMatchingDetail"),
    path('teamApplication/<int:teamMatchingId>', match.views.teamApplication, name = "teamApplication"),
    path('appliedTeam/<int:teamMatchingId>', match.views.appliedTeam, name = "appliedTeam"),
    path('teamCancel/<int:teamMatchingId>', match.views.teamCancel, name="teamCancel"),
    path('matchApprove/<int:teamMatchingId>/<int:teamId>', match.views.matchApprove, name = "matchApprove"),
    path('matchDeny/<int:teamMatchingId>/<int:teamId>', match.views.matchDeny, name = "matchDeny"),
    path('teamMatchingComment/<int:teamMatchingId>', match.views.teamMatchingComment, name = "teamMatchingComment"),
    path('tmcomment_write/', match.views.tmcomment_write, name = "tmcomment_write"),
    path('deleteTC/<int:teamComment_id>', match.views.deleteTC, name='deleteTC'),
    path('editTC/<int:teamComment_id>', match.views.editTC, name='editTC'),
    path('teamReply_write/', match.views.teamReply_write, name = "teamReply_write"),
    path('deleteTeamReply/<int:reply_id>', match.views.deleteTeamReply, name = "deleteTeamReply"),
    path('editTeamReply/<int:reply_id>', match.views.editTeamReply, name = "editTeamReply"),
    path('teamMatchingEditForm/<int:teamMatchingId>', match.views.teamMatchingEditForm, name="teamMatchingEditForm"),
    path('tEditTime', match.views.tEditTime, name = "tEditTime"),
    path('tMatchingEdit', match.views.tMatchingEdit, name = "tMatchingEdit"),
    path('teamMatchingDelete/<int:teamMatchingId>', match.views.teamMatchingDelete, name="teamMatchingDelete"),
    path('teamMatching_create', match.views.teamMatching_create, name = "teamMatching_create"),
    path('teamMatchingEdit/<int:teamMatchingId>', match.views.teamMatchingEdit, name="teamMatchingEdit"),

    path('recruiting', match.views.recruiting, name = "recruiting"),
    path('recruiting_new', match.views.recruiting_new, name = "recruiting_new"),
    path('recruiting_create', match.views.recruiting_create, name = "recruiting_create"),
    path('recruiting_detail/<int:recruiting_id>', match.views.recruiting_detail, name = "recruiting_detail"),
    path('recruiting_apply/<int:recruiting_id>', match.views.recruiting_apply, name="recruiting_apply"),
    path('recruiting_list/<int:recruiting_id>', match.views.recruiting_list, name="recruiting_list"),
    path('recruiting_accept/<int:recruiting_id>/<int:player_id>', match.views.recruiting_accept, name = "recruiting_accept"),
    path('recruiting_deny/<int:recruiting_id>/<int:player_id>', match.views.recruiting_deny, name = "recruiting_deny"),
    path('recruiting_cancel/<int:recruiting_id>', match.views.recruiting_cancel, name = "recruiting_cancel"),
    path('recruiting_editForm/<int:recruiting_id>', match.views.recruiting_editForm, name = "recruiting_editForm"),
    path('recruiting_edit/<int:recruiting_id>', match.views.recruiting_edit, name = "recruiting_edit"),
    path('recruiting_delete/<int:recruiting_id>', match.views.recruiting_delete, name = "recruiting_delete"),
    path('recomment_write', match.views.recomment_write, name="recomment_write"),
    path('deleteRC/<int:recruitingComment_id>', match.views.deleteRC, name='deleteRC'),
    path('editRC/<int:recruitingComment_id>', match.views.editRC, name='editRC'),
    path('recruitingReply_write/', match.views.recruitingReply_write, name = "recruitingReply_write"),
    path('deleteRecruitingReply/<int:reply_id>', match.views.deleteRecruitingReply, name = "deleteRecruitingReply"),
    path('editRecruitingReply/<int:reply_id>', match.views.editRecruitingReply, name = "editRecruitingReply"),

    path('league', match.views.league, name="league"),
    path('league_new', match.views.league_new, name="league_new"),
    path('league_create', match.views.league_create, name="league_create"),
    path('league_editForm/<int:league_id>', match.views.league_editForm, name="league_editForm"),
    path('league_edit/<int:league_id>', match.views.league_edit, name="league_edit"),
    path('league_detail/<int:league_id>', match.views.league_detail, name = "league_detail"),
    path('league_delete/<int:league_id>', match.views.league_delete, name = "league_delete"),
    path('personal_apply/<int:league_id>', match.views.personal_apply, name = "personal_apply"),
    path('personal_cancel/<int:league_id>', match.views.personal_cancel, name = "personal_cancel"),
    path('team_apply/<int:league_id>', match.views.team_apply, name="team_apply"),
    path('team_cancel/<int:league_id>', match.views.team_cancel, name = "team_cancel"),
    path('lgcomment_write', match.views.lgcomment_write, name="lgcomment_write"),
    path('deleteLC/<int:leagueComment_id>', match.views.deleteLC, name='deleteLC'),
    path('editLC/<int:leagueComment_id>', match.views.editLC, name='editLC'),
    path('leagueReply_write/', match.views.leagueReply_write, name = "leagueReply_write"),
    path('deleteLeagueReply/<int:reply_id>', match.views.deleteLeagueReply, name = "deleteLeagueReply"),
    path('editLeagueReply/<int:reply_id>', match.views.editLeagueReply, name = "editLeagueReply"),

    path('team/', include('team.urls')),
    path('result/', include('result.urls')),
    path('account/', include('account.urls')),
    path('decidedMatch/', include('decidedMatch.urls')),
    path('rank/', include('rank.urls')),
    path('notification/', include('notification.urls')),
    path('customerService/', include('customerService.urls')),
    path('reservation/', include('reservation.urls')),
    path('match2/', include('match2.urls')),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
