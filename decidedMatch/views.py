from django.shortcuts import render, get_object_or_404
from decidedMatch.models import DecidedMatch
from result.models import Result, ScoredPlayer, AttendedPlayer
from account.models import FNSUser
from django.core.paginator import Paginator
import datetime
# Create your views here.
def decidedMatch(request):
    matches = DecidedMatch.objects.all().order_by('-timeFrom')
    fnsuser = get_object_or_404(FNSUser, pk=request.session.get('userId'))
    notification = fnsuser.to.all().order_by('-created')
    countNotification = notification.filter(userCheck = False).count() 

        # 객체를 한 페이지로 자르기
    matchPaginator = Paginator(matches, 10)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    matchList = matchPaginator.get_page(page)
    
    return render(request, 'decidedMatch.html', {'countNotification':countNotification, 'matchList':matchList,
    'notification':notification, 'fnsuser':fnsuser, 'matches':matches})

def decidedDetail(request, decidedMatch_id):
    fnsuser = get_object_or_404(FNSUser, pk=request.session.get('userId'))
    notification = fnsuser.to.all().order_by('-created')
    countNotification = notification.filter(userCheck = False).count() 
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
    'notification':notification, 'fnsuser':fnsuser, 'decidedMatch':decidedMatch, 'myAttendedPlayer':myAttendedPlayer,
    'vsAttendedPlayer':vsAttendedPlayer,'myScoredPlayer':myScoredPlayer,'vsScoredPlayer':vsScoredPlayer})
