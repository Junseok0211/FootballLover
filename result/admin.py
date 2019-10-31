from django.contrib import admin
from result.models import Result, AttendedPlayer, ScoredPlayer
# Register your models here.
admin.site.register(Result)
admin.site.register(AttendedPlayer)
admin.site.register(ScoredPlayer)