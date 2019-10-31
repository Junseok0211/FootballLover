from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import result.views
import match.views
import team.views
import rank.views

urlpatterns = [
    path('', rank.views.individualRank, name = "individualRank"),
    path('individualGa', rank.views.individualGa, name="individualGa"),
    path('teamRank', rank.views.teamRank, name = "teamRank"),

]