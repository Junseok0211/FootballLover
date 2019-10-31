from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from .forms import RegisterForm
from django.contrib.auth.hashers import make_password, check_password
from . import models as m
from .models import FNSUser
import requests
# Create your views here.

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    elif request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        res_data = {}
        if not (username and password):
            res_data['error'] = '모든 값을 입력해야 합니다.'

        else:
            fnsuser = FNSUser.objects.get(username = username)
            if check_password(password, fnsuser.password):
                # 비밀번호 일치, 로그인 처리
                # 세션
                request.session['userId'] = fnsuser.id
                request.session['name'] = fnsuser.name
                return redirect('/')
            else:
                res_data['error'] = '비밀번호가 틀렸습니다.'

        return render(request, 'login.html', res_data)


def logout(request):
    if request.session.get('userId'):
        del(request.session['userId'])
        del(request.session['name'])

    return redirect('/')

def test(request):
    datetimepicker = request.GET.get('datetimepicker')
    timepicker = request.GET.get('timepicker')
    return render(request, 'test1.html', {'datetimepicker':datetimepicker,'timepicker':timepicker})

def test2(request):
    return render(request, 'test2.html')

def test3(request):
    date = request.POST.get('date')
    time = date.substr(11,15)
    return render(request, 'test2.html', {'time':time})

def register(request):
    if request.method == "GET":
        return render(request, 'register.html')
    elif request.method == "POST":
        if(request.FILES['userimg'] is not None):
            userimg = request.FILES['userimg']
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        re_password = request.POST.get('re_password', None)
        name = request.POST.get('name', None)
        region = request.POST.get('region', None)
        city = "error"

        if request.POST.get('seoul') is not None:
            city = request.POST.get('seoul')
        
        elif request.POST.get('gyeonggi') is not None:
            city = request.POST.get('gyeonggi')

        elif request.POST.get('north_chungcheong') is not None:
            city = request.POST.get('north_chungcheong')
        
        elif request.POST.get('south_chungcheong') is not None:
            city = request.POST.get('south_chungcheong')
        
        elif request.POST.get('north_jeolla') is not None:
            city = request.POST.get('north_jeolla')

        elif request.POST.get('south_jeolla') is not None:
            city = request.POST.get('south_jeolla')

        elif request.POST.get('north_gyeongsang') is not None:
            city = request.POST.get('north_gyeongsang')

        elif request.POST.get('south_gyeongsang') is not 'south_gyeongsang':
            city = request.POST.get('south_gyeongsang')

        elif request.POST.get('jeju') is not 'jeju':
            city = request.POST.get('jeju')
        
        school = request.POST.get('school', None)
        phone_number = request.POST.get('phone_number', None)
        auth_number = request.POST.get('auth_number', None)
        # 키값이 없으면 none을 지정하라는 뜻

        res_data = {}

        if (username is None or password is None or re_password is None or 
        name is None or email is None or region is None or school is None 
        or phone_number is None or auth_number is None):
            res_data['error'] = "프로필 사진을 제외한 모든 값을 입력해야 합니다."
            res_data['userimg'] = userimg
            res_data['username'] = username
            res_data['email'] = email
            res_data['password'] = password
            res_data['name'] = name
            res_data['region'] = region
            res_data['city'] = city
            res_data['school'] = school
            res_data['phone_number'] = phone_number
            res_data['auth_number'] = auth_number

        else:
            if FNSUser.objects.filter(username = username):
                res_data['error'] = '중복된 아이디가 있습니다.'    
                return render(request, 'register.html', {'res_data':res_data})

            res_data['error'] = '성공'
            fnsuser = FNSUser.objects.get(phone_number = phone_number, auth_number = auth_number)
            fnsuser.userimg = userimg
            fnsuser.username = username
            fnsuser.email = email
            fnsuser.password = make_password(password)
            fnsuser.name = name
            fnsuser.region = region
            fnsuser.city = city
            fnsuser.school = school
            fnsuser.save()
            return render(request, 'login.html')
            # m.FNSUser.objects.update_or_create(
            # userimg = userimg,
            # username = username,
            # email = email,
            # password = make_password(password),
            # name = name,
            # region = region,
            # city = city,
            # school = school,
            # phone_number=phone_number, 
            # auth_number=auth_number
            # )


        return render(request, 'register.html', {'res_data':res_data})

def myPage(request, fnsuser_id):
    fnsuser = get_object_or_404(FNSUser, pk=fnsuser_id)
    notification = fnsuser.to.all().order_by('-created')
    countNotification = notification.filter(userCheck = False).count() 
    return render(request, 'myPage.html', {'countNotification':countNotification,
    'notification':notification, 'fnsuser':fnsuser})

def checkId(request):
    id = request.POST.get('username')
    checkId = FNSUser.objects.all().filter(username=id).exists()
    return JsonResponse({'checkId':checkId})

class FNSAuth(APIView):
    # post는 sendSMS
    @method_decorator(csrf_protect)
    def post(self, request):
        try:
            p_num = request.data['phone_number']
        except KeyError:
            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            fnsuser = FNSUser.objects.filter(phone_number = p_num).first()
                    
            if fnsuser:
                fnsuser = FNSUser.objects.get(phone_number = p_num)
                if fnsuser.name == '':
                    message = "문자 메시지를 보냈습니다."
                    m.FNSUser.objects.update_or_create(phone_number=p_num)
                    return JsonResponse({'message':message})
                else:
                    message = "이미 등록된 휴대폰입니다."
                    return JsonResponse({'message':message})
            else:
                message = "문자 메시지를 보냈습니다."
                m.FNSUser.objects.update_or_create(phone_number=p_num)
                return JsonResponse({'message':message})

            return JsonResponse({'message':message})
            # return Response({'message': 'OK'})
            # return render(request, 'test1.html', {'p_num': p_num})

    # get는 checkSMS
    def get(self, request):
        try:
            p_num = request.query_params['phone_number']
            a_num = request.query_params['auth_number']
        except KeyError:
            return Response({'message': '인증실패'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            result = m.FNSUser.check_auth_number(p_num, a_num)
            return Response({'message': '인증완료', 'result': result})
