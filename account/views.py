from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from .forms import RegisterForm
from django.contrib.auth.hashers import make_password, check_password
from . import models as m
from django.core.paginator import Paginator
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
    fnsuser = get_object_or_404(FNSUser, pk = request.session.get('userId'))
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.filter(userCheck=False).count()
     # 객체를 한 페이지로 자르기
    paginator = Paginator(notification, 5)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    notificationList = paginator.get_page(page)
    return render(request, 'test1.html', {'notification':notification,
    'fnsuser':fnsuser, 'countNotification':countNotification, 'notificationList':notificationList})

def test2(request):
    fnsuser = FNSUser.objects.all()
    return render(request, 'test2.html', {'fnsuser':fnsuser})

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
            fnsuser.sms = True
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
    fnsuser = get_object_or_404(FNSUser, pk=request.session.get('userId'))
    pageUser = get_object_or_404(FNSUser, pk = fnsuser_id)
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.filter(userCheck = False).count() 
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')[:20]
    # 객체를 한 페이지로 자르기
    paginator = Paginator(notification, 5)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    notificationList = paginator.get_page(page)
    if fnsuser != pageUser:
        return render(request, 'myPage.html', {'countNotification':countNotification,
        'notificationList':notificationList, 'fnsuser':fnsuser, 'pageUser':pageUser})    
    else:
        return render(request, 'personalMyPage.html', {'countNotification':countNotification,
        'notificationList':notificationList, 'fnsuser':fnsuser, 'pageUser':pageUser})

def checkId(request):
    id = request.POST.get('username')
    checkId = FNSUser.objects.all().filter(username=id).exists()
    return JsonResponse({'checkId':checkId})

def findId(request):
    if request.method == 'GET':
        return render(request, 'findId.html')
    else:
        name = request.POST.get('name').strip()
        email = request.POST.get('email').strip()

        if not name:
            error = '이름을 입력해주세요.'
            return render(request, 'findId.html', {'error':error})
        elif not email:
            error = '이메일을 입력해주세요.'
            return render(request, 'findId.html', {'error':error})
        findUser = FNSUser.objects.filter(name=name, email=email)
        return render(request, 'findResult.html', {'findUser':findUser})

def findPw(request):
    if request.method == 'GET':
        return render(request, 'findPw.html')

    else:
        username = request.POST.get('username')
        phone_number = request.POST.get('email')
        

        if not username:
            error = '아이디를 입력해주세요.'
            return render(request, 'findPw.html', {'error':error})
        elif not phone_number:
            error = '휴대폰 번호를 입력해주세요.'
            return render(request, 'findPw.html', {'error':error})
        
        return render(request, 'login.html')

def sendSMS(request):
    username = request.POST.get('username')
    p_num = request.POST.get('phone_number')
    if FNSUser.objects.filter(phone_number = p_num, username=username).count() == 0:
        message = "입력하신 정보에 맞는 회원이 없습니다."
        return JsonResponse({'message':message})    
    else:
        fnsuser = FNSUser.objects.get(phone_number = p_num, username=username)
        fnsuser.save()
        message='성공적으로 메시지를 보냈습니다.'
        return JsonResponse({'message':message})
    
def changePw(request):
    username = request.POST.get('username')
    phone_number = request.POST.get('phone_number')
    auth_number = request.POST.get('auth_number')

    if not username:
        error = '아이디를 입력해주세요.'
        return render(request, 'findPw.html', {'error':error})

    elif not phone_number:
        error = '휴대폰 번호를 입력해주세요.'
        return render(request, 'findPw.html', {'error':error})

    elif not auth_number:
        error = '인증번호를 입력해주세요.'
        return render(request, 'findPw.html', {'error':error})

    return render(request, 'changePw.html', {'username':username, 'phone_number':phone_number, 'auth_number':auth_number})

def finalPw(request):
    username = request.POST.get('username')
    phone_number = request.POST.get('phone_number')
    auth_number = request.POST.get('auth_number')
    password = request.POST.get('password')
    re_password = request.POST.get('re_password')

    if not username:
        errormessage = '중간에 오류가 생겨 처음부터 다시 해주세요.'
        return render(request, 'findPw.html', {'errormessage':errormessage})

    if not phone_number:
        errormessage = '중간에 오류가 생겨 처음부터 다시 해주세요.'
        return render(request, 'findPw.html', {'errormessage':errormessage})

    if not auth_number:
        errormessage = '중간에 오류가 생겨 처음부터 다시 해주세요.'
        return render(request, 'findPw.html', {'errormessage':errormessage})
        
    if not password:
        error = '비밀번호를 입력해주세요.'
        return render(request, 'changePw.html', {'error':error})

    elif not re_password:
        error = '비밀번호 확인을 입력해주세요.'
        return render(request, 'changePw.html', {'error':error})

    fnsuser = FNSUser.objects.get(phone_number = phone_number, username=username, auth_number=auth_number)
    fnsuser.password = make_password(password)
    fnsuser.sms = True
    fnsuser.save()
    pwSuccess = '비밀번호 변경에 성공했습니다.'
    return render(request, 'login.html', {'pwSuccess':pwSuccess})

def editAccount(request):
    
    fnsuser = get_object_or_404(FNSUser, pk = request.session.get('userId'))
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')[:20]
    # 객체를 한 페이지로 자르기
    paginator = Paginator(notification, 5)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    notificationList = paginator.get_page(page)
    if request.method == 'GET':
        return render(request, 'editAccount.html', {'fnsuser':fnsuser, 'notificationList':notificationList,
        'countNotification':countNotification})
    else:
        if(request.FILES['userimg'] is not None):
            userimg = request.FILES['userimg']
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
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
        # 키값이 없으면 none을 지정하라는 뜻

        res_data = {}

        if (username is None or userimg is None or 
        name is None or email is None or region is None or school is None):
            res_data['error'] = "모든 값을 입력해야 합니다."
            res_data['userimg'] = userimg
            res_data['username'] = username
            res_data['email'] = email
            res_data['name'] = name
            res_data['region'] = region
            res_data['city'] = city
            res_data['school'] = school

        else:
            # if FNSUser.objects.filter(username = username):
            #     res_data['error'] = '중복된 아이디가 있습니다.'    
            #     return render(request, 'myPage.html', {'res_data':res_data, 'fnsuser':fnsuser, 
            #     'notificationList':notificationList, 'countNotification':countNotification})

            res_data['error'] = '성공'
            fnsuser.userimg = userimg
            fnsuser.username = username
            fnsuser.email = email
            fnsuser.name = name
            fnsuser.region = region
            fnsuser.city = city
            fnsuser.school = school
            fnsuser.sms = True
            fnsuser.save()
            return render(request, 'login.html', {'res_data':res_data, 'fnsuser':fnsuser, 
            'notificationList':notificationList, 'countNotification':countNotification})

        return render(request, 'login.html', {'res_data':res_data, 'fnsuser':fnsuser, 
        'notificationList':notificationList, 'countNotification':countNotification})

def checkPhone_number(request):
    phone_number = request.POST['phone_number']
    username = request.POST['username']
    isUsername = FNSUser.objects.filter(username = username).exists()
    fnsuser = FNSUser.objects.get(username = username)
    if isUsername:
        # 휴대폰 번호가 등록되어 있는 번호와 다를 때
        if str(fnsuser.phone_number) != str(phone_number):
            message = '아이디에 등록되어 있는 휴대폰 번호가 틀립니다.'
            return JsonResponse({'message':message})
        else:
            message = 'True'
            return JsonResponse({'message':message})
    else:
        message = '아이디가 등록되어 있지 않습니다.'
        return JsonResponse({'message':message})

class FNSAuth(APIView):
    # post는 sendSMS
    @method_decorator(csrf_protect)
    def post(self, request):
        try:
            p_num = request.data['phone_number']
            findPw = request.data['findPw']
        except KeyError:
            return JsonResponse({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            fnsuser = FNSUser.objects.filter(phone_number = p_num).first()
                    
            if fnsuser:
                fnsuser = FNSUser.objects.get(phone_number = p_num)
                if fnsuser.name == '':
                    message = "문자 메시지를 보냈습니다."
                    m.FNSUser.objects.update_or_create(phone_number=p_num)
                    return JsonResponse({'message':message})
                else:
                    if findPw == 'findPw':
                        message = "문자 메시지를 보냈습니다."
                        fnsuser.sms = False
                        fnsuser.save()
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
