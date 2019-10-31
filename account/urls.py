from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views import generic
import match.views
import team.views
from . import views

urlpatterns = [
    path('test', views.test, name="test"),
    path('test2', views.test2, name="test2"),
    path('test3', views.test3, name="test3"),
    path('test1', views.FNSAuth.as_view(), name = "verification"),
    path('register', views.register, name = "register"),
    path('login', views.login, name = "login"),
    path('logout', views.logout, name = "logout"),
    path('myPage/<int:fnsuser_id>', views.myPage, name="myPage"),
    path('checkId', views.checkId, name = "checkId"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
