from django import forms
from django.db import models
from django.core.validators import MinLengthValidator
from team.models import Team
from model_utils.models import TimeStampedModel
from django.utils import timezone
from random import randint
import requests
import datetime

class DateForm(forms.Form):
    date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])

class RegisterForm(forms.Form):
    userimg = forms.ImageField()
    username = forms.CharField(max_length=20, validators=[MinLengthValidator(8)],
                                label='아이디', error_messages={'required': '아이디를 입력해주세요.'})
    email = forms.EmailField(max_length=128,
                            label='사용자이메일', error_messages={'required': '이메일을 입력해주세요.'})
    password = forms.CharField(max_length=20, validators=[MinLengthValidator(8)],
                                label='비밀번호', error_messages={'required': '비밀번호를 입력해주세요.'},
                                widget= forms.PasswordInput)
    re_password = forms.CharField(max_length=20, validators=[MinLengthValidator(8)],
                                label='비밀번호 확인', error_messages={'required': '아이디를 입력해주세요.'},
                                widget= forms.PasswordInput)                            
    name = forms.CharField(max_length=20,
                            label='이름', error_messages={'required': '이름을 입력해주세요.'})
    region_ex = (('1', '서울특별시'), ('2', '경기도'),)

    region = forms.ChoiceField(widget=forms.Select, choices=region_ex,
                            label='활동지역도',error_messages={'required': '시도를 입력해주세요.'})
    city_ex = (
        ('1', '남서울대 재학생'),
        ('2', '타대학교 학생'),
        ('3', '지역주민'),
    )
    city = forms.ChoiceField(widget=forms.Select, choices=city_ex,
                            label='활동지역시', error_messages={'required': '시군구를 입력해주세요.'})
    uni = (
        ('1', '남서울대 재학생'),
        ('2', '타대학교 학생'),
        ('3', '지역주민'),
    )
    school = forms.ChoiceField(widget=forms.Select, choices=uni, label='학교', error_messages={'required': '학교를 입력해주세요.'})

    phone_number = forms.CharField(label='휴대폰 번호', max_length=11,
    error_messages={'required': '휴대폰 번호를 입력해주세요.'})
    auth_number = forms.IntegerField(label='인증 번호',
    error_messages={'required': '인증 번호를 입력해주세요.'}) 

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        re_password = cleaned_data.get('re_password')

        if password and re_password:
            if password != re_password:
                self.add_error('password', '비밀번호가 서로 다릅니다.')
                self.add_error('re_password', '비밀번호가 서로 다릅니다.')
       