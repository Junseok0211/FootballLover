from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import result.views
import match.views
import team.views
import decidedMatch.views

urlpatterns = [
    path('', decidedMatch.views.decidedMatch, name="decidedMatch"),
    path('decidedDetail/<int:decidedMatch_id>', decidedMatch.views.decidedDetail, name="decidedDetail"),

]