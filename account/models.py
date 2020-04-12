from django.db import models
from django.core.validators import MinLengthValidator
from model_utils.models import TimeStampedModel
from django.utils import timezone
from random import randint
from team.models import Team
import requests
import datetime

# Create your models here.

class FNSUser(TimeStampedModel):
    sms = models.BooleanField(default=False)
    isStaff = models.BooleanField(default=False)
    userimg = models.ImageField(upload_to = "userimg")
    username = models.CharField(max_length=15, validators=[MinLengthValidator(8)],
                                verbose_name='아이디')
    email = models.EmailField(max_length=30,
                                  verbose_name='사용자이메일')
    password = models.CharField(max_length=150,
                                verbose_name='비밀번호')
    # password = models.CharField(max_length=15, validators=[MinLengthValidator(8)],
    name = models.CharField(max_length=10,
                            verbose_name='이름')
    birthday = models.IntegerField(default=000000, null=True, blank=True,
                            verbose_name='생년월일')
    region = models.CharField(max_length = 10,
                            verbose_name='활동지역도')
    city = models.CharField(max_length = 10,
                            verbose_name='활동지역시')
    school = models.CharField(max_length=10, null = True,
                            verbose_name='학교')
    teamname = models.ForeignKey(Team, on_delete=models.SET_NULL, related_name='member' , null=True, blank=True)
    matchcount = models.IntegerField(default=0,
                                    verbose_name='경기수', blank=True, null=True)
    score = models.IntegerField(default=0,
                                verbose_name='득점수', blank=True, null=True)
    goalAverage = models.FloatField(default = 0, verbose_name='득점률', blank=True, null=True)
    registered_date = models.DateTimeField(auto_now_add=True,
                                           verbose_name='등록시간', null = True, blank = True)

    sessionId = models.CharField(null=True, default=None, max_length=100)
    phone_number = models.CharField(verbose_name='휴대폰 번호', unique = True, max_length=11)
    auth_number = models.IntegerField(verbose_name='인증 번호', blank=True, null=True)

    servicePolicy = models.BooleanField(verbose_name="이용약관 동의", default=True)
    informationPolicy = models.BooleanField(verbose_name="개인정보처리방침 동의", default=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'FNSUser'
        verbose_name = 'FNS 사용자'
        verbose_name_plural = 'FNS 사용자' 

    def save(self, *args, **kwargs):
        self.auth_number = randint(10000,100000)
        super().save(*args, **kwargs)
        if not self.sms:
            self.send_sms() #인증번호가 담긴 SMS를 전송

    def send_sms(self):
        url = 'https://api-sens.ncloud.com/v1/sms/services/ncp:sms:kr:256774183707:fns/messages/'
        data = {
            "type": "SMS",
            "from": "01050509042",
            "to": [self.phone_number],
            "content": "[풋볼러버] 인증 번호 [{}]를 입력해주세요.".format(self.auth_number)
        }
        headers = {
            "Content-Type": "application/json",
            "x-ncp-auth-key": "fnWjFriyC3BquhVC9cpb",
            "x-ncp-service-secret": "75d5fd6b78e047768ebe0786bffe5fb0",
        }
        requests.post(url, json=data, headers=headers)

    @classmethod
    def check_auth_number(cls, p_num, c_num):
        time_limit = timezone.now() - datetime.timedelta(minutes=5)
        result = cls.objects.filter(
            phone_number=p_num,
            auth_number=c_num,
            modified__gte=time_limit
        )
        if result:
            return True
        return False


