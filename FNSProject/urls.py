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
    path('personal', match.views.personal, name = "personal"),
    path('personal_detail/<int:personal_id>', match.views.personal_detail, name = "personal_detail"),
    path('personal_new', match.views.personal_new, name="personal_new"),
    path('personal_create', match.views.personal_create, name = "personal_create"),
    path('personal_editForm/<int:personal_id>', match.views.personal_editForm, name = "personal_editForm"),
    path('personal_edit/<int:personal_id>', match.views.personal_edit, name = "personal_edit"),
    path('personal_delete/<int:personal_id>', match.views.personal_delete, name="personal_delete"),
    path('personal_attendance/', match.views.personal_attendance, name="personal_attendance"),
    path('personalcm_write/', match.views.personalcm_write, name = "personalcm_write"),
    path('deletePC/<int:personalComment_id>', match.views.deletePC, name='deletePC'),
    path('editPC/<int:personalComment_id>', match.views.editPC, name='editPC'),
    path('personalReply_write/', match.views.personalReply_write, name = "personalReply_write"),
    path('deletePersonalReply/<int:reply_id>', match.views.deletePersonalReply, name = "deletePersonalReply"),
    path('editPersonalReply/<int:reply_id>', match.views.editPersonalReply, name = "editPersonalReply"),

    path('teamMatching', match.views.teamMatching, name = "teamMatching"),
    path('teamMatching_new', match.views.teamMatching_new, name = "teamMatching_new"),
    path('teamMatching_detail/<int:teamMatching_id>', match.views.teamMatching_detail, name = "teamMatching_detail"),
    path('teamApplication/<int:teamMatching_id>', match.views.teamApplication, name = "teamApplication"),
    path('applied_team/<int:teamMatching_id>', match.views.applied_team, name = "applied_team"),
    path('teamCancel/<int:teamMatching_id>', match.views.teamCancel, name="teamCancel"),
    path('match_approve/<int:teamMatching_id>/<int:team_id>', match.views.match_approve, name = "match_approve"),
    path('tmcomment_write/', match.views.tmcomment_write, name = "tmcomment_write"),
    path('deleteTC/<int:teamComment_id>', match.views.deleteTC, name='deleteTC'),
    path('editTC/<int:teamComment_id>', match.views.editTC, name='editTC'),
    path('teamReply_write/', match.views.teamReply_write, name = "teamReply_write"),
    path('deleteTeamReply/<int:reply_id>', match.views.deleteTeamReply, name = "deleteTeamReply"),
    path('editTeamReply/<int:reply_id>', match.views.editTeamReply, name = "editTeamReply"),
    path('teamMatching_editForm/<int:teamMatching_id>', match.views.teamMatching_editForm, name="teamMatching_editForm"),
    path('teamMatching_delete/<int:teamMatching_id>', match.views.teamMatching_delete, name="teamMatching_delete"),
    path('teamMatching_create', match.views.teamMatching_create, name = "teamMatching_create"),
    path('teamMatching_edit/<int:team_id>', match.views.teamMatching_edit, name="teamMatching_edit"),

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

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
