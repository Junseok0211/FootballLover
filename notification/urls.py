from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import match.views
import team.views
import notification.views 

urlpatterns = [
    path('notification', notification.views.notification, name='notification'),
    path('checkAllNotification', notification.views.checkAllNotification, name='checkAllNotification'),
    path('checkNotification/<int:notification_id>', notification.views.checkNotification, name='checkNotification'),
    

]