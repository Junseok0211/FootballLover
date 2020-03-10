from django.contrib import admin
from .models import PlaygroundList, ReservationList

# Register your models here.
admin.site.register(PlaygroundList)
admin.site.register(ReservationList)