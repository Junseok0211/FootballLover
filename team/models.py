from django.db import models
from django.core.validators import MinLengthValidator
from model_utils.models import TimeStampedModel
from django.utils import timezone
from random import randint
import requests
import datetime

# Create your models here.

class Team(models.Model):
    name = models.CharField(max_length = 20)
    region = models.CharField(max_length = 10)
    city = models.CharField(max_length = 10)
    school = models.CharField(max_length = 10)
    introduction = models.TextField(max_length = 300)

    win = models.IntegerField(null=True, default=0, blank=True)
    draw = models.IntegerField(null=True, default=0, blank=True)
    lose = models.IntegerField(null=True, default=0, blank=True)
    matchcount = models.IntegerField(null=True, default=0, blank=True)
    point = models.IntegerField(null=True, default=0, blank=True)
    
    gf = models.IntegerField(null=True, default=0, blank=True)
    ga = models.IntegerField(null=True, default=0, blank=True)
    gd = models.IntegerField(null=True, default=0, blank=True)
    rank = models.CharField(max_length=30, null=True, default=0)

    teamimg = models.ImageField(upload_to="teamimg", null =True)

    created = models.DateTimeField(auto_now_add= True, null = True, blank = True)
    updated = models.DateTimeField(auto_now = True, null = True, blank = True)
    teamleader = models.OneToOneField('account.FNSUser', related_name= 'captain', on_delete=models.SET_NULL, null=True, blank=True)
    applied_member = models.ManyToManyField('account.FNSUser', related_name='applied', blank=True, default=0)

    def summary(self):
        return self.introduction[:20]

    def __str__(self):
        return self.name