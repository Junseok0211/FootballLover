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
    path('update/', views.update, name = "update"),
    path('delete/', views.delete, name = "delete"),
    path('searchTeam/', views.searchTeam, name = "searchTeam"),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
