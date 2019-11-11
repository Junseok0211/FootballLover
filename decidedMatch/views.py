from django.shortcuts import render, get_object_or_404
from decidedMatch.models import DecidedMatch
from result.models import Result, ScoredPlayer, AttendedPlayer
from account.models import FNSUser
from django.core.paginator import Paginator
import datetime
# Create your views here.
def decidedMatch(request):
    if not (request.session.get('userId')):
        errormessage = '로그인을 해주세요.'
        return render(request, 'login.html', {'errormessage':errormessage})
    matches = DecidedMatch.objects.all().order_by('-timeFrom')
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

        # 객체를 한 페이지로 자르기
    matchPaginator = Paginator(matches, 10)
    # request에 담아주기
    matchPage = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    matchList = matchPaginator.get_page(matchPage)
    
    return render(request, 'decidedMatch.html', {'countNotification':countNotification,
    'notificationList':notificationList, 'fnsuser':fnsuser, 'matchList':matchList})

def decidedDetail(request, decidedMatch_id):
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

    decidedMatch = get_object_or_404(DecidedMatch, pk=decidedMatch_id)
    myAttendedPlayer = AttendedPlayer.objects.filter(match = decidedMatch.match, team = decidedMatch.myTeam).all()
    vsAttendedPlayer = AttendedPlayer.objects.filter(match = decidedMatch.match, team = decidedMatch.vsTeam).all()
    myScoredPlayer = ScoredPlayer.objects.filter(match = decidedMatch.match, team = decidedMatch.myTeam).all()
    vsScoredPlayer = ScoredPlayer.objects.filter(match = decidedMatch.match, team = decidedMatch.vsTeam).all()

    now = datetime.datetime.now()
    timeFrom = decidedMatch.timeFrom
    timeTo = decidedMatch.timeTo
    state = None
    if now < timeFrom:
        state = 'before'
    elif now > timeFrom and now < timeTo:
        state = "ing"
    elif now > timeTo:
        state = 'finished'

    return render(request, 'decidedDetail.html', {'countNotification':countNotification, 'state':state,
    'notificationList':notificationList, 'fnsuser':fnsuser, 'decidedMatch':decidedMatch, 'myAttendedPlayer':myAttendedPlayer,
    'vsAttendedPlayer':vsAttendedPlayer,'myScoredPlayer':myScoredPlayer,'vsScoredPlayer':vsScoredPlayer})
