from django.shortcuts import render, get_object_or_404
from account.models import FNSUser
from team.models import Team
# Create your views here.
def individualRank(request):
    if not request.session.get('userId'):
        errormessage = '로그인을 해주세요.'
        return render(request, 'login.html', {'errormessage':errormessage})
    fnsuser = get_object_or_404(FNSUser, pk=request.session.get('userId'))
    notification = fnsuser.to.all().order_by('-created')
    countNotification = notification.filter(userCheck = False).count() 
    scoreFnsuser = FNSUser.objects.all().order_by('-score')
    gaFnsuser = FNSUser.objects.all().order_by('-goalAverage')
    return render(request, 'individualRank.html', {'countNotification':countNotification,
    'notification':notification, 'fnsuser':fnsuser, 'scoreFnsuser':scoreFnsuser, 'gaFnsuser':gaFnsuser})

def individualGa(request):
    fnsuser = get_object_or_404(FNSUser, pk=request.session.get('userId'))
    notification = fnsuser.to.all().order_by('-created')
    countNotification = notification.filter(userCheck = False).count() 
    gaFnsuser = FNSUser.objects.all().order_by('-goalAverage')
    
    return render(request, 'individualGa.html', {'countNotification':countNotification,
    'notification':notification, 'fnsuser':fnsuser, 'gaFnsuser':gaFnsuser})
    

def teamRank(request):
    fnsuser = get_object_or_404(FNSUser, pk=request.session.get('userId'))
    notification = fnsuser.to.all().order_by('-created')
    countNotification = notification.filter(userCheck = False).count() 
    teams = Team.objects.all().order_by('-point')
    return render(request, 'teamRank.html', {'countNotification':countNotification,
    'notification':notification, 'fnsuser':fnsuser, 'teams':teams})