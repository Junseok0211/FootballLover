from django.conf import settings
from django.db import models
from django.utils import timezone
from account.models import FNSUser
import datetime

# Create your models here.
class PlaygroundList(models.Model):
    playgroundName = models.CharField(max_length = 100)
    playgroundLocation = models.CharField(max_length = 200)
    weekDayPrice = models.CharField(max_length = 200)
    weekNightPrice = models.CharField(max_length = 200)
    weekendDayPrice = models.CharField(max_length = 200)
    weekendNightPrice = models.CharField(max_length = 200)
    playgroundPhoto = models.ImageField(upload_to="playground", null=True)
    playgroundOption1 = models.BooleanField(default=True)
    playgroundOption2 = models.BooleanField(default=True)
    playgroundOption3 = models.BooleanField(default=True)
    playgroundOption4 = models.BooleanField(default=True)
    playgroundOption5 = models.BooleanField(default=True)
    playgroundOption6 = models.BooleanField(default=True)
    playgroundInfo = models.TextField(max_length = 500)
    possibleReservation = models.BooleanField(default=True)

    region = models.CharField(max_length = 10,
                            verbose_name='소재지(시/도)', null=True, blank = True)
    city = models.CharField(max_length = 10,
                            verbose_name='소재지(시/군/구)', null=True, blank = True)

    created = models.DateTimeField(auto_now_add= True, null = True, blank = True)
    updated = models.DateTimeField(auto_now = True, null = True, blank = True)
    

    def summary(self):
        return self.playgroundInfo[:20]

    def __str__(self):
        return self.playgroundName


class ReservationList(models.Model):
    playgroundName = models.ForeignKey(PlaygroundList, on_delete=models.CASCADE)
    reservationDate = models.CharField(max_length = 10)
    reservationTime = models.CharField(max_length = 10)
    resercationUserId = models.CharField(max_length = 45)
    reservationUserName = models.CharField(max_length = 10)
    user = models.ForeignKey(FNSUser, on_delete = models.SET_NULL, related_name='reservedGround', null = True, blank = True)
    resercationUserPhone = models.CharField(max_length = 15)
    created = models.DateTimeField(auto_now_add= True, null = True, blank = True)
    updated = models.DateTimeField(auto_now = True, null = True, blank = True)

    def __str__(self):
        return self.reservationDate
