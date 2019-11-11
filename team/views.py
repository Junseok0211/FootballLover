from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.exceptions import ObjectDoesNotExist
from .models import Team
from account.models import FNSUser
from match.models import TeamMatching
from django.core.paginator import Paginator
from decidedMatch.models import DecidedMatch
from notification.models import Notification

# Create your views here.

def team(request):
    teams = Team.objects.all().order_by('created')
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

          # 객체를 한 페이지로 자르기
    teamPaginator = Paginator(teams, 10)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    teamList = teamPaginator.get_page(page)
    return render(request, 'team.html', {'countNotification':countNotification, 'notificationList':notificationList, 
    'teamList':teamList, 'fnsuser':fnsuser, 'teams' : teams})

def detail(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    members = team.member.all()
    is_member = team.member.filter(pk=request.session.get('userId')).exists()
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

    is_applied = fnsuser.applied.all().filter(pk=team_id).exists()
    return render(request, 'detail.html', {'notificationList':notificationList, 'fnsuser':fnsuser, 
    'countNotification':countNotification, 'team': team, 'members': members, 'is_member':is_member, 'is_applied':is_applied})

def new(request):
    userId = request.session.get('userId')
    teams = Team.objects.all()
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
    if not (userId):
        error = '로그인을 해야 팀을 생성할 수 있습니다.'
        return render(request, 'team.html', {'notificationList':notificationList, 'fnsuser':fnsuser, 
        'countNotification':countNotification, 'error':error, 'teams' : teams})

    if fnsuser.teamname:
        error = '한 사람이 여러 개의 팀을 만들 수 없습니다.'
        teams = Team.objects.all()
        return render(request, 'team.html', {'notificationList':notificationList, 'fnsuser':fnsuser, 
        'countNotification':countNotification, 'error':error, 'teams' : teams})

    return render(request, 'new.html', {'countNotification':countNotification, 'notificationList':notificationList, 'fnsuser':fnsuser})

def create(request):
    team = Team()
    fnsuser = get_object_or_404(FNSUser, pk = request.session.get('userId'))
    team.teamimg = request.FILES['teamimg']
    team.name = request.POST.get('name')
    team.introduction = request.POST.get('introduction')
    team.region = request.POST.get('region')
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
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

    elif request.POST.get('south_gyeongsang') is not None:
        city = request.POST.get('south_gyeongsang')

    elif request.POST.get('jeju') is not None:
        city = request.POST.get('jeju')

    team.city = city
    team.school = request.POST.get('school')
    user_id = request.session.get('userId')
    teamleader = get_object_or_404(FNSUser, pk=user_id)    
    team.teamleader = teamleader
    team.save()
    fnsuser.teamname = team
    fnsuser.save()
    return redirect('/team/')


def delete(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    if(request.user != post.user):
        return redirect('/team')
    post.delete()
    return redirect('/team/')

def application(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    pk = request.session.get('userId')
    fnsuser = get_object_or_404(FNSUser, pk=pk)
    is_applied = team.applied_member.filter(pk=pk).exists()
    members = team.member.all()
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')[:20]
    # 객체를 한 페이지로 자르기
    paginator = Paginator(notification, 5)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    notificationList = paginator.get_page(page)
    is_member = members.filter(pk=pk).exists()
    applied_number = fnsuser.applied.all().count()
    if applied_number == 1:
        message = '동시에 여러 팀에 지원하실 수 없습니다.'
        return render(request, 'detail.html', {'notificationList':notificationList, 'fnsuser':fnsuser, 
        'countNotification':countNotification, 'team': team, 'members': members, 'message':message })

    if is_member:
        message = '이미 팀 회원이십니다.'
        return render(request, 'detail.html', {'notificationList':notificationList, 'fnsuser':fnsuser, 
        'countNotification':countNotification, 'team': team, 'members': members, 'message':message })

    is_othermember = fnsuser.teamname
    if is_othermember:
        message = '이미 다른 팀에 가입하셨습니다.'
        return render(request, 'detail.html', {'notificationList':notificationList, 'fnsuser':fnsuser, 
        'countNotification':countNotification, 'team': team, 'members': members, 'message':message })

    if is_applied:
        message = '이미 가입신청이 완료되었습니다.'    
    else:
        message = '가입신청이 완료되었습니다.'
        team.applied_member.add(fnsuser)

        newNotification = Notification.objects.create(
        creator = get_object_or_404(FNSUser, pk=request.session.get('userId')),
        to = team.teamleader,
        notification_type = Notification.joinTeam,
        team = team
        )
            
        newNotification.joinTeamText()
        newNotification.save()

    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')[:20]
    # 객체를 한 페이지로 자르기
    paginator = Paginator(notification, 5)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    notificationList = paginator.get_page(page)
    is_applied = fnsuser.applied.all().filter(pk=team_id).exists()

    return render(request, 'detail.html', {'notificationList':notificationList, 'fnsuser':fnsuser, 'is_applied':is_applied,
    'countNotification':countNotification, 'team': team, 'members': members, 'message':message, 'is_member':is_member })
    
def cancelApplication(request, team_id):
    team = get_object_or_404(Team, pk = team_id)
    fnsuser = get_object_or_404(FNSUser, pk = request.session.get('userId'))
    team.applied_member.remove(fnsuser)
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    teams = Team.objects.all()
    countNotification = notification.filter(userCheck = False).count()
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')[:20]
    # 객체를 한 페이지로 자르기
    paginator = Paginator(notification, 5)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    notificationList = paginator.get_page(page)

    message = '가입신청을 취소했습니다.'
    return render(request, 'team.html', {'message':message, 'countNotification':countNotification, 'notificationList':notificationList, 'fnsuser':fnsuser, 'teams' : teams})

def teamApplicationDenied(request, team_id, player_id):
    team = get_object_or_404(Team, pk = team_id)
    fnsuser = get_object_or_404(FNSUser, pk = request.session.get('userId'))
    player = get_object_or_404(FNSUser, pk=player_id)
    team.applied_member.remove(player)
    newNotification = Notification.objects.create(
        creator = get_object_or_404(FNSUser, pk=request.session.get('userId')),
        to = player,
        notification_type = Notification.teamApplicationDenied,
        team = team
    )
            
    newNotification.teamApplicationDeniedText()
    newNotification.save()
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    teams = Team.objects.all()
    countNotification = notification.filter(userCheck = False).count()
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')[:20]
    # 객체를 한 페이지로 자르기
    paginator = Paginator(notification, 5)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    notificationList = paginator.get_page(page)

    is_applied = fnsuser.applied.all().filter(pk=team_id).exists()
    is_member = team.member.filter(pk=request.session.get('userId')).exists()

    message = '가입신청을 거절했습니다.'
    return render(request, 'detail.html', {'message':message, 'countNotification':countNotification, 
    'is_member':is_member, 'is_applied':is_applied, 'notificationList':notificationList, 'fnsuser':fnsuser, 'teams' : teams, 'team':team})




def applied_list(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    pk = request.session.get('userId')
    fnsuser = get_object_or_404(FNSUser, pk=pk)
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')[:20]
    # 객체를 한 페이지로 자르기
    paginator = Paginator(notification, 5)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    notificationList = paginator.get_page(page)

    members = team.member.all()
    applied_members = team.applied_member.all()
    message = ''
    is_applied = fnsuser.applied.all().filter(pk=team_id).exists()
    is_member = team.member.filter(pk=request.session.get('userId')).exists()
    if team.teamleader != fnsuser:
        message = '팀대표만 참가신청현황을 볼 수 있습니다.'
        return render(request, 'detail.html', {'notificationList':notificationList, 'fnsuser':fnsuser, 'is_member':is_member,
        'is_applied':is_applied, 'countNotification':countNotification, 'team': team, 'members': members, 'message':message })

    else:
        return render(request, 'applied_list.html', {'notificationList':notificationList, 'fnsuser':fnsuser, 
        'countNotification':countNotification, 'team': team, 'applied_members': applied_members, 'message':message })

def approve(request, team_id, fnsuser_id):
    team = get_object_or_404(Team, pk=team_id)
    fnsuser1 = get_object_or_404(FNSUser, pk=fnsuser_id)
    fnsuser = get_object_or_404(FNSUser, pk=request.session.get('userId'))
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    team.applied_member.remove(fnsuser1)
    team.save()
    fnsuser1.teamname = team
    fnsuser1.save()
    members = team.member.all()
    applied_members = team.applied_member.all()

    newNotification = Notification.objects.create(
    creator = get_object_or_404(FNSUser, pk=request.session.get('userId')),
    to = fnsuser1,
    notification_type = Notification.teamAccepted,
    team = team
    )
        
    newNotification.teamAcceptedText()
    newNotification.save()
    message = '성공적으로 가입수락이 되었습니다.'

    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')[:20]
    # 객체를 한 페이지로 자르기
    paginator = Paginator(notification, 5)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    notificationList = paginator.get_page(page)

    return render(request, 'applied_list.html', {'countNotification':countNotification, 'notificationList':notificationList, 'fnsuser':fnsuser, 
    'message':message, 'applied_members':applied_members, 'team':team})

def dropout(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
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
    is_member = team.member.filter(pk=request.session.get('userId')).exists()
    is_applied = fnsuser.applied.all().filter(pk=team_id).exists()
    message = ''
    # 혼자인데 팀을 탈퇴한 경우 -> 팀도 삭제
    if team.member.all().count() < 2:
        fnsuser.teamname = None
        team.delete()
        fnsuser.save()
        message = '성공적으로 팀탈퇴가 되었습니다.'
        teams = Team.objects.all().order_by('created')
        return render(request, 'team.html', {'countNotification':countNotification, 'notificationList':notificationList, 'fnsuser':fnsuser, 
        'teams': teams, 'message':message})
        
    else:
        if fnsuser == team.teamleader:
            message = '팀 탈퇴를 하기 전 대표를 변경해주세요.'
            members = team.member.all()
            is_member = team.member.filter(pk=request.session.get('userId')).exists()
            return render(request, 'detail.html', {'countNotification':countNotification, 'notificationList':notificationList, 'fnsuser':fnsuser, 
            'is_member':is_member, 'is_applied':is_applied, 'team': team, 'members':members, 'is_member':is_member, 'message':message})

        else:
            team.applied_member.remove(fnsuser)
            team.save()
            fnsuser.teamname = None
            fnsuser.save()
            members = team.member.all()
            is_member = team.member.filter(pk=request.session.get('userId')).exists()

    
    message = '성공적으로 팀탈퇴가 되었습니다.'
    is_applied = fnsuser.applied.all().filter(pk=team_id).exists()
    return render(request, 'detail.html', {'countNotification':countNotification, 'notificationList':notificationList, 'fnsuser':fnsuser, 
    'team': team, 'members':members, 'is_member':is_member, 'message':message, 'is_applied':is_applied})

def searchTeam(request):
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
    condition = request.POST.get('condition')
    content = request.POST.get('content')
    teams = None
    if condition == 'name':
        teams = Team.objects.all().filter(name__icontains = content).order_by('-created')

    elif condition == 'city':
        teams = Team.objects.all().filter(city__icontains = content).order_by('-created')
    
    elif condition == 'school':
        teams = Team.objects.all().filter(school__icontains = content).order_by('-created')

    
    count = str(teams.count())    


    return render(request, 'team.html', {'countNotification':countNotification, 'notificationList':notificationList, 'fnsuser':fnsuser, 
    'teams':teams, 'count':count})

def changeCaptain(request, team_id):
    user_id = request.POST.get('captain')
    captain = get_object_or_404(FNSUser, pk = user_id)
    team = get_object_or_404(Team, pk = team_id)
    fnsuser = get_object_or_404(FNSUser, pk = request.session.get('userId'))
    team.teamleader = captain
    team.save()
    members = team.member.all()
    is_member = team.member.filter(pk=request.session.get('userId')).exists()
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')[:20]
    # 객체를 한 페이지로 자르기
    paginator = Paginator(notification, 5)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    notificationList = paginator.get_page(page)
    is_applied = fnsuser.applied.all().filter(pk=team_id).exists()
    message = '성공적으로 주장이 변경되었습니다.'
    return render(request, 'detail.html', {'notificationList':notificationList, 'fnsuser':fnsuser, 'message'
    'countNotification':countNotification, 'team': team, 'members': members, 'is_member':is_member, 'is_applied':is_applied})


def suggestTeamMatching(request, team_id):
    if request.method == 'GET':
        fnsuser = get_object_or_404(FNSUser, pk=request.session.get('userId'))
        myteam = fnsuser.teamname
        notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
        countNotification = notification.filter(userCheck = False).count()
        notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')[:20]
        # 객체를 한 페이지로 자르기
        paginator = Paginator(notification, 5)
        # request에 담아주기
        page = request.GET.get('page')
        # request된 페이지를 얻어온 뒤 return 해 준다.
        notificationList = paginator.get_page(page)
        return render(request, 'suggestTeamMatching.html', {'myteam':myteam, 'notificationList':notificationList, 
        'team_id':team_id, 'countNotification':countNotification, 'fnsuser':fnsuser})

    elif request.method == 'POST':
        fnsuser = get_object_or_404(FNSUser, pk=request.session.get('userId'))
        myteam = get_object_or_404(Team, pk=fnsuser.teamname.id)
        vs_team = get_object_or_404(Team, pk = team_id)

        teamMatching = TeamMatching()
        teamMatching.myteam = myteam
        teamMatching.vs_team = vs_team
        teamMatching.user = fnsuser
        teamMatching.title = request.POST.get('title')
        teamMatching.location = request.POST.get('location')
        time_from = request.POST.get('time_from')
        year = time_from[:4]
        month = time_from[5:7]
        date = time_from[8:10]
        hour = time_from[11:13]
        minute = time_from[14:16]
        startTime = year + '-' + month + '-' + date + ' ' + hour + ':' + minute
        teamMatching.time_from = startTime
        time_to = request.POST.get('time_to')
        endHour = time_to[:2]
        endMin = time_to[3:5]
        endTime = year + '-' + month + '-' + date + ' ' + endHour + ':' + endMin
        teamMatching.time_to = endTime
        teamMatching.is_applied = True
        teamMatching.content = request.POST.get('content')
        teamMatching.save()

        vsTeamMember = vs_team.member.all()
        for member in vsTeamMember:
            newNotification = Notification.objects.create(
                creator = get_object_or_404(FNSUser, pk=request.session.get('userId')),
                to = member,
                notification_type = Notification.suggestTeamMatching,
                team = vs_team,
            )
            newNotification.suggestTeamMatchingText()
            newNotification.save()

        is_member = vs_team.member.filter(pk=request.session.get('userId')).exists()
        notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
        countNotification = notification.filter(userCheck = False).count()
        notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')[:20]
        # 객체를 한 페이지로 자르기
        paginator = Paginator(notification, 5)
        # request에 담아주기
        page = request.GET.get('page')
        # request된 페이지를 얻어온 뒤 return 해 준다.
        notificationList = paginator.get_page(page)
        is_applied = fnsuser.applied.all().filter(pk=team_id).exists()
        message = '성공적으로 매치신청을 했습니다.'
        members = vs_team.member.all()
        return render(request, 'detail.html', {'notificationList':notificationList, 'fnsuser':fnsuser, 'message':message,
        'members':members, 'countNotification':countNotification, 'team': vs_team, 'is_member':is_member, 'is_applied':is_applied})

def suggestList(request, team_id):
    fnsuser = get_object_or_404(FNSUser, pk = request.session.get('userId'))
    team = get_object_or_404(Team, pk = team_id)
    teams = Team.objects.all()
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')[:20]
    # 객체를 한 페이지로 자르기
    paginator = Paginator(notification, 5)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    notificationList = paginator.get_page(page)
    if(fnsuser.teamname != team):
        message = '팀원만 확인할 수 있습니다.'
        return render(request, 'team.html', {'fnsuser':fnsuser, 'teams':teams, 'message':message,
        'notificationList':notificationList,'countNotification':countNotification})

    teamMatching = TeamMatching.objects.all().filter(is_applied=True, vs_team = team)
    return render(request, 'suggestList.html', {'fnsuser':fnsuser, 'teamMatching':teamMatching,
    'notificationList':notificationList,'countNotification':countNotification})

def suggestDetail(request, teamMatching_id):
    fnsuser = get_object_or_404(FNSUser, pk = request.session.get('userId'))
    teamMatching = get_object_or_404(TeamMatching, pk = teamMatching_id)
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')[:20]
    # 객체를 한 페이지로 자르기
    paginator = Paginator(notification, 5)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    notificationList = paginator.get_page(page)
    teams = Team.objects.all()
    if(fnsuser.teamname != teamMatching.vs_team):
        message = '팀원만 확인할 수 있습니다.'
        return render(request, 'team.html', {'fnsuser':fnsuser, 'teams':team, 'message':message,
        'notificationList':notificationList,'countNotification':countNotification})

    return render(request, 'suggestDetail.html', {'fnsuser':fnsuser, 'teamMatching':teamMatching,
    'notificationList':notificationList,'countNotification':countNotification})

def acceptSuggest(request, teamMatching_id):
    fnsuser = get_object_or_404(FNSUser, pk = request.session.get('userId'))
    teamMatching = get_object_or_404(TeamMatching, pk = teamMatching_id)
    teamMatching.is_applied = False
    teamMatching.save()
    decidedMatch = DecidedMatch()
    decidedMatch.myTeam = teamMatching.myteam
    decidedMatch.vsTeam = teamMatching.vs_team
    decidedMatch.location = teamMatching.location
    decidedMatch.timeFrom = teamMatching.time_from
    decidedMatch.timeTo = teamMatching.time_to
    decidedMatch.match = teamMatching
    decidedMatch.save()
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    teams = Team.objects.all()
    

  
    newNotification = Notification.objects.create(
        creator = get_object_or_404(FNSUser, pk=request.session.get('userId')),
        to = teamMatching.user,
        teamMatching = teamMatching,
        notification_type = Notification.acceptSuggestion,
        team = fnsuser.teamname,
    )
    newNotification.acceptSuggestionText()
    newNotification.save()
    teamMatching = TeamMatching.objects.all().filter(is_applied=True, vs_team = fnsuser.teamname)

    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')[:20]
    # 객체를 한 페이지로 자르기
    paginator = Paginator(notification, 5)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    notificationList = paginator.get_page(page)
    return render(request, 'suggestList.html', {'fnsuser':fnsuser, 'teamMatching':teamMatching,
    'notificationList':notificationList,'countNotification':countNotification})

def denySuggest(request, teamMatching_id):
    fnsuser = get_object_or_404(FNSUser, pk = request.session.get('userId'))
    teamMatching = get_object_or_404(TeamMatching, pk = teamMatching_id)
    teamMatching.delete()
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    teams = Team.objects.all()
    # 객체를 한 페이지로 자르기
    paginator = Paginator(notification, 5)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    notificationList = paginator.get_page(page)
    return render(request, 'team.html', {'countNotification':countNotification, 'notificationList':notificationList, 'fnsuser':fnsuser, 'teams' : teams})

def editForm(request, team_id):
    fnsuser = get_object_or_404(FNSUser, pk = request.session.get('userId'))
    team = get_object_or_404(Team, pk = team_id)
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    return render(request, 'editForm.html', {'countNotification':countNotification, 'notificationList':notificationList, 'fnsuser':fnsuser, 'team' : team})

def update(request):
    team = get_object_or_404(Team, pk=team_id)
    team.name = request.POST.get('name')
    team.introduction = request.POST.get('introduction')
    team.region = request.POST.get('region')
    team.city = request.POST.get('city')
    team.school = request.POST.get('school')
    team.save()
    teams = Team.objects.all()
    fnsuser = get_object_or_404(FNSUser, pk = request.session.get('userId'))
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    return render(request, 'team.html', {'countNotification':countNotification, 
    'teams':teams, 'notificationList':notificationList, 'fnsuser':fnsuser, 'team' : team})

    return redirect('/team/')

