from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from customerService import views
urlpatterns = [
    path('', views.cs, name="cs"),
    path('csNew', views.csNew, name="csNew"),
    path('csEdit/<int:cs_id>', views.csEdit, name="csEdit"),
    path('csEditform/<int:cs_id>', views.csEditform, name="csEditform"),
    path('csDetail/<int:cs_id>', views.csDetail, name="csDetail"),
    path('csDelete/<int:cs_id>', views.csDelete, name="csDelete"),

]