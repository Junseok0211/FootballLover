from django.shortcuts import render, get_object_or_404
from decidedMatch.models import DecidedMatch
from django import template
from team.models import Team
from result.models import Result, AttendedPlayer, ScoredPlayer
from account.models import FNSUser
from django.core.paginator import Paginator
from notification.models import Notification
import datetime
# Create your views here.
register = template.Library()

def result(request):
    if not (request.session.get('userId')):
        result = Result.objects.filter(confirm = True).order_by('-timeFrom')
        # 객체를 한 페이지로 자르기
        resultPaginator = Paginator(result, 15)
        # request에 담아주기
        resultPage = request.GET.get('page')
        # request된 페이지를 얻어온 뒤 return 해 준다.
        resultList = resultPaginator.get_page(resultPage)
        return render(request, 'result.html', {'resultList':resultList})
    else:
        result = Result.objects.filter(confirm = True).order_by('-timeFrom')
        # 객체를 한 페이지로 자르기
        resultPaginator = Paginator(result, 15)
        # request에 담아주기
        resultPage = request.GET.get('page')
        # request된 페이지를 얻어온 뒤 return 해 준다.
        resultList = resultPaginator.get_page(resultPage)

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

        return render(request, 'result.html', {'resultList':resultList, 'countNotification':countNotification, 
        'notificationList':notificationList, 'fnsuser':fnsuser})

def input(request, decidedMatch_id):
    decidedMatch = get_object_or_404(DecidedMatch, pk = decidedMatch_id)
    myTeam = decidedMatch.myTeam.member.all()
    vsTeam = decidedMatch.vsTeam.member.all()
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

    if fnsuser != decidedMatch.myTeam.teamleader and fnsuser != decidedMatch.vsTeam.teamleader:
        message = '팀주장만 결과를 입력할 수 있습니다.'
        return render(request, 'decidedDetail.html', {'message':message, 'fnsuser':fnsuser, 
        'countNotification':countNotification, 'notificationList':notificationList, 'decidedMatch': decidedMatch})

    return render(request, 'input.html', {'fnsuser':fnsuser, 'decidedMatch': decidedMatch, 'myTeam':myTeam, 
    'countNotification':countNotification, 'notificationList':notificationList, 'vsTeam':vsTeam})


def inputScorer(request):
    attendedPlayer_id = request.POST.getlist('attendedPlayer_id[]')
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
    decidedMatch_id = request.POST.get('decidedMatch_id')
    decidedMatch = get_object_or_404(DecidedMatch, pk = decidedMatch_id)
    myTeamScore = request.POST.get('myTeamScore')
    vsTeamScore = request.POST.get('vsTeamScore')

    if fnsuser != decidedMatch.myTeam.teamleader and fnsuser != decidedMatch.vsTeam.teamleader:
        message = '팀주장만 결과를 입력할 수 있습니다.'
        return render(request, 'decidedDetail.html', {'message':message, 'fnsuser':fnsuser, 
        'countNotification':countNotification, 'notificationList':notificationList, 'decidedMatch': decidedMatch})


    attendedPlayer = []
    num = 1
    for pk in attendedPlayer_id:
        user = get_object_or_404(FNSUser, pk=pk)
        attendedPlayer.insert(num, user)
        num += 1

    if decidedMatch.myTeam.teamleader == fnsuser:
        score = []
        for i in range(0, int(myTeamScore)): 
            name = i+1
            score.insert(i, name)

    elif decidedMatch.vsTeam.teamleader == fnsuser:
        score = []
        for i in range(0, int(vsTeamScore)): 
            name = i+1
            score.insert(i, name)


    number = len(attendedPlayer)
    vsTeamScore = request.POST.get('vsTeamScore')
    test = request.POST.get('test')
    return render(request, 'inputScorer.html', 
    {'attendedPlayer_id':attendedPlayer_id, 'number':number, 'attendedPlayer': attendedPlayer , 'score': score, 
    'countNotification':countNotification, 'notificationList':notificationList, 'myTeamScore': myTeamScore, 
    'fnsuser':fnsuser, 'vsTeamScore': vsTeamScore , 'decidedMatch': decidedMatch})

def myTeamResult(request):
    decidedMatch_id = request.POST.get('decidedMatch_id')
    decidedMatch = get_object_or_404(DecidedMatch, pk = decidedMatch_id)
    fnsuser = get_object_or_404(FNSUser, pk=request.session.get('userId'))
    
    if decidedMatch.my_suggest == False and decidedMatch.vs_suggest == False:
        result = Result.objects.create()
    else: 
        result = get_object_or_404(Result, pk = decidedMatch.result.id)

    result.myTeam = decidedMatch.myTeam
    result.vsTeam = decidedMatch.vsTeam
    result.myTeamScore = request.POST.get('myTeamScore')
    result.vsTeamScore = request.POST.get('vsTeamScore')
    
    result.match = decidedMatch
    result.timeFrom = decidedMatch.timeFrom
    attendedPlayer_id = request.POST.getlist('attendedPlayer_id[]')
    number = len(attendedPlayer_id)
    num = 0
    for i in range(0, number):
        number = attendedPlayer_id[i]
        user = get_object_or_404(FNSUser, pk= number)
        attendedPlayer = AttendedPlayer.objects.create(player = user, team = user.teamname, match = decidedMatch.match)
        num+=1


    scorer = []
    if decidedMatch.myTeam.teamleader == fnsuser:
        newNotification = Notification.objects.create(
            creator = get_object_or_404(FNSUser, pk=request.session.get('userId')),
            to = decidedMatch.vsTeam.teamleader,
            notification_type = Notification.resultInput,
            teamMatching = decidedMatch.match,
            team = decidedMatch.myTeam
        )
           
        newNotification.resultInputText()
        newNotification.save()
        num = result.myTeamScore
    elif decidedMatch.vsTeam.teamleader == fnsuser:
        num = result.vsTeamScore
    for i in range(1, int(num)+1):
        name = 'scorer' + str(i)
        pk = request.POST.get(name)
        
        if pk == 'ownGoal':
            scoredPlayer = ScoredPlayer.objects.create(player = None, team = fnsuser.teamname, match = decidedMatch.match)
        else:
            user = get_object_or_404(FNSUser, pk=pk)
            scoredPlayer = ScoredPlayer.objects.create(player = user, team = user.teamname, match = decidedMatch.match)

    if fnsuser == decidedMatch.myTeam.teamleader:
        decidedMatch.my_suggest = True
        result.myCheck = True
        if int(result.vsTeamScore) != ScoredPlayer.objects.filter(team = result.vsTeam, match = decidedMatch.match).count():
            if decidedMatch.vs_suggest == True:
                result.vsCheck = False
                decidedMatch.vs_confirm = False
                decidedMatch.vs_suggest = False
        else:
            result.vsCheck = True

    elif fnsuser == decidedMatch.vsTeam.teamleader:
        newNotification = Notification.objects.create(
            creator = get_object_or_404(FNSUser, pk=request.session.get('userId')),
            to = decidedMatch.myTeam.teamleader,
            notification_type = Notification.resultInput,
            teamMatching = decidedMatch.match,
            team = decidedMatch.vsTeam
        )
           
        newNotification.resultInputText()
        newNotification.save()

        decidedMatch.vs_suggest = True
        result.vsCheck = True
        if int(result.myTeamScore) != ScoredPlayer.objects.filter(team = result.myTeam, match = decidedMatch.match).count():
            if decidedMatch.my_suggest == True:
                decidedMatch.my_confirm = False
                decidedMatch.my_suggest = False
                result.myCheck = False
                # myCheck가 False 면 myTeam에서 입력을 확인하고 수정해야 함.
        else:
            result.myCheck = True

    decidedMatch.save()
    decidedMatch = get_object_or_404(DecidedMatch, pk = decidedMatch_id)
    result2 = result
    result.save()
    result = result2
    matches = DecidedMatch.objects.all().order_by('-created')
    matchPaginator = Paginator(matches, 10)
    # request에 담아주기
    matchPage = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    matchList = matchPaginator.get_page(matchPage)

    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')[:20]
    # 객체를 한 페이지로 자르기
    paginator = Paginator(notification, 5)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    notificationList = paginator.get_page(page)
    return render(request, 'decidedMatch.html', {'matchList':matchList ,'result':result, 'fnsuser':fnsuser,
    'countNotification':countNotification, 'notificationList':notificationList, 'decidedMatch':decidedMatch})
   
        
def edit(request, decidedMatch_id):
    decidedMatch = get_object_or_404(DecidedMatch, pk = decidedMatch_id)
    myTeam = decidedMatch.myTeam.member.all()
    vsTeam = decidedMatch.vsTeam.member.all()
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

    attendedPlayer = AttendedPlayer.objects.filter(match = decidedMatch.match, team = fnsuser.teamname).all()
    return render(request, 'edit.html', {'myTeam':myTeam,'vsTeam':vsTeam,'fnsuser':fnsuser,
    'countNotification':countNotification, 'notificationList':notificationList, 'decidedMatch':decidedMatch, 'attendedPlayer':attendedPlayer})

def editScorer(request):
    attendedPlayer_id = request.POST.getlist('attendedPlayer_id[]')
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

    decidedMatch_id = request.POST.get('decidedMatch_id')
    decidedMatch = get_object_or_404(DecidedMatch, pk = decidedMatch_id)
    myTeamScore = request.POST.get('myTeamScore')
    vsTeamScore = request.POST.get('vsTeamScore')
    if fnsuser != decidedMatch.myTeam.teamleader and fnsuser != decidedMatch.vsTeam.teamleader:
        message = '팀주장만 결과를 입력할 수 있습니다.'
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
        return render(request, 'decidedDetail.html', {'fnsuser':fnsuser, 'decidedMatch':decidedMatch, 
        'myAttendedPlayer':myAttendedPlayer, 'state':state, 'countNotification':countNotification, 
        'notificationList':notificationList, 'vsAttendedPlayer':vsAttendedPlayer,
        'myScoredPlayer':myScoredPlayer,'vsScoredPlayer':vsScoredPlayer, 'message':message})


    attendedPlayer = []
    num = 1
    for pk in attendedPlayer_id:
        user = get_object_or_404(FNSUser, pk=pk)
        attendedPlayer.insert(num, user)
        num += 1

    if decidedMatch.myTeam.teamleader == fnsuser:
        score = []
        for i in range(0, int(myTeamScore)): 
            name = i+1
            score.insert(i, name)

    elif decidedMatch.vsTeam.teamleader == fnsuser:
        score = []
        for i in range(0, int(vsTeamScore)): 
            name = i+1
            score.insert(i, name)


    number = len(attendedPlayer)
    vsTeamScore = request.POST.get('vsTeamScore')
    scoredPlayer = ScoredPlayer.objects.filter(match=decidedMatch.match, team = fnsuser.teamname).all()
    return render(request, 'editScorer.html', 
    {'countNotification':countNotification, 'notificationList':notificationList, 'scoredPlayer': scoredPlayer, 
    'attendedPlayer_id':attendedPlayer_id, 'number':number, 'attendedPlayer': attendedPlayer , 'score': score , 
    'fnsuser':fnsuser, 'myTeamScore': myTeamScore, 'vsTeamScore': vsTeamScore , 'decidedMatch': decidedMatch})


def editTeamResult(request):
    decidedMatch_id = request.POST.get('decidedMatch_id')
    decidedMatch = get_object_or_404(DecidedMatch, pk = decidedMatch_id)
    fnsuser = get_object_or_404(FNSUser, pk=request.session.get('userId'))
    

    result = get_object_or_404(Result, pk = decidedMatch.result.id)

    result.myTeamScore = request.POST.get('myTeamScore')
    result.vsTeamScore = request.POST.get('vsTeamScore')
    
    result.match = decidedMatch
    result.timeFrom = decidedMatch.timeFrom
    attendedPlayer_id = request.POST.getlist('attendedPlayer_id[]')
    number = len(attendedPlayer_id)
    num = 0
    preAttendedPlayer = AttendedPlayer.objects.filter(team = fnsuser.teamname, match = decidedMatch.match).order_by('created')
    for player in preAttendedPlayer:
        player.delete()

    for i in range(0, number):
        number = attendedPlayer_id[i]
        user = get_object_or_404(FNSUser, pk= number)
        attendedPlayer = AttendedPlayer.objects.create(player = user, team = user.teamname, match = decidedMatch.match)
        num+=1


    scorer = []
    preScoredPlayer = ScoredPlayer.objects.filter(team = fnsuser.teamname, match = decidedMatch.match)
    for player in preScoredPlayer:
        player.delete()

    if decidedMatch.myTeam.teamleader == fnsuser:
        num = result.myTeamScore
    elif decidedMatch.vsTeam.teamleader == fnsuser:
        num = result.vsTeamScore

    for i in range(1, int(num)+1):
        name = 'scorer' + str(i)
        pk = request.POST.get(name)
        
        if pk == 'ownGoal':
            scoredPlayer = ScoredPlayer.objects.create(player = None, team = fnsuser.teamname, match = decidedMatch.match)
        else:
            user = get_object_or_404(FNSUser, pk=pk)
            scoredPlayer = ScoredPlayer.objects.create(player = user, team = user.teamname, match = decidedMatch.match)

 
    if fnsuser == decidedMatch.myTeam.teamleader:
        newNotification = Notification.objects.create(
            creator = get_object_or_404(FNSUser, pk=request.session.get('userId')),
            to = decidedMatch.vsTeam.teamleader,
            notification_type = Notification.resultEdit,
            teamMatching = decidedMatch.match,
            team = decidedMatch.myTeam
        )
           
        newNotification.resultEditText()
        newNotification.save()

        decidedMatch.my_suggest = True
        decidedMatch.vs_confirm = False
        result.myCheck = True
        if int(result.vsTeamScore) != ScoredPlayer.objects.filter(team = result.vsTeam, match = decidedMatch.match).count():
            if decidedMatch.vs_suggest == True:
                result.vsCheck = False
                decidedMatch.vs_confirm = False
                decidedMatch.vs_suggest = False
        else:
            result.vsCheck = True
            

    elif fnsuser == decidedMatch.vsTeam.teamleader:
        newNotification = Notification.objects.create(
            creator = get_object_or_404(FNSUser, pk=request.session.get('userId')),
            to = decidedMatch.myTeam.teamleader,
            notification_type = Notification.resultEdit,
            teamMatching = decidedMatch.match,
            team = decidedMatch.vsTeam
        )
           
        newNotification.resultEditText()
        newNotification.save()

        decidedMatch.vs_suggest = True
        decidedMatch.my_confirm = False
        result.vsCheck = True
        if int(result.myTeamScore) != ScoredPlayer.objects.filter(team = result.myTeam, match = decidedMatch.match).count():
            if decidedMatch.my_suggest == True:
                decidedMatch.my_confirm = False
                decidedMatch.my_suggest = False
                result.myCheck = False
                # myCheck가 False 면 myTeam에서 입력을 확인하고 수정해야 함.
        else:
            result.myCheck = True
                
            

    decidedMatch.save()
    decidedMatch = get_object_or_404(DecidedMatch, pk = decidedMatch_id)
    result2 = result
    result.save()
    result = result2
    matches = DecidedMatch.objects.all().order_by('-created')
    matchPaginator = Paginator(matches, 10)
    # request에 담아주기
    matchPage = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    matchList = matchPaginator.get_page(matchPage)

    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')[:20]
    # 객체를 한 페이지로 자르기
    paginator = Paginator(notification, 5)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    notificationList = paginator.get_page(page)

    return render(request, 'decidedMatch.html', {'countNotification':countNotification, 
    'notificationList':notificationList, 
    'fnsuser':fnsuser, 'matchList':matchList ,'result':result, 'decidedMatch':decidedMatch})


def myConfirm(request, decidedMatch_id):
    decidedMatch = get_object_or_404(DecidedMatch, pk = decidedMatch_id)
    decidedMatch.my_confirm = True
    decidedMatch.save()
    newNotification = Notification.objects.create(
            creator = get_object_or_404(FNSUser, pk=request.session.get('userId')),
            to = decidedMatch.vsTeam.teamleader,
            notification_type = Notification.resultConfirm,
            teamMatching = decidedMatch.match,
            team = decidedMatch.myTeam
        )
           
    newNotification.resultConfirmText()
    newNotification.save()

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

    myAttendedPlayer = AttendedPlayer.objects.filter(match = decidedMatch.match, team = decidedMatch.myTeam).all()
    vsAttendedPlayer = AttendedPlayer.objects.filter(match = decidedMatch.match, team = decidedMatch.vsTeam).all()
    myScoredPlayer = ScoredPlayer.objects.filter(match = decidedMatch.match, team = decidedMatch.myTeam).all()
    vsScoredPlayer = ScoredPlayer.objects.filter(match = decidedMatch.match, team = decidedMatch.vsTeam).all()
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
    result = decidedMatch.result

    if decidedMatch.vs_confirm:
        decidedMatch.result.confirm = True
        decidedMatch.result.save()
        myTeamId = decidedMatch.myTeam.id
        myTeam = get_object_or_404(Team, pk = myTeamId)
        myTeam.gf = result.myTeamScore
        myTeam.ga = result.vsTeamScore
        myTeam.gd = int(result.myTeamScore - result.vsTeamScore)
        myTeam.matchcount += 1
        if (myTeam.gf > myTeam.ga):
            myTeam.win += 1
            myTeam.point += 3
        elif (myTeam.gf == myTeam.ga):
            myTeam.draw += 1
            myTeam.point += 1
        elif (myTeam.gf < myTeam.ga):
            myTeam.lose += 1

        myTeam.save()
        attendedPlayer = AttendedPlayer.objects.filter(team = decidedMatch.myTeam, match = decidedMatch.match).all()
        scoredPlayer = ScoredPlayer.objects.filter(team = decidedMatch.myTeam, match = decidedMatch.match).all()
        for player in attendedPlayer:
            user = player.player
            if user is not None:
                user.matchcount += 1
                user.save()

        for player in scoredPlayer:
            user = player.player
            if user is not None:
                user.score += 1
                if float(user.score) is 0:
                    goalAverage = 0
                else:
                    goalAverage = float(user.score) / float(user.matchcount)
                average = round(goalAverage, 3)
                user.goalAverage = average
                user.save()

        vsTeamId = decidedMatch.vsTeam.id
        vsTeam = get_object_or_404(Team, pk = vsTeamId)
        vsTeam.gf = result.vsTeamScore
        vsTeam.ga = result.myTeamScore
        vsTeam.gd = int(result.vsTeamScore - result.myTeamScore)
        vsTeam.matchcount += 1
        if (vsTeam.gf > vsTeam.ga):
            vsTeam.win += 1
            vsTeam.point += 3
        elif (vsTeam.gf == vsTeam.ga):
            vsTeam.draw += 1
            vsTeam.point += 1
        elif (vsTeam.gf < vsTeam.ga):
            vsTeam.lose += 1

        vsTeam.save()
        attendedPlayer = AttendedPlayer.objects.filter(team = decidedMatch.vsTeam, match = decidedMatch.match).all()
        scoredPlayer = ScoredPlayer.objects.filter(team = decidedMatch.vsTeam, match = decidedMatch.match).all()
        for player in attendedPlayer:
            user = player.player
            if user is not None:
                user.matchcount += 1
                user.save()

        for player in scoredPlayer:
            user = player.player
            if user is not None:
                user.score += 1
                if float(user.score) is 0:
                    goalAverage = 0
                else:
                    goalAverage = float(user.score) / float(user.matchcount)
                average = round(goalAverage, 3)
                user.goalAverage = average
                user.save()

    decidedMatch = get_object_or_404(DecidedMatch, pk = decidedMatch_id)
    return render(request, 'decidedDetail.html', {'fnsuser':fnsuser, 'decidedMatch':decidedMatch, 'myAttendedPlayer':myAttendedPlayer,
    'state':state, 'countNotification':countNotification, 'notificationList':notificationList, 'vsAttendedPlayer':vsAttendedPlayer,'myScoredPlayer':myScoredPlayer,'vsScoredPlayer':vsScoredPlayer})

def vsConfirm(request, decidedMatch_id):
    decidedMatch = get_object_or_404(DecidedMatch, pk = decidedMatch_id)
    decidedMatch.vs_confirm = True
    decidedMatch.save()
    
    newNotification = Notification.objects.create(
        creator = get_object_or_404(FNSUser, pk=request.session.get('userId')),
        to = decidedMatch.myTeam.teamleader,
        notification_type = Notification.resultConfirm,
        teamMatching = decidedMatch.match,
        team = decidedMatch.vsTeam
    )
           
    newNotification.resultConfirmText()
    newNotification.save()

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

    myAttendedPlayer = AttendedPlayer.objects.filter(match = decidedMatch.match, team = decidedMatch.myTeam).all()
    vsAttendedPlayer = AttendedPlayer.objects.filter(match = decidedMatch.match, team = decidedMatch.vsTeam).all()
    myScoredPlayer = ScoredPlayer.objects.filter(match = decidedMatch.match, team = decidedMatch.myTeam).all()
    vsScoredPlayer = ScoredPlayer.objects.filter(match = decidedMatch.match, team = decidedMatch.vsTeam).all()
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
    result = decidedMatch.result

    if decidedMatch.my_confirm:
        decidedMatch.result.confirm = True
        decidedMatch.result.save()
        myTeamId = decidedMatch.myTeam.id
        myTeam = get_object_or_404(Team, pk = myTeamId)
        myTeam.gf = result.myTeamScore
        myTeam.ga = result.vsTeamScore
        myTeam.gd = int(result.myTeamScore - result.vsTeamScore)
        myTeam.matchcount += 1
        if (myTeam.gf > myTeam.ga):
            myTeam.win += 1
            myTeam.point += 3
        elif (myTeam.gf == myTeam.ga):
            myTeam.draw += 1
            myTeam.point += 1
        elif (myTeam.gf < myTeam.ga):
            myTeam.lose += 1

        myTeam.save()
        attendedPlayer = AttendedPlayer.objects.filter(team = decidedMatch.myTeam, match = decidedMatch.match).all()
        scoredPlayer = ScoredPlayer.objects.filter(team = decidedMatch.myTeam, match = decidedMatch.match).all()
        for player in attendedPlayer:
            user = player.player
            if user is not None:
                user.matchcount += 1
                user.save()

        for player in scoredPlayer:
            user = player.player
            if user is not None:
                user.score += 1
                if float(user.score) is 0:
                    goalAverage = 0
                else:
                    goalAverage = float(user.score) / float(user.matchcount)
                average = round(goalAverage, 3)
                user.goalAverage = average
                user.save()
                

        vsTeamId = decidedMatch.vsTeam.id
        vsTeam = get_object_or_404(Team, pk = vsTeamId)
        vsTeam.gf = result.vsTeamScore
        vsTeam.ga = result.myTeamScore
        vsTeam.gd = int(result.vsTeamScore - result.myTeamScore)
        vsTeam.matchcount += 1
        if (vsTeam.gf > vsTeam.ga):
            vsTeam.win += 1
            vsTeam.point += 3
        elif (vsTeam.gf == vsTeam.ga):
            vsTeam.draw += 1
            vsTeam.point += 1
        elif (vsTeam.gf < vsTeam.ga):
            vsTeam.lose += 1

        vsTeam.save()
        attendedPlayer = AttendedPlayer.objects.filter(team = decidedMatch.vsTeam, match = decidedMatch.match).all()
        scoredPlayer = ScoredPlayer.objects.filter(team = decidedMatch.vsTeam, match = decidedMatch.match).all()
        for player in attendedPlayer:
            user = player.player
            if user is not None:
                user.matchcount += 1
                user.save()

        for player in scoredPlayer:
            user = player.player
            if user is not None:
                user.score += 1
                if float(user.score) is 0:
                    goalAverage = 0
                else:
                    goalAverage = float(user.score) / float(user.matchcount)
                average = round(goalAverage, 3)
                user.goalAverage = average
                user.save()
                
            
    decidedMatch = get_object_or_404(DecidedMatch, pk = decidedMatch_id)
    return render(request, 'decidedDetail.html', {'fnsuser':fnsuser, 'decidedMatch':decidedMatch, 'myAttendedPlayer':myAttendedPlayer,
    'state':state, 'countNotification':countNotification, 'notificationList':notificationList, 'vsAttendedPlayer':vsAttendedPlayer,'myScoredPlayer':myScoredPlayer,'vsScoredPlayer':vsScoredPlayer})
    