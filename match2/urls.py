from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('match1', views.match1, name='match1'),
    path('match2', views.match2, name='match2'),
    path('match3', views.match3, name='match3'),
    path('match4', views.match4, name='match4'),
    path('match5', views.match5, name='match5')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)