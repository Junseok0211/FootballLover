from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.playground_list, name='playground_list'),
    path('playground/<int:id>/', views.playground, name='playground'),
    path("goReservation/<int:id>", views.goReservation, name='goReservation'),
    path("tryReservation", views.tryReservation, name='tryReservation'),
    path("resultReservation", views.resultReservation, name='resultReservation'),
    path("mobilePayment", views.mobilePayment, name='mobilePayment'),
    path("paymentPop", views.paymentPop, name='paymentPop')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)