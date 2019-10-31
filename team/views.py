from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.exceptions import ObjectDoesNotExist
from .models import Team
from account.models import FNSUser
from notification.models import Notification

# Create your views here.

def team(request):
    teams = Team.objects.all().order_by('rank')
    if not request.session.get('userId'):
        errormessage = '로그인을 해주세요.'
        return render(request, 'login.html', {'errormessage':errormessage})
    


    fnsuser = get_object_or_404(FNSUser, pk=request.session.get('userId'))
    notification = fnsuser.to.all().order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    return render(request, 'team.html', {'countNotification':countNotification, 'notification':notification, 'fnsuser':fnsuser, 'teams' : teams})

def detail(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    members = team.member.all()
    is_member = team.member.filter(pk=request.session.get('userId')).exists()
    fnsuser = get_object_or_404(FNSUser, pk=request.session.get('userId'))
    notification = fnsuser.to.all().order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    return render(request, 'detail.html', {'notification':notification, 'fnsuser':fnsuser, 
    'countNotification':countNotification, 'team': team, 'members': members, 'is_member':is_member})

def new(request):
    userId = request.session.get('userId')
    teams = Team.objects
    fnsuser = get_object_or_404(FNSUser, pk=request.session.get('userId'))
    notification = fnsuser.to.all().order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    if not (userId):
        error = '로그인을 해야 팀을 생성할 수 있습니다.'
        return render(request, 'team.html', {'notification':notification, 'fnsuser':fnsuser, 
        'countNotification':countNotification, 'error':error, 'teams' : teams})
    
    fnsuser = get_object_or_404(FNSUser, pk=request.session.get('userId'))
    try:
        if fnsuser.captain:
            error = '한 사람이 여러 개의 팀을 만들 수 없습니다.'
            teams = Team.objects
            return render(request, 'team.html', {'notification':notification, 'fnsuser':fnsuser, 
            'countNotification':countNotification, 'error':error, 'teams' : teams})

    except ObjectDoesNotExist:
        pass

    return render(request, 'new.html', {'countNotification':countNotification, 'notification':notification, 'fnsuser':fnsuser})

def create(request):
    team = Team()
    team.teamimg = request.FILES['teamimg']
    team.name = request.POST.get('name')
    team.introduction = request.POST.get('introduction')
    team.region = request.POST.get('region')
    notification = fnsuser.to.all().order_by('-created')
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
    fnsuser = get_object_or_404(FNSUser, pk = request.session.get('userId'))
    fnsuser.teamname = team
    fnsuser.save()
    return redirect('/team/')

def update(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    team.name = request.GET['name']
    team.region = request.GET['region']
    team.city = request.GET['city']
    team.school = request.GET['school']
    team.save()
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
    notification = fnsuser.to.all().order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    is_member = members.filter(pk=pk).exists()
    if is_member:
        message = '이미 팀 회원이십니다.'
        return render(request, 'detail.html', {'notification':notification, 'fnsuser':fnsuser, 
        'countNotification':countNotification, 'team': team, 'members': members, 'message':message })

    is_othermember = fnsuser.teamname
    if is_othermember:
        message = '이미 다른 팀에 가입하셨습니다.'
        return render(request, 'detail.html', {'notification':notification, 'fnsuser':fnsuser, 
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
    
    return render(request, 'detail.html', {'notification':notification, 'fnsuser':fnsuser, 
    'countNotification':countNotification, 'team': team, 'members': members, 'message':message })
    

def applied_list(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    pk = request.session.get('userId')
    fnsuser = get_object_or_404(FNSUser, pk=pk)
    notification = fnsuser.to.all().order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    members = team.member.all()
    applied_members = team.applied_member.all()
    message = ''
    if team.teamleader != fnsuser:
        message = '팀대표만 참가신청현황을 볼 수 있습니다.'
        return render(request, 'detail.html', {'notification':notification, 'fnsuser':fnsuser, 
        'countNotification':countNotification, 'team': team, 'members': members, 'message':message })

    else:
        return render(request, 'applied_list.html', {'notification':notification, 'fnsuser':fnsuser, 
        'countNotification':countNotification, 'team': team, 'applied_members': applied_members, 'message':message })

def approve(request, team_id, fnsuser_id):
    team = get_object_or_404(Team, pk=team_id)
    fnsuser1 = get_object_or_404(FNSUser, pk=fnsuser_id)
    fnsuser = get_object_or_404(FNSUser, pk=request.session.get('userId'))
    notification = fnsuser.to.all().order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    team.applied_member.remove(fnsuser1)
    team.save()
    members = team.member.all()
    fnsuser1.teamname = team
    fnsuser1.save()
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

    return render(request, 'applied_list.html', {'countNotification':countNotification, 'notification':notification, 'fnsuser':fnsuser, 
    'message':message, 'applied_members':applied_members, 'team':team})

def dropout(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    fnsuser = get_object_or_404(FNSUser, pk=request.session.get('userId'))
    notification = fnsuser.to.all().order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    team.applied_member.remove(fnsuser)
    team.save()
    fnsuser.teamname = None
    fnsuser.save()
    members = team.member.all()
    is_member = team.member.filter(pk=request.session.get('userId')).exists()
    message = '성공적으로 팀탈퇴가 되었습니다.'

    return render(request, 'detail.html', {'countNotification':countNotification, 'notification':notification, 'fnsuser':fnsuser, 
    'team': team, 'members':members, 'is_member':is_member, 'message':message})

def searchTeam(request):
    fnsuser = get_object_or_404(FNSUser, pk=request.session.get('userId'))
    notification = fnsuser.to.all().order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
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


    return render(request, 'team.html', {'countNotification':countNotification, 'notification':notification, 'fnsuser':fnsuser, 
    'teams':teams, 'count':count})