from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import result.views
import match.views
import team.views


urlpatterns = [
    path('', result.views.result, name="result"),
    path('input/<int:decidedMatch_id>', result.views.input, name="input"),
    path('inputScorer', result.views.inputScorer, name="inputScorer"),
    path('myTeamResult', result.views.myTeamResult, name="myTeamResult"),
    path('edit<int:decidedMatch_id>', result.views.edit, name = "edit"),
    path('editScorer', result.views.editScorer, name = "editScorer"),
    path('editTeamResult', result.views.editTeamResult, name="editTeamResult"),
    path('myConfirm<int:decidedMatch_id>', result.views.myConfirm, name = "myConfirm"),
    path('vsConfirm<int:decidedMatch_id>', result.views.vsConfirm, name = "vsConfirm"),

]