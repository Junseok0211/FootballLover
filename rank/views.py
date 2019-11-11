from django.shortcuts import render, get_object_or_404
from account.models import FNSUser
from django.core.paginator import Paginator
from team.models import Team
# Create your views here.
def individualRank(request):
    if not request.session.get('userId'):
        errormessage = '로그인을 해주세요.'
        return render(request, 'login.html', {'errormessage':errormessage})
    fnsuser = get_object_or_404(FNSUser, pk=request.session.get('userId'))
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.filter(userCheck = False).count() 
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')[:20]
    # 객체를 한 페이지로 자르기
    paginator = Paginator(notification, 5)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    notificationList = paginator.get_page(page)
    scoreFnsuser = FNSUser.objects.all().order_by('-score')
    gaFnsuser = FNSUser.objects.all().order_by('-goalAverage')

    # 객체를 한 페이지로 자르기
    scorePaginator = Paginator(scoreFnsuser, 10)
    gaPaginator = Paginator(gaFnsuser, 10)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    scoreList = scorePaginator.get_page(page)
    gaList = gaPaginator.get_page(page)
    return render(request, 'individualRank.html', {'countNotification':countNotification, 'scoreList':scoreList, 'gaList':gaList,
    'notificationList':notificationList, 'fnsuser':fnsuser, 'scoreFnsuser':scoreFnsuser, 'gaFnsuser':gaFnsuser})

def individualGa(request):
    fnsuser = get_object_or_404(FNSUser, pk=request.session.get('userId'))
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.filter(userCheck = False).count() 
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')[:20]
    # 객체를 한 페이지로 자르기
    paginator = Paginator(notification, 5)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    notificationList = paginator.get_page(page)
    gaFnsuser = FNSUser.objects.all().order_by('-goalAverage')
    
    return render(request, 'individualGa.html', {'countNotification':countNotification,
    'notificationList':notificationList, 'fnsuser':fnsuser, 'gaFnsuser':gaFnsuser})
    

def teamRank(request):
    fnsuser = get_object_or_404(FNSUser, pk=request.session.get('userId'))
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.filter(userCheck = False).count() 
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')[:20]
    # 객체를 한 페이지로 자르기
    paginator = Paginator(notification, 5)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    notificationList = paginator.get_page(page)
    teams = Team.objects.all().order_by('-point')
    return render(request, 'teamRank.html', {'countNotification':countNotification,
    'notificationList':notificationList, 'fnsuser':fnsuser, 'teams':teams})