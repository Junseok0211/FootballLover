from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.team, name = "team"),
    path('detail/<int:team_id>', views.detail, name = 'detail'),
    path('new/', views.new, name = "new"),
    path('create/', views.create, name = "create"),
    path('application/<int:team_id>', views.application, name = "application"),
    path('applied_list/<int:team_id>', views.applied_list, name = "applied_list"),
    path('approve/<int:team_id>/<int:fnsuser_id>', views.approve, name = 'approve'),
    path('dropout/<int:team_id>', views.dropout, name="dropout"),
    path('editForm/<int:team_id>', views.editForm, name="editForm"),
    path('update/<int:team_id>', views.update, name = "update"),
    path('delete/', views.delete, name = "delete"),
    path('searchTeam/', views.searchTeam, name = "searchTeam"),
    path('changeCaptain/<int:team_id>', views.changeCaptain, name = "changeCaptain"),
    path('cancelApplication/<int:team_id>', views.cancelApplication, name="cancelApplication"),
    path('teamApplicationDenied/<int:team_id>/<int:player_id>', views.teamApplicationDenied, name="teamApplicationDenied"),
    path('suggestTeamMatching/<int:team_id>/', views.suggestTeamMatching, name="suggestTeamMatching"),
    path('suggestList/<int:team_id>/', views.suggestList, name="suggestList"),
    path('suggestDetail/<int:teamMatching_id>/', views.suggestDetail, name="suggestDetail"),
    path('denySuggest/<int:teamMatching_id>/', views.denySuggest, name="denySuggest"),
    path('acceptSuggest/<int:teamMatching_id>/', views.acceptSuggest, name="acceptSuggest"),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
