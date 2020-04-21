from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import PlaygroundList, ReservationList
from team.models import Team
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
import datetime
from account.models import FNSUser

# Create your views here.
def playground_list(request):
    playgrounds = PlaygroundList.objects.all().order_by('created')
    Teams = Team.objects.all().order_by('created')
    
    if request.session.get('userId', None) != None:
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
        data = {
            'fnsuser':fnsuser,
            'notification':notification,
            'countNotification':countNotification,
            'notificationList': notificationList,
            'playgrounds' : playgrounds,
        }
        return render(request, 'reservation/playground_list.html', data)
    
    else:
        data = {
            'playgrounds': playgrounds
        }
        return render(request, 'reservation/playground_list.html', data)


def playground(request, id):
    playground = get_object_or_404(PlaygroundList, id = id)
    
    if request.session.get('userId', None) != None:
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
        data = {
            'fnsuser':fnsuser,
            'notification':notification,
            'countNotification':countNotification,
            'notificationList': notificationList,
            'playground' : playground,
        }
        return render(request, 'reservation/playground.html', data)

    else:
        data = {
            'playground' : playground,
        }
        return render(request, 'reservation/playground.html', data)


def goReservation(request, id):

    if not (request.session.get('userId')):
        errormessage = '로그인을 해주세요.'
        return render(request, 'login.html', {'errormessage':errormessage})

    playground = get_object_or_404(PlaygroundList, id = id)

    reservationPossible = [["06"],["07"],["08"],["09"],["10"],["11"],["12"],["13"],["14"],["15"],["16"],["17"],["18"],["19"],["20"],["21"],["22"],["23"]]
    weekArray = []

    today = datetime.datetime.now()
    for i in range(0, 10):
        tomorrow = today + datetime.timedelta(days=i)
        tomorrow_formet = tomorrow.strftime("%Y%m%d") 
        weekArray.append(tomorrow_formet)

    selectedDay = request.GET.get('selectedDay')
    if not (selectedDay):
        selectedDay = datetime.datetime.now().strftime("%Y%m%d") 

    for idx, reservation in enumerate(reservationPossible): 
        
        playgroundName = playground.playgroundName
        reservationTime = reservation[0] + "00"

        price = playground.weekDayPrice
        if reservation[0] > '17':
            price = playground.weekNightPrice

        checkReservation = ReservationList.objects.filter(playgroundName = playground, reservationDate = selectedDay ,reservationTime = reservationTime)      

        existReservation = 0
        if checkReservation:
            existReservation = 1

        reservationPossible[idx].append(price)
        reservationPossible[idx].append(existReservation)


    if request.session.get('userId', None) != None:
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
        data = {
            'fnsuser':fnsuser,
            'notification':notification,
            'countNotification':countNotification,
            'notificationList': notificationList,
            'playground' : playground,
            "reservationPossible" : reservationPossible, 
            "today" : today, 
            "weekArray" : weekArray, 
            "selectedDay" : selectedDay
        }

        return render(request, 'reservation/goReservation.html', data)

    else:
        data = {
            'playground' : playground,
            "reservationPossible" : reservationPossible, 
            "today" : today, 
            "weekArray" : weekArray, 
            "selectedDay" : selectedDay
        }
        return render(request, 'reservation/goReservation.html', data)


def tryReservation(request):

    id = request.GET.get('id')
    playground = get_object_or_404(PlaygroundList, id = id)
    reservationTime = request.POST.get('reservationTime', None)
    reservationDate = request.POST.get('reservationDate', None)
    totalPrice = request.POST.get('totalPrice', None)
    reservationTimeArray = reservationTime.split(",")
    reservedDateToString = reservationDate[0:4] + "년 " + reservationDate[4:6] + "월 " + reservationDate[6:8] + "일"
    reservationLength = len(reservationTimeArray)

    # 유저정보
    if request.session.get('userId', None) != None:
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
        # 유저정보 끝

    err_msg = ""
    for reservation in reservationTimeArray:
        # 중복 예약을 체크
        checkReservation = ReservationList.objects.filter(playgroundName = playground, reservationDate = reservationDate ,reservationTime = reservation)

        if checkReservation:
            err_msg = "duplicate reservation"

            if request.session.get('userId', None) != None:
                data = {
                    'fnsuser':fnsuser,
                    'notification':notification,
                    'countNotification':countNotification,
                    'notificationList': notificationList,
                    'err_msg' : err_msg, 
                    'id' : id
                }

            else:
                data = {
                    'err_msg' : err_msg, 
                    'id' : id
                }

            return render(request, 'reservation/tryReservation.html', data)
        
    if err_msg != "duplicate reservation":
        err_msg = "try reservation"
        reserved_time = []

        for idx, reservation in enumerate(reservationTimeArray):

            if idx == 0:
                reserved_time.append(reservation[0:2])
            if idx == (len(reservationTimeArray) - 1):
                reserved_time.append(int(reservation[0:2]) + 1)

        if request.session.get('userId', None) != None:
            data = {
                'fnsuser':fnsuser,
                'notification':notification,
                'countNotification':countNotification,
                'notificationList': notificationList,
                'err_msg' : err_msg, 
                "totalPrice" : totalPrice, 
                "reserved_time" : reserved_time, 
                "playground" : playground, 
                "reservedDateToString" : reservedDateToString, 
                "reservationLength" : reservationLength, 
                "reservationTime" : reservationTime, 
                "reservationDate" : reservationDate
            }

        else:
            data = {
                'err_msg' : err_msg, 
                "totalPrice" : totalPrice, 
                "reserved_time" : reserved_time, 
                "playground" : playground, 
                "reservedDateToString" : reservedDateToString, 
                "reservationLength" : reservationLength, 
                "reservationTime" : reservationTime, 
                "reservationDate" : reservationDate
            }

        return render(request, 'reservation/tryReservation.html/', data)


def resultReservation(request):
    if request.session.get('userId', None) != None:
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
    else:
        errormessage = '로그인을 해주세요.'
        data = {
            'errormessage':errormessage
        }   
        return redirect('account/login')

    id = request.GET.get('id')
    playground = get_object_or_404(PlaygroundList, id = id)
    reservationTime = request.POST.get('reservationTime', None)
    reservationDate = request.POST.get('reservationDate', None)
    reservationTimeArray = reservationTime.split(",")
    reservationLength = len(reservationTimeArray)
    reservationName = request.POST.get('user_name', None)   
    reservationPhone = request.POST.get('user_phone', None)   
    totalPrice = request.POST.get('totalPrice', None)
    err_msg = ""
    reserved_time = []

    for idx, reservation in enumerate(reservationTimeArray):
        newReservation = ReservationList(user = fnsuser, playgroundName = playground, reservationDate = reservationDate, reservationTime = reservation, resercationUserId = "moonlit0130", reservationUserName = reservationName, resercationUserPhone = reservationPhone)
        newReservation.save()

        if idx == 0:
            reserved_time.append(reservation[0:2])
        if idx == (len(reservationTimeArray) - 1):
            reserved_time.append(int(reservation[0:2]) + 1)

    

    
    data = {
        'fnsuser':fnsuser,
        'notification':notification,
        'countNotification':countNotification,
        'notificationList': notificationList,
        'err_msg' : err_msg, 
        'id' : id, 
        "reserved_time" : reserved_time, 
        "reservationLength" : reservationLength, 
        "playground" : playground, 
        "totalPrice" : totalPrice
    }  
    
    return render(request, 'reservation/resultReservation.html', data)

def paymentPop(request):

    pay_method = request.POST.get('pay_method', None)
    totalPrice = request.POST.get('totalPrice', None)
    user_name = request.POST.get('user_name', None)
    user_phone = request.POST.get('user_phone', None)

    data = {
        'pay_method' : pay_method,
        'totalPrice' : totalPrice,
        'user_name' : user_name,
        'user_phone' : user_phone        
    }

    return render(request, 'reservation/paymentPop.html', data)


def mobilePayment(request):
    payResult = request.GET.get('imp_success', None)
    data = {
        'payResult' : payResult
    }

    return render(request, 'reservation/mobilePayment.html', data)