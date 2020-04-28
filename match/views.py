from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import PersonalMatching, TeamMatching, Recruiting, PersonalComment, PersonalReply, TMComment, REComment, League, LGComment, LgPlayerAttendance, LgTeamAttendance, TmAppliedTeam
from .models import TeamReply, RecruitingReply, LeagueReply
from django.views.decorators.http import require_POST
from account.models import FNSUser
from decidedMatch.models import DecidedMatch
from team.models import Team
from notification.models import Notification
from reservation.models import ReservationList
from django.core.paginator import Paginator
from datetime import datetime, date, timedelta
from django.utils.dateformat import DateFormat
from django.core import serializers
from reservation.models import PlaygroundList, ReservationList
import json, logging

# Create your views here.
def home(request):
    today = date.today()
    personalMatching = PersonalMatching.objects.filter(time_from__gt = today).order_by('-time_from')
    teamMatching = TeamMatching.objects.filter(time_from__gt = today, isApplied=False).order_by('-time_from')
    recruiting = Recruiting.objects.filter(time_from__gt = today).order_by('-time_from')
    league = League.objects.all().order_by('-time_from')
    personal_notice = PersonalMatching.objects.order_by('-created').first()
    user_id = request.session.get('userId')

    # 자동로그인 쿠키가 있는 경우 자동로그인
    if request.COOKIES.get('username') != None:
        username = request.COOKIES.get('username')
        fnsuser = get_object_or_404(FNSUser, username = username)
        sessionId = request.COOKIES.get('sessionId')
        
        if sessionId == fnsuser.sessionId:
            request.session['userId'] = fnsuser.id
            request.session['name'] = fnsuser.name
            notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
            countNotification = notification.filter(userCheck=False).count()
            return render(request, 'home.html', {'fnsuser':fnsuser, 'notification':notification,'countNotification':countNotification})
            

    if user_id:
        fnsuser = FNSUser.objects.get(pk=user_id)
        notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
        countNotification = notification.filter(userCheck = False).count()
        notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')[:20]
        # 객체를 한 페이지로 자르기
        paginator = Paginator(notification, 5)
        # request에 담아주기
        page = request.GET.get('page')
        # request된 페이지를 얻어온 뒤 return 해 준다.
        notificationList = paginator.get_page(page)
        return render(request, 'home.html', {'personal_notice':personal_notice, 'countNotification':countNotification, 'league':league, 
        'personalMatching':personalMatching, 'teamMatching':teamMatching, 'recruiting':recruiting, 'name':fnsuser.name, 'fnsuser':fnsuser, 'notificationList':notificationList, 'countNotification':countNotification})
    return render(request, 'home.html', {'personal_notice':personal_notice, 'league':league, 'personalMatching':personalMatching, 'teamMatching':teamMatching, 'recruiting':recruiting})

def about(request):
    if not request.session.get('userId'):
        return render(request, 'about.html')
    else:
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
        return render(request, 'about.html', {'countNotification':countNotification, 'notificationList':notificationList, 'fnsuser':fnsuser})

def play(request):
    if not request.session.get('userId'):
        return render(request, 'play.html')
    else:
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
            'fnsuser' : fnsuser,
            'notificationList' : notificationList,
            'countNotification' : countNotification,
        }
        
        return render(request, 'play.html', data)

def personal(request):
    today = date.today()
    month = today.month
    day = today.day
    if not request.session.get('userId'):
        personal = PersonalMatching.objects.all().filter(region = '충청남도', city = '천안시',
        time_from__month = today.month, time_from__day = today.day).order_by('time_from')
        # 객체를 한 페이지로 자르기
        paginator = Paginator(personal, 8)
        # request에 담아주기
        page = request.GET.get('page')
        # request된 페이지를 얻어온 뒤 return 해 준다.
        personalList = paginator.get_page(page)

        data = {
            'personalList': personalList,
            'personal':personal,
            'today':today,
            'month':month,
            'day':day
        }
        return render(request, 'personalMatching/personal.html', data)
    else:
        fnsuser = get_object_or_404(FNSUser, pk = request.session.get('userId'))
        personal = PersonalMatching.objects.all().filter(region = fnsuser.region, city = fnsuser.city,
        time_from__month = today.month, time_from__day = today.day).order_by('time_from')
        # 객체를 한 페이지로 자르기
        paginator = Paginator(personal, 8)
        # request에 담아주기
        page = request.GET.get('page')
        # request된 페이지를 얻어온 뒤 return 해 준다.
        personalList = paginator.get_page(page)

        
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
            'month':month,
            'day':day,
            'countNotification':countNotification, 
            'personal':personal, 
            'personalList':personalList, 
            'notificationList':notificationList, 
            'fnsuser':fnsuser, 
            'today':today
        }
        return render(request, 'personalMatching/personal.html', data)

def personalDay(request):
    today = datetime.today()
    month = request.GET.get('month')
    # month = int(month) + 1
    day = request.GET.get('day')
    region = request.GET.get('region')

    if request.GET.get('seoul') != None:
        city = request.GET.get('seoul')
    
    elif request.GET.get('gyeonggi') != None:
        city = request.GET.get('gyeonggi')

    elif request.GET.get('north_chungcheong') != None:
        city = request.GET.get('north_chungcheong')
    
    elif request.GET.get('south_chungcheong') != None:
        city = request.GET.get('south_chungcheong')
    
    elif request.GET.get('north_jeolla') != None:
        city = request.GET.get('north_jeolla')

    elif request.GET.get('south_jeolla') != None:
        city = request.GET.get('south_jeolla')

    elif request.GET.get('north_gyeongsang') != None:
        city = request.GET.get('north_gyeongsang')

    elif request.GET.get('south_gyeongsang') != None:
        city = request.GET.get('south_gyeongsang')

    elif request.GET.get('jeju') != None:
        city = request.GET.get('jeju')

    elif request.GET.get('incheon') != None:
        city = request.GET.get('incheon')

    elif request.GET.get('daejeon') != None:
        city = request.GET.get('daejeon')
    
    elif request.GET.get('gwangju') != None:
        city = request.GET.get('gwangju')

    elif request.GET.get('daegu') != None:
        city = request.GET.get('daegu')

    elif request.GET.get('ulsan') != None:
        city = request.GET.get('ulsan')

    elif request.GET.get('busan') != None:
        city = request.GET.get('busan')

    elif request.GET.get('sejong') != None:
        city = request.GET.get('sejong')

    elif request.GET.get('gangwon') != None:
        city = request.GET.get('gangwon')

    personal = PersonalMatching.objects.all().filter(region=region, city=city,
        time_from__month = int(month) + 1, time_from__day = day
    ).order_by('time_from')
    # 객체를 한 페이지로 자르기
    paginator = Paginator(personal, 8)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    personalList = paginator.get_page(page)

    if request.session.get('userId'):
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
            'personal':personal,
            'personalList':personalList,
            'month' : month,
            'day' : day,
            'today':today,
            'fnsuser':fnsuser,
            'notificationList':notificationList,
            'countNotification':countNotification,
            'region':region,
            'city':city
        }
        return render(request, 'personalMatching/personal.html', data)

    data = {
        'personal':personal,
        'personalList':personalList,
        'month' : month,
        'day' : day,
        'today':today,
        'region':region,
        'city':city
    }
    return render(request, 'personalMatching/personal.html', data)

def pCheckReservation(request):
    if not (request.session.get('userId')):
        errormessage = '로그인을 해주세요.'
        data = {
            'errormessage' : errormessage
        }
        return render(request, 'login.html', data)

    else:
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
            'fnsuser': fnsuser,
            'notification': notification,
            'countNotification':countNotification,
            'notificationList':notificationList
        }
        return render(request, 'personalMatching/pCheckReservation.html', data)

def pIsReserved(request):
    if not (request.session.get('userId')):
        errormessage = '로그인을 해주세요.'
        data = {
            'errormessage' : errormessage
        }
        return render(request, 'login.html', data)

    else:
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
            'fnsuser': fnsuser,
            'notification': notification,
            'countNotification':countNotification,
            'notificationList':notificationList
        }
        return render(request, 'personalMatching/pIsReserved.html', data)

def personalDetail(request, personal_id):
    if not (request.session.get('userId')):
        errormessage = '로그인을 해주세요.'
        return render(request, 'login.html', {'errormessage':errormessage})

    fnsuser = get_object_or_404(FNSUser, pk = request.session.get('userId'))
    personalMatching = get_object_or_404(PersonalMatching, pk = personal_id)
    comments = PersonalComment.objects.filter(post = personalMatching.id).order_by('-created')
    # 객체를 한 페이지로 자르기
    commentPaginator = Paginator(comments, 15)
    # request에 담아주기
    commentPage = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    commentList = commentPaginator.get_page(commentPage)


    attendedPlayer = personalMatching.attendedPlayer.all()
    appliedPlayer = personalMatching.appliedPlayer.all()
    isApplied = personalMatching.appliedPlayer.filter(pk = fnsuser.id ).exists()
    isAttended = personalMatching.attendedPlayer.filter(pk = fnsuser.id).exists()

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
        'countNotification':countNotification, 
        'notificationList':notificationList, 
        'fnsuser':fnsuser, 
        'personalMatching':personalMatching, 
        'isApplied':isApplied,
        'isAttended':isAttended
    }
    return render(request, 'personalMatching/personalDetail.html', data)

def personalComment(request, personalId):
    if not (request.session.get('userId')):
        errormessage = '로그인을 해주세요.'
        return render(request, 'login.html', {'errormessage':errormessage})

    fnsuser = get_object_or_404(FNSUser, pk = request.session.get('userId'))
    personalMatching = get_object_or_404(PersonalMatching, pk = personalId)
    comments = PersonalComment.objects.filter(post = personalMatching.id).order_by('-created')
    # 객체를 한 페이지로 자르기
    commentPaginator = Paginator(comments, 15)
    # request에 담아주기
    commentPage = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    commentList = commentPaginator.get_page(commentPage)

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
        'countNotification':countNotification, 
        'notificationList':notificationList, 
        'fnsuser':fnsuser, 
        'personalMatching':personalMatching, 
        'comments':comments,
        'commentList':commentList
    }
    return render(request, 'personalMatching/personalComment.html', data)

@require_POST
def personalcm_write(request):
    errormessage = None
    if request.method == 'POST':
        fnsuser = get_object_or_404(FNSUser, pk = request.session.get('userId'))    
        personalMatching_id = request.POST.get('personalMatching_id', '').strip()
        personalMatching = get_object_or_404(PersonalMatching, pk=personalMatching_id)
        content = request.POST.get('content', '').strip()

        if not content: 
            errormessage = '댓글을 입력해주세요.'

        if not errormessage:
            comment = PersonalComment.objects.create(user=fnsuser, post_id= personalMatching_id, content= content)

            newNotification = Notification.objects.create(
            creator = get_object_or_404(FNSUser, pk=request.session.get('userId')),
            to = personalMatching.user,
            notification_type = Notification.prComment,
            personalMatching = personalMatching
            )
           
            newNotification.personalCommentText()
            newNotification.save()
            # return redirect(reverse('personalDetail', kwargs={'personal_id':personalMatching_id}))

    comments = PersonalComment.objects.filter(post = personalMatching.id).order_by('-created')
    # 객체를 한 페이지로 자르기
    commentPaginator = Paginator(comments, 15)
    # request에 담아주기
    commentPage = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    commentList = commentPaginator.get_page(commentPage)
    

    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')[:20]
    # 객체를 한 페이지로 자르기
    paginator = Paginator(notification, 5)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    notificationList = paginator.get_page(page)

    return render(request, 'personalMatching/personalComment.html', {'countNotification':countNotification, 
    'notificationList':notificationList, 'errormessage':errormessage, 'fnsuser':fnsuser, 'commentList':commentList, 'personalMatching':personalMatching})

def deletePC(request, personalComment_id):
    personalComment = get_object_or_404(PersonalComment, pk=personalComment_id)
    personalMatching = personalComment.post
    personalComment.delete()

    fnsuser = get_object_or_404(FNSUser, pk = request.session.get('userId'))
    comments = PersonalComment.objects.filter(post = personalMatching.id).order_by('-created')
    # 객체를 한 페이지로 자르기
    commentPaginator = Paginator(comments, 15)
    # request에 담아주기
    commentPage = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    commentList = commentPaginator.get_page(commentPage)

    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')[:20]
    # 객체를 한 페이지로 자르기
    paginator = Paginator(notification, 5)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    notificationList = paginator.get_page(page)
    return render(request, 'personalMatching/personalComment.html', {'countNotification':countNotification, 
    'notificationList':notificationList, 'fnsuser':fnsuser, 'commentList':commentList, 'personalMatching':personalMatching})

def editPC(request, personalComment_id):
    errormessage = None
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
    content = request.POST.get('content')
    personalComment = get_object_or_404(PersonalComment, pk = personalComment_id)

    if not content:
        errormessage = '내용을 입력해주세요.'

    if not errormessage:
        personalComment.content = content
        personalComment.save()
    
    personalMatching = personalComment.post
    comments = PersonalComment.objects.filter(post = personalMatching.id).order_by('-created')
    # 객체를 한 페이지로 자르기
    commentPaginator = Paginator(comments, 15)
    # request에 담아주기
    commentPage = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    commentList = commentPaginator.get_page(commentPage)
    return render(request, 'personalMatching/personalComment.html', {'personalMatching':personalMatching, 'errormessage':errormessage,
    'commentList':commentList, 'countNotification':countNotification, 'notificationList':notificationList, 'fnsuser':fnsuser})

def personalReply_write(request):
    errormessage = None
    if request.method == 'POST':
        fnsuser = get_object_or_404(FNSUser, pk = request.session.get('userId'))    
        personalMatching_id = request.POST.get('personalMatching_id', '').strip()
        personalMatching = get_object_or_404(PersonalMatching, pk=personalMatching_id)
        comment_id = request.POST.get('comment_id')
        personalComment = get_object_or_404(PersonalComment, pk = comment_id)

        comments = PersonalComment.objects.filter(post = personalMatching.id).order_by('-created')
        # 객체를 한 페이지로 자르기
        commentPaginator = Paginator(comments, 15)
        # request에 담아주기
        commentPage = request.GET.get('page')
        # request된 페이지를 얻어온 뒤 return 해 준다.
        commentList = commentPaginator.get_page(commentPage)
        content = request.POST.get('content', '').strip()

        if not content:
            errormessage = '답글을 입력해주세요.'

        if not errormessage:
            commentReply = PersonalReply.objects.create(user=fnsuser, post= personalMatching, 
            content= content, comment=personalComment)

            newNotification = Notification.objects.create(
            creator = get_object_or_404(FNSUser, pk=request.session.get('userId')),
            to = personalComment.user,
            notification_type = Notification.personalReply,
            personalMatching = personalMatching,
            personalComment = personalComment
            )
           
            newNotification.personalReplyText()
            newNotification.save()
            # return redirect(reverse('personalDetail', kwargs={'personal_id':personalMatching_id}))

    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')[:20]
    # 객체를 한 페이지로 자르기
    paginator = Paginator(notification, 5)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    notificationList = paginator.get_page(page)

    return render(request, 'personalMatching/personalComment.html', {'countNotification':countNotification, 
    'notificationList':notificationList, 'errormessage':errormessage, 'fnsuser':fnsuser, 'commentList':commentList, 'personalMatching':personalMatching})

def deletePersonalReply(request, reply_id):
    personalReply = get_object_or_404(PersonalReply, pk=reply_id)
    personalMatching = personalReply.post
    personalReply.delete()

    fnsuser = get_object_or_404(FNSUser, pk = request.session.get('userId'))
    comments = PersonalComment.objects.filter(post = personalMatching.id).order_by('-created')
    # 객체를 한 페이지로 자르기
    commentPaginator = Paginator(comments, 15)
    # request에 담아주기
    commentPage = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    commentList = commentPaginator.get_page(commentPage)

    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')[:20]
    # 객체를 한 페이지로 자르기
    paginator = Paginator(notification, 5)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    notificationList = paginator.get_page(page)
    return render(request, 'personalMatching/personalComment.html', {'countNotification':countNotification, 
    'notificationList':notificationList, 'fnsuser':fnsuser, 'commentList':commentList, 'personalMatching':personalMatching})

def editPersonalReply(request, reply_id):
    errormessage = None
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
    content = request.POST.get('content')
    personalReply = get_object_or_404(PersonalReply, pk = reply_id)

    if not content:
        errormessage = '내용을 입력해주세요.'

    if not errormessage:
        personalReply.content = content
        personalReply.save()

    personalMatching = personalReply.post
    comments = PersonalComment.objects.filter(post = personalMatching.id).order_by('-created')
    # 객체를 한 페이지로 자르기
    commentPaginator = Paginator(comments, 15)
    # request에 담아주기
    commentPage = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    commentList = commentPaginator.get_page(commentPage)
    return render(request, 'personalMatching/personalComment.html', {'personalMatching':personalMatching, 'errormessage':errormessage,
    'commentList':commentList, 'countNotification':countNotification, 'notificationList':notificationList, 'fnsuser':fnsuser})



def personalNew(request):
    if not (request.session.get('userId')):
        errormessage = '로그인을 해주세요.'
        return render(request, 'login.html', {'errormessage':errormessage})
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

    # 구장목록
    possiblePlayground = PlaygroundList.objects.filter(possibleReservation = True).all()
    impossiblePlayground = PlaygroundList.objects.filter(possibleReservation = False).all()

    data = {
        'possiblePlayground':possiblePlayground,
        'impossiblePlayground':impossiblePlayground,
        'countNotification':countNotification, 
        'notificationList':notificationList, 
        'fnsuser':fnsuser
    }
    return render(request, 'personalMatching/personalNew.html', data)

def selectCity(request):
    city = request.GET.get('city');
    possibleList = PlaygroundList.objects.filter(city = city, possibleReservation=True).all()
    impossibleList = PlaygroundList.objects.filter(city = city, possibleReservation=False).all()
    possibleGround = {}
    impossibleGround = {}
    i = 0
    for ground in possibleList:
        playground = [ground.id, ground.playgroundName]
        possibleGround[i] = playground
        i += 1 

    i = 0
    for ground in impossibleList:
        playground = [ground.id, ground.playgroundName]
        impossibleGround[i] = playground
        i += 1 

    data = {'possibleGround':possibleGround, 'impossibleGround':impossibleGround}
    json_data = json.dumps(data)
    return JsonResponse(json_data, safe=False)


def personalCreate(request):
    fnsuser = get_object_or_404(FNSUser, pk = request.session.get('userId'))
    personalMatching =  PersonalMatching()
    personalMatching.sport = request.POST.get('sport')
    personalMatching.content = request.POST.get('content')
    personalMatching.region = request.POST.get('region')

    if request.POST.get('seoul') != None:
        city = request.POST.get('seoul')
    
    elif request.POST.get('gyeonggi') != None:
        city = request.POST.get('gyeonggi')

    elif request.POST.get('north_chungcheong') != None:
        city = request.POST.get('north_chungcheong')
    
    elif request.POST.get('south_chungcheong') != None:
        city = request.POST.get('south_chungcheong')
    
    elif request.POST.get('north_jeolla') != None:
        city = request.POST.get('north_jeolla')

    elif request.POST.get('south_jeolla') != None:
        city = request.POST.get('south_jeolla')

    elif request.POST.get('north_gyeongsang') != None:
        city = request.POST.get('north_gyeongsang')

    elif request.POST.get('south_gyeongsang') != None:
        city = request.POST.get('south_gyeongsang')

    elif request.POST.get('jeju') != None:
        city = request.POST.get('jeju')

    elif request.POST.get('incheon') != None:
        city = request.POST.get('incheon')

    elif request.POST.get('daejeon') != None:
        city = request.POST.get('daejeon')
    
    elif request.POST.get('gwangju') != None:
        city = request.POST.get('gwangju')

    elif request.POST.get('daegu') != None:
        city = request.POST.get('daegu')

    elif request.POST.get('ulsan') != None:
        city = request.POST.get('ulsan')

    elif request.POST.get('busan') != None:
        city = request.POST.get('busan')

    elif request.POST.get('sejong') != None:
        city = request.POST.get('sejong')

    elif request.POST.get('gangwon') != None:
        city = request.POST.get('gangwon')

    personalMatching.city = city
    location = request.POST.get('location')
    if location == 'playground':
        personalMatching.location = None
    else:
        ground = location.split(",")
        playgroundList = get_object_or_404(PlaygroundList, pk = ground[0])
        personalMatching.location = playgroundList
    playDate = request.POST.get('playDate')
    playTime = request.POST.get('playTime')
    timeValue = playTime.split(',')
    smallNum = 0;
    largeNum = 0;
    reservationTimeArray = []
    for i in timeValue:
        reservationTimeArray.append(i)
        if smallNum is 0 and largeNum is 0:
            smallNum = int(i)
            largeNum = int(i)

        elif int(i) > largeNum:
            smallNum = largeNum
            largeNum = int(i)
            
        elif (int(i) < largeNum):
            if int(i) < smallNum:
                smallNum = int(i)
            
        

    year = playDate[0:4]
    month = playDate[6:8]
    date = playDate[10:12]
    if smallNum < 10:
        smallNum = '0' + str(smallNum)
    hour = str(smallNum)
    startDay = datetime(int(year), int(month), int(date))
    if int(hour) is 24:
        hour = '00'
        changedDate = startDay + timedelta(days=1)
        startMonth = changedDate.strftime('%m')
        startDate = changedDate.strftime('%d')
        startTime = year + '-' + startMonth + '-' + startDate + ' ' + hour + ':' + '00'
    else:
        startTime = year + '-' + month + '-' + date + ' ' + hour + ':' + '00'

    personalMatching.time_from = startTime
    

    if largeNum < 9:
        largeNum = '0' + str(largeNum+1)
    else:
        largeNum = int(largeNum) + 1
    endHour = str(largeNum)
    endMin = '00'
    day = datetime(int(year), int(month), int(date))
    if int(endHour) is 24 or int(endHour) is 25:
        if int(endHour) is 24:
            endHour = '00'
        elif int(endHour) is 25:
            endHour = '01'

        changedDate = day + timedelta(days=1)
        month = changedDate.strftime('%m')
        date = changedDate.strftime('%d')


    endTime = year + '-' + month + '-' + date + ' ' + endHour + ':' + endMin
    personalMatching.time_to = endTime
    personalMatching.number = request.POST.get('number')
    personalMatching.joinFee = request.POST.get('joinFee')
    personalMatching.content = request.POST.get('content')
    user_id = request.session.get('userId')
    fnsUser = get_object_or_404(FNSUser, pk = user_id)
    personalMatching.user = fnsUser

    # check 예약 있는지 없는지
    for idx, reservation in enumerate(reservationTimeArray):
        if personalMatching.location != None:
            reservationDate = str(year) + str(month) + str(date)
            #if int(reservationTimeArray[idx]) < 10:
            #    reservationTimeArray[idx] = '0' + str(reservationTimeArray[idx])
            reservationTime = str(reservationTimeArray[idx]) + "00"
            
            if playgroundList.reservation.filter(user = fnsuser, playgroundName = playgroundList, 
            reservationDate = reservationDate, reservationTime = reservationTime, 
            reservationUserName = fnsuser.name, resercationUserPhone = fnsuser.phone_number).exists():
                error = '작성한 시간대는 이미 예약되어 있습니다.'
                data = {
                    'error':error
                }
                return render(request, 'personalMatching/personalNew.html', data)
    
    for idx, reservation in enumerate(reservationTimeArray):
        if personalMatching.location != None:
            reservationDate = str(year) + str(month) + str(date)
            #if int(reservationTimeArray[idx]) < 10:
            #    reservationTimeArray[idx] = '0' + str(reservationTimeArray[idx])
            reservationTime = str(reservationTimeArray[idx]) + "00"
            newReservation = ReservationList(user = fnsuser, playgroundName = playgroundList, 
            reservationDate = reservationDate, reservationTime = reservationTime, 
            resercationUserId = "moonlit0130", reservationUserName = fnsuser.name, 
            resercationUserPhone = fnsuser.phone_number)
            newReservation.save()

    
    personalMatching.save()
    return redirect(reverse('personal'))

def personalResult(request, personalId):
    if not (request.session.get('userId')):
        errormessage = '로그인을 해주세요.'
        return render(request, 'login.html', {'errormessage':errormessage})

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

    personalMatching = get_object_or_404(PersonalMatching, pk = personalId)

    isAttended = personalMatching.attendedPlayer.filter(pk = request.session.get('userId')).exists()

    comments = PersonalComment.objects.filter(post = personalMatching.id).order_by('-created')
    # 객체를 한 페이지로 자르기
    commentPaginator = Paginator(comments, 15)
    # request에 담아주기
    commentPage = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    commentList = commentPaginator.get_page(commentPage)

    #만약 글 게시자가 신청 눌렀을 시
    if (fnsuser == personalMatching.user):
        error = "글 작성자는 신청을 못합니다."
        data = {
            'personalMatching':personalMatching, 
            'isApplied': isApplied, 
            'total_attendance': personalMatching.total_attendance(), 
            'error':error, 
            'isAttended':isAttended,
            'commentList':commentList,
            'countNotification':countNotification, 
            'notificationList':notificationList, 
            'fnsuser':fnsuser,
        }

        return render(request, 'personalMatching/personalDetail.html', data)

    elif (personalMatching.attendedPlayer.filter(pk = request.session.get('userId')).exists()):
        error = "이미 참가 확정 중입니다."
        data = {
            'personalMatching':personalMatching, 
            'isApplied': isApplied, 
            'isAttended':isAttended,
            'total_attendance': personalMatching.total_attendance(), 
            'error':error, 
            'commentList':commentList,
            'countNotification':countNotification, 
            'notificationList':notificationList, 
            'fnsuser':fnsuser,
        }

        return render(request, 'personalMatching/personalDetail.html', data)

    if isApplied:
        personalMatching.appliedPlayer.remove(fnsuser)
        isApplied = False
        alarm = '참가신청이 취소되었습니다.'
    
    
    elif personalMatching.number <= personalMatching.total_attendance():
        error = '모집인원이 다 모아져서 참가신청이 안됩니다.'
        data = {
            'personalMatching':personalMatching, 
            'isApplied': isApplied, 
            'isAttended':isAttended,
            'total_attendance': personalMatching.total_attendance(), 
            'error':error, 
            'commentList':commentList,
            'countNotification':countNotification, 
            'notificationList':notificationList, 
            'fnsuser':fnsuser,
        }

        return render(request, 'personalMatching/personalDetail.html', data)
    
    else:    
        personalMatching.appliedPlayer.add(fnsuser)
        isApplied = True
        alarm = '참가신청이 완료되었습니다.'
        newNotification = Notification.objects.create(
            creator = fnsuser,
            to = personalMatching.user,
            notification_type = Notification.personalApply,
            personalMatching = personalMatching
        )

        newNotification.personalApplyText()
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

    data = {
        'personalMatching':personalMatching, 
        'isApplied': isApplied, 
        'isAttended':isAttended,
        'total_attendance': personalMatching.total_attendance(), 
        'commentList':commentList,
        'countNotification':countNotification, 
        'notificationList':notificationList, 
        'fnsuser':fnsuser,
        'alarm':alarm,
    }
    return render(request, 'personalMatching/personalDetail.html', data)
    message = request.POST.get('message', none)
    data = {
        'message': message
    }
    return render(request, 'personalDetail.html', data)

def personalEdit(request, personalId):
    if not (request.session.get('userId')):
        errormessage = '로그인을 해주세요.'
        return render(request, 'login.html', {'errormessage':errormessage})

    if request.method == 'GET':
        personalMatching = get_object_or_404(PersonalMatching, pk = personalId)
        userId = request.session.get('userId')
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

        if(userId != personalMatching.user.id):
            personal = PersonalMatching.objects.all().filter(region = fnsuser.region, city = fnsuser.city,
            time_from__month = today.month, time_from__day = today.day).order_by('time_from')
            # 객체를 한 페이지로 자르기
            paginator = Paginator(personal, 10)
            # request에 담아주기
            page = request.GET.get('page')
            # request된 페이지를 얻어온 뒤 return 해 준다.
            personalList = paginator.get_page(page)
            error = '글을 작성한 사용자만 수정할 수 있습니다.'
            data = {
                'countNotification':countNotification, 
                'notificationList':notificationList, 
                'fnsuser':fnsuser, 
                'personal': personal,
                'personalList':personalList, 
                'error':error
            }
            return render(request, 'personalMatching/personal.html', data)

        else:
            data = {
                'countNotification':countNotification, 
                'notificationList':notificationList, 
                'fnsuser':fnsuser, 
                'personalMatching':personalMatching
            }
            return render(request, 'personalMatching/personalEdit.html', data)

    # 글 수정하기
    elif request.method == 'POST':
        fnsuser = get_object_or_404(FNSUser, pk = request.session.get('userId'))
        personalMatching =  get_object_or_404(PersonalMatching, pk = personalId)

        # 이전 시간 구장 및 시간(예약삭제용)
        preTimeFrom = personalMatching.time_from
        preTimeTo = personalMatching.time_to
        prePlayground = personalMatching.location

        personalMatching.sport = request.POST.get('sport')
        personalMatching.content = request.POST.get('content')
        personalMatching.region = request.POST.get('region')

        if request.POST.get('seoul') != None:
            city = request.POST.get('seoul')
        
        elif request.POST.get('gyeonggi') != None:
            city = request.POST.get('gyeonggi')

        elif request.POST.get('north_chungcheong') != None:
            city = request.POST.get('north_chungcheong')
        
        elif request.POST.get('south_chungcheong') != None:
            city = request.POST.get('south_chungcheong')
        
        elif request.POST.get('north_jeolla') != None:
            city = request.POST.get('north_jeolla')

        elif request.POST.get('south_jeolla') != None:
            city = request.POST.get('south_jeolla')

        elif request.POST.get('north_gyeongsang') != None:
            city = request.POST.get('north_gyeongsang')

        elif request.POST.get('south_gyeongsang') != None:
            city = request.POST.get('south_gyeongsang')

        elif request.POST.get('jeju') != None:
            city = request.POST.get('jeju')

        elif request.POST.get('incheon') != None:
            city = request.POST.get('incheon')

        elif request.POST.get('daejeon') != None:
            city = request.POST.get('daejeon')
        
        elif request.POST.get('gwangju') != None:
            city = request.POST.get('gwangju')

        elif request.POST.get('daegu') != None:
            city = request.POST.get('daegu')

        elif request.POST.get('ulsan') != None:
            city = request.POST.get('ulsan')

        elif request.POST.get('busan') != None:
            city = request.POST.get('busan')

        elif request.POST.get('sejong') != None:
            city = request.POST.get('sejong')

        elif request.POST.get('gangwon') != None:
            city = request.POST.get('gangwon')

        personalMatching.city = city
        location = request.POST.get('location')
        if location == 'playground':
            personalMatching.location = None
        else:
            ground = location.split(",")
            playgroundList = get_object_or_404(PlaygroundList, pk = ground[0])
            personalMatching.location = playgroundList

        playDate = request.POST.get('playDate')
        playTime = request.POST.get('playTime')
        timeValue = playTime.split(',')
        smallNum = 0;
        largeNum = 0;
        reservationTimeArray = []
        for i in timeValue:
            reservationTimeArray.append(int(i))
            if smallNum is 0 and largeNum is 0:
                smallNum = int(i)
                largeNum = int(i)

            elif int(i) > largeNum:
                smallNum = largeNum
                largeNum = int(i)
                
            elif (int(i) < largeNum):
                if int(i) < smallNum:
                    smallNum = int(i)
                
        

            year = playDate[0:4]
            month = playDate[6:8]
            date = playDate[10:12]
            hour = str(smallNum)
            startDay = datetime(int(year), int(month), int(date))
            if int(hour) is 24:
                hour = '00'
                changedDate = startDay + timedelta(days=1)
                startMonth = changedDate.strftime('%m')
                startDate = changedDate.strftime('%d')
                startTime = year + '-' + startMonth + '-' + startDate + ' ' + hour + ':' + '00'
            else:
                startTime = year + '-' + month + '-' + date + ' ' + hour + ':' + '00'

            personalMatching.time_from = startTime
    


            endHour = str(largeNum+1)
            endMin = '00'
            day = datetime(int(year), int(month), int(date))
            if int(endHour) is 24 or int(endHour) is 25:
                if int(endHour) is 24:
                    endHour = '00'
                elif int(endHour) is 25:
                    endHour = '01'

                changedDate = day + timedelta(days=1)
                month = changedDate.strftime('%m')
                date = changedDate.strftime('%d')


            endTime = year + '-' + month + '-' + date + ' ' + endHour + ':' + endMin
            personalMatching.time_to = endTime
            personalMatching.number = request.POST.get('number')
            personalMatching.joinFee = request.POST.get('joinFee')
            personalMatching.content = request.POST.get('content')
            user_id = request.session.get('userId')
            fnsUser = get_object_or_404(FNSUser, pk = user_id)
            personalMatching.user = fnsUser



            preYear = preTimeFrom.strftime("%Y")
            preMonth = preTimeFrom.strftime("%m")
            preDay = preTimeFrom.strftime("%d")
            preReservationDate = str(preYear) + str(preMonth) + str(preDay)
            preStartTime = preTimeFrom.strftime("%H")
            preEndTime = preTimeTo.strftime("%H")
            preReservation = []
            for i in range(int(preEndTime) - int(preStartTime)):
                preReservationTime = str(preStartTime) + '00'
                preReservation.append(preReservationTime)
                preStartTime = int(preStartTime) + 1
                if int(preStartTime) < 10:
                    preStartTime = '0' + str(preStartTime)

            backupObject = []
            for i in preReservation:
                if prePlayground != None:
                    reservation = prePlayground.reservation.filter(reservationTime = i).all()
                    for reList in reservation:
                        preReservation = get_object_or_404(ReservationList, pk= reList.id)
                        if preReservation.reservationTime == i and preReservation.user == fnsuser and preReservation.playgroundName == prePlayground and preReservation.reservationDate == preReservationDate and preReservation.resercationUserId == "moonlit0130" and preReservation.reservationUserName == fnsuser.name and preReservation.resercationUserPhone == fnsuser.phone_number:
                            backupObject.append(preReservation)
                            preReservation.delete()            

            # check 예약 있는지 없는지  
            for idx, reservation in enumerate(reservationTimeArray):
                if personalMatching.location != None:
                    reservationDate = str(year) + str(month) + str(date)
                    if int(reservationTimeArray[idx]) < 10:
                        reservationTimeArray[idx] = '0' + str(reservationTimeArray[idx])
                    reservationTime = str(reservationTimeArray[idx]) + "00"
                    
                    if playgroundList.reservation.filter(user = fnsuser, playgroundName = playgroundList, 
                    reservationDate = reservationDate, reservationTime = reservationTime, 
                    reservationUserName = fnsuser.name, resercationUserPhone = fnsuser.phone_number).exists():
                        error = '작성한 시간대는 이미 예약되어 있습니다.'
                        for i in backupObject:
                            i.save()
                        data = {
                            'error':error,
                            'personalMatching':personalMatching
                        }
                        return render(request, 'personalMatching/personalEdit.html', data)


            for idx, reservation in enumerate(reservationTimeArray):
                if personalMatching.location != None:
                    reservationDate = str(year) + str(month) + str(date)
                    if int(reservationTimeArray[idx]) < 10:
                        reservationTimeArray[idx] = '0' + str(reservationTimeArray[idx])
                    reservationTime = str(reservationTimeArray[idx]) + "00"
                    newReservation = ReservationList(user = fnsuser, playgroundName = playgroundList, 
                    reservationDate = reservationDate, reservationTime = reservationTime, 
                    resercationUserId = "moonlit0130", reservationUserName = fnsuser.name, 
                    resercationUserPhone = fnsuser.phone_number)
                    newReservation.save()

            
            personalMatching.save()
        return redirect(reverse('personal'))
    return render(request, 'personalMatching/personalDetail.html', {'countNotification':countNotification, 'notificationList':notificationList, 'fnsuser':fnsuser, 'personalMatching':personalMatching})


def personalDelete(request, personal_id):
    personalMatching = get_object_or_404(PersonalMatching, pk=personal_id)
    userId = request.session.get('userId')
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
    if(userId != personalMatching.user.id):
        personal = PersonalMatching.objects.order_by('-created')
        # 객체를 한 페이지로 자르기
        paginator = Paginator(personal, 8)
        # request에 담아주기
        page = request.GET.get('page')
        # request된 페이지를 얻어온 뒤 return 해 준다.
        personalList = paginator.get_page(page)
        error = '글을 작성한 사용자만 삭제할 수 있습니다.'
        return render(request, 'personalMatching/personal.html', {'countNotification':countNotification, 
        'notificationList':notificationList, 'fnsuser':fnsuser, 'personalList':personalList, 'error':error})
    personalMatching.delete()
    return redirect('personal')
    

def personalApply(request, personalId):
    if not (request.session.get('userId')):
        errormessage = '로그인을 해주세요.'
        return render(request, 'login.html', {'errormessage':errormessage})

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

    personalMatching = get_object_or_404(PersonalMatching, pk = personalId)

    isApplied = personalMatching.appliedPlayer.filter(id=request.session.get('userId')).exists()
    isAttended = personalMatching.attendedPlayer.filter(pk = request.session.get('userId')).exists()

    comments = PersonalComment.objects.filter(post = personalMatching.id).order_by('-created')
    # 객체를 한 페이지로 자르기
    commentPaginator = Paginator(comments, 15)
    # request에 담아주기
    commentPage = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    commentList = commentPaginator.get_page(commentPage)

        #만약 글 게시자가 신청 눌렀을 시
    if (fnsuser == personalMatching.user):
        error = "글 작성자는 신청을 못합니다."
        data = {
            'personalMatching':personalMatching, 
            'isApplied': isApplied, 
            'total_attendance': personalMatching.total_attendance(), 
            'error':error, 
            'isAttended':isAttended,
            'commentList':commentList,
            'countNotification':countNotification, 
            'notificationList':notificationList, 
            'fnsuser':fnsuser,
        }

        return render(request, 'personalMatching/personalDetail.html', data)

    elif (personalMatching.attendedPlayer.filter(pk = request.session.get('userId')).exists()):
        error = "이미 참가 확정 중입니다."
        data = {
            'personalMatching':personalMatching, 
            'isApplied': isApplied, 
            'isAttended':isAttended,
            'total_attendance': personalMatching.total_attendance(), 
            'error':error, 
            'commentList':commentList,
            'countNotification':countNotification, 
            'notificationList':notificationList, 
            'fnsuser':fnsuser,
        }

        return render(request, 'personalMatching/personalDetail.html', data)

    if isApplied:
        personalMatching.appliedPlayer.remove(fnsuser)
        isApplied = False
        alarm = '참가신청이 취소되었습니다.'
    
    
    elif personalMatching.number <= personalMatching.total_attendance():
        error = '모집인원이 다 모아져서 참가신청이 안됩니다.'
        data = {
            'personalMatching':personalMatching, 
            'isApplied': isApplied, 
            'isAttended':isAttended,
            'total_attendance': personalMatching.total_attendance(), 
            'error':error, 
            'commentList':commentList,
            'countNotification':countNotification, 
            'notificationList':notificationList, 
            'fnsuser':fnsuser,
        }

        return render(request, 'personalMatching/personalDetail.html', data)
    
    else:    
        personalMatching.appliedPlayer.add(fnsuser)
        isApplied = True
        alarm = '참가신청이 완료되었습니다.'
        newNotification = Notification.objects.create(
            creator = fnsuser,
            to = personalMatching.user,
            notification_type = Notification.personalApply,
            personalMatching = personalMatching
        )

        newNotification.personalApplyText()
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

    data = {
        'personalMatching':personalMatching, 
        'isApplied': isApplied, 
        'isAttended':isAttended,
        'total_attendance': personalMatching.total_attendance(), 
        'commentList':commentList,
        'countNotification':countNotification, 
        'notificationList':notificationList, 
        'fnsuser':fnsuser,
        'alarm':alarm,
    }
    return render(request, 'personalMatching/personalDetail.html', data)

def appliedPlayer(request, personalId):
    if not (request.session.get('userId')):
        errormessage = '로그인을 해주세요.'
        return render(request, 'login.html', {'errormessage':errormessage})

    fnsuser = get_object_or_404(FNSUser, pk = request.session.get('userId'))
    personalMatching = get_object_or_404(PersonalMatching, pk = personalId)

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
        'personalMatching':personalMatching,
        'countNotification':countNotification, 
        'notificationList':notificationList, 
    }

    return render(request, 'personalMatching/appliedPlayer.html', data)

#참가신청 수락
def personalAccept(request, userId, personalId):
    if not (request.session.get('userId')):
        errormessage = '로그인을 해주세요.'
        return render(request, 'login.html', {'errormessage':errormessage})

    fnsuser = get_object_or_404(FNSUser, pk = request.session.get('userId'))
    player = get_object_or_404(FNSUser, pk = userId)
    
    personalMatching = get_object_or_404(PersonalMatching, pk = personalId)
    personalMatching.attendedPlayer.add(player)
    personalMatching.appliedPlayer.remove(player)

    newNotification = Notification.objects.create(
        creator = fnsuser,
        to = player,
        notification_type = Notification.personalAccept,
        personalMatching = personalMatching
    )

    newNotification.personalAcceptText()
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

    alarm = '성공적으로 수락되었습니다.'

    data = {
        'personalMatching':personalMatching, 
        'total_attendance': personalMatching.total_attendance(), 
        'commentList':commentList,
        'countNotification':countNotification, 
        'notificationList':notificationList, 
        'fnsuser':fnsuser,
        'alarm':alarm,
    }

    return render(request, 'personalMatching/personalDetail.html', data)

#참가신청 전체수락
def personalAcceptAll(request, personalId):
    if not (request.session.get('userId')):
        errormessage = '로그인을 해주세요.'
        return render(request, 'login.html', {'errormessage':errormessage})

    fnsuser = get_object_or_404(FNSUser, pk = request.session.get('userId'))
    
    personalMatching = get_object_or_404(PersonalMatching, pk = personalId)
    appliedPlayer = personalMatching.appliedPlayer.all()
    for player in appliedPlayer:
        personalMatching.attendedPlayer.add(player)
        personalMatching.appliedPlayer.remove(player)
        newNotification = Notification.objects.create(
            creator = fnsuser,
            to = player,
            notification_type = Notification.personalAccept,
            personalMatching = personalMatching
        )
        newNotification.personalAcceptText()
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

    alarm = '성공적으로 수락되었습니다.'

    data = {
        'personalMatching':personalMatching, 
        'countNotification':countNotification, 
        'notificationList':notificationList, 
        'fnsuser':fnsuser,
        'alarm':alarm,
    }

    return render(request, 'personalMatching/personalDetail.html', data)

def personalDeny(request, userId, personalId):
    if not (request.session.get('userId')):
        errormessage = '로그인을 해주세요.'
        return render(request, 'login.html', {'errormessage':errormessage})

    fnsuser = get_object_or_404(FNSUser, pk = request.session.get('userId'))
    player = get_object_or_404(FNSUser, pk = userId)
    
    personalMatching = get_object_or_404(PersonalMatching, pk = personalId)
    personalMatching.appliedPlayer.remove(player)

    newNotification = Notification.objects.create(
        creator = fnsuser,
        to = player,
        notification_type = Notification.personalDeny,
        personalMatching = personalMatching
    )

    newNotification.personalDenyText()
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

    alarm = '성공적으로 거절되었습니다.'
    isApplied = False
    isAttended = False

    data = {
        'personalMatching':personalMatching, 
        'countNotification':countNotification, 
        'notificationList':notificationList, 
        'fnsuser':fnsuser,
        'alarm':alarm,
        'isApplied':isApplied,
        'isAttended':isAttended
    }

    return render(request, 'personalMatching/appliedPlayer.html', data)

def personalAttendanceCancel(request, personalId):
    if not (request.session.get('userId')):
        errormessage = '로그인을 해주세요.'
        return render(request, 'login.html', {'errormessage':errormessage})

    fnsuser = get_object_or_404(FNSUser, pk = request.session.get('userId'))
    personalMatching = get_object_or_404(PersonalMatching, pk = personalId)
    personalMatching.attendedPlayer.remove(fnsuser)

    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')[:20]
    # 객체를 한 페이지로 자르기
    paginator = Paginator(notification, 5)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    notificationList = paginator.get_page(page)

    alarm = '성공적으로 취소되었습니다.'

    data = {
        'personalMatching':personalMatching, 
        'countNotification':countNotification, 
        'notificationList':notificationList, 
        'fnsuser':fnsuser,
        'alarm':alarm
    }

    return render(request, 'personalMatching/personalDetail.html', data)

@require_POST
def personal_attendance(request):
    personalMatching = get_object_or_404(PersonalMatching, pk = request.POST.get('personal_id'))
    is_liked = personalMatching.attendance.filter(id=request.session.get('userId')).exists()
    comments = PersonalComment.objects.filter(post = personalMatching.id).order_by('-created')
    # 객체를 한 페이지로 자르기
    commentPaginator = Paginator(comments, 15)
    # request에 담아주기
    commentPage = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    commentList = commentPaginator.get_page(commentPage)

    if is_liked:
        personal = get_object_or_404(FNSUser, pk= request.session.get('userId'))
        personalMatching.attendance.remove(personal)
    
    
    elif personalMatching.number <= personalMatching.total_attendance():
        error = '모집인원이 다 모아져서 참가신청이 안됩니다.'
        attendance = personalMatching.attendance.all()
        return render(request, 'personalMatching/personalDetail.html', {'personalMatching':personalMatching, 
        'is_liked': is_liked, 'total_attendance': personalMatching.total_attendance(), 
        'attendance':attendance, 'error':error, 'commentList':commentList})
    
    else:    
        personal = get_object_or_404(FNSUser, pk= request.session.get('userId'))
        personalMatching.attendance.add(personal)
        newNotification = Notification.objects.create(
            creator = get_object_or_404(FNSUser, pk = request.session.get('userId')),
            to = personalMatching.user,
            notification_type = Notification.personalApply,
            personalMatching = personalMatching
        )

        newNotification.personalApplyText()
        newNotification.save()
        

    return HttpResponseRedirect(reverse('personalMatching/personalDetail', kwargs={'personal_id':personalMatching.id}))


def teamMatching(request):
    today = date.today()
    month = today.month
    day = today.day
    if not request.session.get('userId'):
        teamMatching = PersonalMatching.objects.all().filter(region = '충청남도', city = '천안시',
        time_from__month = today.month, time_from__day = today.day).order_by('time_from')
        # 객체를 한 페이지로 자르기
        paginator = Paginator(teamMatching, 8)
        # request에 담아주기
        page = request.GET.get('page')
        # request된 페이지를 얻어온 뒤 return 해 준다.
        teamList = paginator.get_page(page)

        data = {
            'teamList': teamList,
            'teamMatching':teamMatching,
            'today':today,
            'month':month,
            'day':day
        }
        return render(request, 'teamMatching/teamMatching.html', data)
    else:
        fnsuser = get_object_or_404(FNSUser, pk = request.session.get('userId'))
        teamMatching = TeamMatching.objects.all().filter(region = fnsuser.region, city = fnsuser.city,
        time_from__month = today.month, time_from__day = today.day).order_by('time_from')
        # 객체를 한 페이지로 자르기
        paginator = Paginator(teamMatching, 8)
        # request에 담아주기
        page = request.GET.get('page')
        # request된 페이지를 얻어온 뒤 return 해 준다.
        teamList = paginator.get_page(page)
        
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
            'month':month,
            'day':day,
            'countNotification':countNotification, 
            'teamMatching':teamMatching, 
            'teamList':teamList, 
            'notificationList':notificationList, 
            'fnsuser':fnsuser, 
            'today':today
        }
        return render(request, 'teamMatching/teamMatching.html', data)

def teamDay(request):
    today = datetime.today()
    month = request.GET.get('month')
    day = request.GET.get('day')
    region = request.GET.get('region')

    if request.GET.get('seoul') != None:
        city = request.GET.get('seoul')
    
    elif request.GET.get('gyeonggi') != None:
        city = request.GET.get('gyeonggi')

    elif request.GET.get('north_chungcheong') != None:
        city = request.GET.get('north_chungcheong')
    
    elif request.GET.get('south_chungcheong') != None:
        city = request.GET.get('south_chungcheong')
    
    elif request.GET.get('north_jeolla') != None:
        city = request.GET.get('north_jeolla')

    elif request.GET.get('south_jeolla') != None:
        city = request.GET.get('south_jeolla')

    elif request.GET.get('north_gyeongsang') != None:
        city = request.GET.get('north_gyeongsang')

    elif request.GET.get('south_gyeongsang') != None:
        city = request.GET.get('south_gyeongsang')

    elif request.GET.get('jeju') != None:
        city = request.GET.get('jeju')

    elif request.GET.get('incheon') != None:
        city = request.GET.get('incheon')

    elif request.GET.get('daejeon') != None:
        city = request.GET.get('daejeon')
    
    elif request.GET.get('gwangju') != None:
        city = request.GET.get('gwangju')

    elif request.GET.get('daegu') != None:
        city = request.GET.get('daegu')

    elif request.GET.get('ulsan') != None:
        city = request.GET.get('ulsan')

    elif request.GET.get('busan') != None:
        city = request.GET.get('busan')

    elif request.GET.get('sejong') != None:
        city = request.GET.get('sejong')

    elif request.GET.get('gangwon') != None:
        city = request.GET.get('gangwon')

    print('region : ' + region + ' city: ' + city)
    teamMatching = TeamMatching.objects.all().filter(region=region, city=city,
        time_from__month = int(month) + 1, time_from__day = day
    ).order_by('time_from')
    # 객체를 한 페이지로 자르기
    paginator = Paginator(teamMatching, 8)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    teamList = paginator.get_page(page)

    if request.session.get('userId'):
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
            'teamMatching':teamMatching,
            'teamList':teamList,
            'month' : month,
            'day' : day,
            'today':today,
            'fnsuser':fnsuser,
            'notificationList':notificationList,
            'countNotification':countNotification,
            'region':region,
            'city':city
        }
        return render(request, 'teamMatching/teamMatching.html', data)

    data = {
        'teamMatching':teamMatching,
        'teanList':teamList,
        'month' : month,
        'day' : day,
        'today':today,
        'region':region,
        'city':city
    }
    return render(request, 'teamMatching/teamMatching.html', data)

def teamMatchingNew(request):
    today = date.today()
    month = today.month
    day = today.day
    if not (request.session.get('userId')):
        errormessage = '로그인을 해주세요.'
        return render(request, 'login.html', {'errormessage':errormessage})

    fnsuser = get_object_or_404(FNSUser, pk = request.session.get('userId'))
    if not (fnsuser.teamname):
        error = '팀에 가입해야 글을 작성할 수 있습니다.'    
        teamMatching = TeamMatching.objects.all().filter(region = fnsuser.region, city = fnsuser.city,
        time_from__month = today.month, time_from__day = today.day).order_by('time_from')
        # 객체를 한 페이지로 자르기
        paginator = Paginator(teamMatching, 8)
        # request에 담아주기
        page = request.GET.get('page')
        # request된 페이지를 얻어온 뒤 return 해 준다.
        teamList = paginator.get_page(page)
        
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
            'month':month,
            'day':day,
            'countNotification':countNotification, 
            'teamMatching':teamMatching, 
            'teamList':teamList, 
            'notificationList':notificationList, 
            'fnsuser':fnsuser, 
            'today':today,
            'error':error
        }
        return render(request, 'teamMatching/teamMatching.html', data)

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
        'countNotification':countNotification, 
        'notificationList':notificationList, 
        'fnsuser':fnsuser
    }  
    return render(request, 'teamMatching/teamMatchingNew.html', data)

# 대관확인 페이지
def tCheckReservation(request):
    if not (request.session.get('userId')):
        errormessage = '로그인을 해주세요.'
        return render(request, 'login.html', {'errormessage':errormessage})

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
        'countNotification':countNotification, 
        'notificationList':notificationList, 
        'fnsuser':fnsuser
    }  
    return render(request, 'teamMatching/tCheckReservation.html', data)

def tIsReserved(request):
    if not (request.session.get('userId')):
        errormessage = '로그인을 해주세요.'
        return render(request, 'login.html', {'errormessage':errormessage})

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

    groundList = fnsuser.reservedGround.order_by('reservationDate')

    data = {
        'countNotification':countNotification, 
        'notificationList':notificationList, 
        'fnsuser':fnsuser,
        'groundList':groundList
    }  
    return render(request, 'teamMatching/tIsReserved.html', data)

def tPartnerNew(request):
    if not (request.session.get('userId')):
        errormessage = '로그인을 해주세요.'
        return render(request, 'login.html', {'errormessage':errormessage})

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

    groundList = fnsuser.reservedGround.order_by('reservationDate')

    selectedReservation = request.POST.get('selectedReservation')
    selected = selectedReservation.split(',')


    timeArray = []
    preReservation = None
    playground = None
    reservationDate = None
    for idx, reservationId in enumerate(selected):
        reservation = get_object_or_404(ReservationList, pk = reservationId)
        playground = reservation.playgroundName
        if preReservation == None: #첫 예약이면
            preReservation = reservation
            timeArray.append(preReservation.reservationTime)
        else:
            if preReservation.playgroundName.playgroundName != reservation.playgroundName.playgroundName:
                error = '2개의 구장을 선택할 수 없습니다.'
                data = {
                    'countNotification':countNotification, 
                    'notificationList':notificationList, 
                    'fnsuser':fnsuser,
                    'groundList':groundList,
                    'error':error
                }  
                return render(request, 'teamMatching/tIsReserved.html', data)

            elif preReservation.reservationDate != reservation.reservationDate:
                error = '다른 날짜의 예약을 동시에 선택할 수 없습니다.'
                data = {
                    'countNotification':countNotification, 
                    'notificationList':notificationList, 
                    'fnsuser':fnsuser,
                    'groundList':groundList,
                    'error':error
                }  
                return render(request, 'teamMatching/tIsReserved.html', data)

            else:
                reservationDate = reservation.reservationDate
                timeArray.append(reservation.reservationTime)

    minTime = None # 가장 이른 시간
    maxTime = None # 가장 나중 시간
    # 예약 시간 중 가장 빠른 시간과 늦은 시간을 구하는 for문
    for time in timeArray:
        if minTime == None and maxTime == None:
            minTime = time
            maxTime = time

        else:
            if int(time[0:2]) > int(maxTime[0:2]):
                maxTime = time

            elif int(time[0:2]) < int(minTime[0:2]):
                minTime = time

    # 예약 선택 시간이 연속된 시간이 아닐 시
    if len(selected) < ((int(maxTime[0:2])+1) - int(minTime[0:2])):
        error = '연속된 시간을 선택해주세요.'
        data = {
            'countNotification':countNotification, 
            'notificationList':notificationList, 
            'fnsuser':fnsuser,
            'groundList':groundList,
            'error':error
        }  
        return render(request, 'teamMatching/tIsReserved.html', data)

    data = {
        'countNotification':countNotification, 
        'notificationList':notificationList, 
        'fnsuser':fnsuser,
        'playground':playground.id,
        'maxTime':maxTime,
        'minTime':minTime,
        'reservationDate':reservationDate
    }
    return render(request, 'teamMatching/tPartnerNew.html', data)

def tPartnerCreate(request):
    if not (request.session.get('userId')):
        errormessage = '로그인을 해주세요.'
        return render(request, 'login.html', {'errormessage':errormessage})

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

    teamMatching = TeamMatching()
    maxTime = request.POST.get('maxTime')
    minTime = request.POST.get('minTime')
    playgroundId = request.POST.get('playground')
    playground = get_object_or_404(PlaygroundList, pk = playgroundId)
    rank = request.POST.get('rank')
    content = request.POST.get('content')
    joinFee = request.POST.get('joinFee')
    playDate = request.POST.get('reservationDate')
    year = playDate[0:4]
    month = playDate[4:6]
    day = playDate[6:8]
    startTime = year + '-' + month + '-' + day + ' ' + minTime[0:2] + ':' + '00'
    endTime = year + '-' + month + '-' + day + ' ' + maxTime[0:2] + ':' + '00'

    teamMatching.user = fnsuser
    teamMatching.location = playground
    teamMatching.region = playground.region
    teamMatching.city = playground.city
    teamMatching.time_from = startTime
    teamMatching.time_to = endTime
    teamMatching.rank = rank
    teamMatching.content = content
    teamMatching.joinFee = joinFee
    teamMatching.isReserved = '대관완료'
    teamMatching.myTeam = fnsuser.teamname
    teamMatching.save()

    redirectTo = reverse('teamMatchingDetail', kwargs = {'teamMatchingId':teamMatching.id})
    return HttpResponseRedirect(redirectTo)

def tNonPartnerNew(request):
    if not (request.session.get('userId')):
        errormessage = '로그인을 해주세요.'
        return render(request, 'login.html', {'errormessage':errormessage})

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

    groundList = fnsuser.reservedGround.order_by('reservationDate')

    return render(request, 'teamMatching/tNonPartnerNew.html')

def tNonPartnerCreate(request):
    if not (request.session.get('userId')):
        errormessage = '로그인을 해주세요.'
        return render(request, 'login.html', {'errormessage':errormessage})

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

    teamMatching =  TeamMatching()
    teamMatching.region = request.POST.get('region')

    if request.POST.get('seoul') != None:
        city = request.POST.get('seoul')
    
    elif request.POST.get('gyeonggi') != None:
        city = request.POST.get('gyeonggi')

    elif request.POST.get('north_chungcheong') != None:
        city = request.POST.get('north_chungcheong')
    
    elif request.POST.get('south_chungcheong') != None:
        city = request.POST.get('south_chungcheong')
    
    elif request.POST.get('north_jeolla') != None:
        city = request.POST.get('north_jeolla')

    elif request.POST.get('south_jeolla') != None:
        city = request.POST.get('south_jeolla')

    elif request.POST.get('north_gyeongsang') != None:
        city = request.POST.get('north_gyeongsang')

    elif request.POST.get('south_gyeongsang') != None:
        city = request.POST.get('south_gyeongsang')

    elif request.POST.get('jeju') != None:
        city = request.POST.get('jeju')

    elif request.POST.get('incheon') != None:
        city = request.POST.get('incheon')

    elif request.POST.get('daejeon') != None:
        city = request.POST.get('daejeon')
    
    elif request.POST.get('gwangju') != None:
        city = request.POST.get('gwangju')

    elif request.POST.get('daegu') != None:
        city = request.POST.get('daegu')

    elif request.POST.get('ulsan') != None:
        city = request.POST.get('ulsan')

    elif request.POST.get('busan') != None:
        city = request.POST.get('busan')

    elif request.POST.get('sejong') != None:
        city = request.POST.get('sejong')

    elif request.POST.get('gangwon') != None:
        city = request.POST.get('gangwon')

    teamMatching.city = city
    location = request.POST.get('location')
    if location == 'playground':
        teamMatching.location = None
    else:
        ground = location.split(",")
        playgroundList = get_object_or_404(PlaygroundList, pk = ground[0])
        teamMatching.location = playgroundList
    playDate = request.POST.get('playDate')
    playTime = request.POST.get('playTime')
    timeValue = playTime.split(',')
    smallNum = 0;
    largeNum = 0;
    reservationTimeArray = []
    for i in timeValue:
        reservationTimeArray.append(i)
        if smallNum is 0 and largeNum is 0:
            smallNum = int(i)
            largeNum = int(i)

        elif int(i) > largeNum:
            smallNum = largeNum
            largeNum = int(i)
            
        elif (int(i) < largeNum):
            if int(i) < smallNum:
                smallNum = int(i)
            
        

    year = playDate[0:4]
    month = playDate[6:8]
    date = playDate[10:12]
    if smallNum < 10:
        smallNum = '0' + str(smallNum)
    hour = str(smallNum)
    startDay = datetime(int(year), int(month), int(date))
    if int(hour) is 24:
        hour = '00'
        changedDate = startDay + timedelta(days=1)
        startMonth = changedDate.strftime('%m')
        startDate = changedDate.strftime('%d')
        startTime = year + '-' + startMonth + '-' + startDate + ' ' + hour + ':' + '00'
    else:
        startTime = year + '-' + month + '-' + date + ' ' + hour + ':' + '00'

    teamMatching.time_from = startTime
    

    if largeNum < 9:
        largeNum = '0' + str(largeNum+1)
    else:
        largeNum = int(largeNum) + 1
    endHour = str(largeNum)
    endMin = '00'
    day = datetime(int(year), int(month), int(date))
    if int(endHour) is 24 or int(endHour) is 25:
        if int(endHour) is 24:
            endHour = '00'
        elif int(endHour) is 25:
            endHour = '01'

        changedDate = day + timedelta(days=1)
        month = changedDate.strftime('%m')
        date = changedDate.strftime('%d')


    endTime = year + '-' + month + '-' + date + ' ' + endHour + ':' + endMin
    teamMatching.time_to = endTime
    teamMatching.joinFee = request.POST.get('joinFee')
    teamMatching.content = request.POST.get('content')
    teamMatching.rank = request.POST.get('rank')
    teamMatching.user = fnsuser
    teamMatching.isReserved = '대관완료'
    teamMatching.myTeam = fnsuser.teamname
    teamMatching.save()

    redirectTo = reverse('teamMatchingDetail', kwargs = {'teamMatchingId':teamMatching.id})
    return HttpResponseRedirect(redirectTo)

# 대관X -> 매칭글 옵션 선택창
def tChoice(request):
    if not (request.session.get('userId')):
        errormessage = '로그인을 해주세요.'
        return render(request, 'login.html', {'errormessage':errormessage})

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
        'countNotification':countNotification, 
        'notificationList':notificationList, 
        'fnsuser':fnsuser
    }  
    return render(request, 'teamMatching/tChoice.html', data)

# 대관 x -> 매칭만
def tMatchingFirst(request):
    if not (request.session.get('userId')):
        errormessage = '로그인을 해주세요.'
        return render(request, 'login.html', {'errormessage':errormessage})

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
        'countNotification':countNotification, 
        'notificationList':notificationList, 
        'fnsuser':fnsuser
    }  
    return render(request, 'teamMatching/tMatchingFirst.html', data)

# 매치먼저 시간선택
def tSelectTime(request):

    if not (request.session.get('userId')):
        errormessage = '로그인을 해주세요.'
        return render(request, 'login.html', {'errormessage':errormessage})


    location = request.POST.get('location')
    if location == 'playground':
        location = None
    else:
        ground = location.split(",")
        playground = get_object_or_404(PlaygroundList, pk = ground[0])
        
    reservationPossible = [["06"],["07"],["08"],["09"],["10"],["11"],["12"],["13"],["14"],["15"],["16"],["17"],["18"],["19"],["20"],["21"],["22"]]
    weekArray = []

    today = datetime.now()
    for i in range(0, 10):
        tomorrow = today + timedelta(days=i)
        tomorrow_format = tomorrow.strftime("%Y%m%d") 
        weekArray.append(tomorrow_format)

    selectedDay = request.GET.get('selectedDay')
    if not (selectedDay):
        selectedDay = datetime.now().strftime("%Y%m%d") 

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

    region = request.POST.get('region')

    if request.POST.get('seoul') != None:
        city = request.POST.get('seoul')
    
    elif request.POST.get('gyeonggi') != None:
        city = request.POST.get('gyeonggi')

    elif request.POST.get('north_chungcheong') != None:
        city = request.POST.get('north_chungcheong')
    
    elif request.POST.get('south_chungcheong') != None:
        city = request.POST.get('south_chungcheong')
    
    elif request.POST.get('north_jeolla') != None:
        city = request.POST.get('north_jeolla')

    elif request.POST.get('south_jeolla') != None:
        city = request.POST.get('south_jeolla')

    elif request.POST.get('north_gyeongsang') != None:
        city = request.POST.get('north_gyeongsang')

    elif request.POST.get('south_gyeongsang') != None:
        city = request.POST.get('south_gyeongsang')

    elif request.POST.get('jeju') != None:
        city = request.POST.get('jeju')

    elif request.POST.get('incheon') != None:
        city = request.POST.get('incheon')

    elif request.POST.get('daejeon') != None:
        city = request.POST.get('daejeon')
    
    elif request.POST.get('gwangju') != None:
        city = request.POST.get('gwangju')

    elif request.POST.get('daegu') != None:
        city = request.POST.get('daegu')

    elif request.POST.get('ulsan') != None:
        city = request.POST.get('ulsan')

    elif request.POST.get('busan') != None:
        city = request.POST.get('busan')

    elif request.POST.get('sejong') != None:
        city = request.POST.get('sejong')

    elif request.POST.get('gangwon') != None:
        city = request.POST.get('gangwon')

    rank = request.POST.get('rank')
    joinFee = request.POST.get('joinFee')
    content = request.POST.get('content')
    playDate = request.POST.get('playDate')

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
        'playground' : playground.id,
        "reservationPossible" : reservationPossible, 
        "today" : today, 
        "weekArray" : weekArray, 
        "selectedDay" : selectedDay,
        'region':region,
        'city':city,
        'rank':rank,
        'joinFee':joinFee,
        'content':content,
        'playDate':playDate
    }

    return render(request, 'teamMatching/tSelectTime.html', data)

# 매칭만 글쓰기
def tMatchingCreate(request):
    if not (request.session.get('userId')):
        errormessage = '로그인을 해주세요.'
        return render(request, 'login.html', {'errormessage':errormessage})

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

    teamMatching =  TeamMatching()
    teamMatching.region = request.POST.get('region')
    teamMatching.city = request.POST.get('city')
    playgroundId = request.POST.get('playgroundId')
    playground = get_object_or_404(PlaygroundList, pk = playgroundId)
    teamMatching.location = playground
    playDate = request.POST.get('playDate')
    playTime = request.POST.get('reservationTime')
    timeValue = playTime.split(',')
    smallNum = 0;
    largeNum = 0;
    reservationTimeArray = []
    for i in timeValue:
        reservationTimeArray.append(i)
        if smallNum is 0 and largeNum is 0:
            smallNum = int(i)
            largeNum = int(i)

        elif int(i) > largeNum:
            smallNum = largeNum
            largeNum = int(i)
            
        elif (int(i) < largeNum):
            if int(i) < smallNum:
                smallNum = int(i)    

    year = playDate[0:4]
    month = playDate[6:8]
    date = playDate[10:12]
    if smallNum < 10:
        smallNum = '0' + str(smallNum)
    hour = str(smallNum)
    startDay = datetime(int(year), int(month), int(date))
    if int(hour) is 24:
        hour = '00'
        changedDate = startDay + timedelta(days=1)
        startMonth = changedDate.strftime('%m')
        startDate = changedDate.strftime('%d')
        startTime = year + '-' + startMonth + '-' + startDate + ' ' + hour + ':' + '00'
    else:
        startTime = year + '-' + month + '-' + date + ' ' + hour + ':' + '00'

    teamMatching.time_from = startTime
    

    if largeNum < 9:
        largeNum = '0' + str(largeNum+1)
    else:
        largeNum = int(largeNum) + 1
    endHour = str(largeNum)
    endMin = '00'
    day = datetime(int(year), int(month), int(date))
    if int(endHour) is 24 or int(endHour) is 25:
        if int(endHour) is 24:
            endHour = '00'
        elif int(endHour) is 25:
            endHour = '01'

        changedDate = day + timedelta(days=1)
        month = changedDate.strftime('%m')
        date = changedDate.strftime('%d')


    endTime = year + '-' + month + '-' + date + ' ' + endHour + ':' + endMin
    teamMatching.time_to = endTime
    teamMatching.isReserved = '매칭 후 대관'
    teamMatching.joinFee = request.POST.get('joinFee')
    teamMatching.content = request.POST.get('content')
    teamMatching.rank = request.POST.get('rank')
    teamMatching.user = fnsuser
    teamMatching.myTeam = fnsuser.teamname
    teamMatching.save()

    redirectTo = reverse('teamMatchingDetail', kwargs = {'teamMatchingId':teamMatching.id})
    return HttpResponseRedirect(redirectTo)

# 대관 x -> 대관 후 매칭
def tBookingFirst(request):
    if not (request.session.get('userId')):
        errormessage = '로그인을 해주세요.'
        return render(request, 'login.html', {'errormessage':errormessage})

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
        'countNotification':countNotification, 
        'notificationList':notificationList, 
        'fnsuser':fnsuser
    }  
    return render(request, 'teamMatching/tBookingFirst.html', data)

# 매치먼저 시간선택
def tBookingTime(request):

    if not (request.session.get('userId')):
        errormessage = '로그인을 해주세요.'
        return render(request, 'login.html', {'errormessage':errormessage})


    location = request.POST.get('location')
    if location == 'playground':
        location = None
    else:
        ground = location.split(",")
        playground = get_object_or_404(PlaygroundList, pk = ground[0])
        
    reservationPossible = [["06"],["07"],["08"],["09"],["10"],["11"],["12"],["13"],["14"],["15"],["16"],["17"],["18"],["19"],["20"],["21"],["22"]]
    weekArray = []

    today = datetime.now()
    for i in range(0, 10):
        tomorrow = today + timedelta(days=i)
        tomorrow_format = tomorrow.strftime("%Y%m%d") 
        weekArray.append(tomorrow_format)

    selectedDay = request.GET.get('selectedDay')
    if not (selectedDay):
        selectedDay = datetime.now().strftime("%Y%m%d") 

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

    region = request.POST.get('region')

    if request.POST.get('seoul') != None:
        city = request.POST.get('seoul')
    
    elif request.POST.get('gyeonggi') != None:
        city = request.POST.get('gyeonggi')

    elif request.POST.get('north_chungcheong') != None:
        city = request.POST.get('north_chungcheong')
    
    elif request.POST.get('south_chungcheong') != None:
        city = request.POST.get('south_chungcheong')
    
    elif request.POST.get('north_jeolla') != None:
        city = request.POST.get('north_jeolla')

    elif request.POST.get('south_jeolla') != None:
        city = request.POST.get('south_jeolla')

    elif request.POST.get('north_gyeongsang') != None:
        city = request.POST.get('north_gyeongsang')

    elif request.POST.get('south_gyeongsang') != None:
        city = request.POST.get('south_gyeongsang')

    elif request.POST.get('jeju') != None:
        city = request.POST.get('jeju')

    elif request.POST.get('incheon') != None:
        city = request.POST.get('incheon')

    elif request.POST.get('daejeon') != None:
        city = request.POST.get('daejeon')
    
    elif request.POST.get('gwangju') != None:
        city = request.POST.get('gwangju')

    elif request.POST.get('daegu') != None:
        city = request.POST.get('daegu')

    elif request.POST.get('ulsan') != None:
        city = request.POST.get('ulsan')

    elif request.POST.get('busan') != None:
        city = request.POST.get('busan')

    elif request.POST.get('sejong') != None:
        city = request.POST.get('sejong')

    elif request.POST.get('gangwon') != None:
        city = request.POST.get('gangwon')

    rank = request.POST.get('rank')
    joinFee = request.POST.get('joinFee')
    content = request.POST.get('content')
    playDate = request.POST.get('playDate')

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
        'playground' : playground.id,
        "reservationPossible" : reservationPossible, 
        "today" : today, 
        "weekArray" : weekArray, 
        "selectedDay" : selectedDay,
        'region':region,
        'city':city,
        'rank':rank,
        'joinFee':joinFee,
        'content':content,
        'playDate':playDate
    }

    return render(request, 'teamMatching/tBookingTime.html', data)

# 결제 바로 이전 창
def tTryReservation(request):
    if not (request.session.get('userId')):
        errormessage = '로그인을 해주세요.'
        return render(request, 'login.html', {'errormessage':errormessage})

    region = request.POST.get('region', None)
    city = request.POST.get('city', None)
    joinFee = request.POST.get('joinFee', None)
    rank = request.POST.get('rank', None)
    content = request.POST.get('content', None)
    playgroundId = request.POST.get('playgroundId', None)
    playground = get_object_or_404(PlaygroundList, id = playgroundId)
    reservationTime = request.POST.get('reservationTime', None)
    playDate = request.POST.get('playDate', None)
    year = playDate[0:4]
    month = playDate[6:8]
    day = playDate[10:12]
    totalPrice = request.POST.get('totalPrice', None)
    reservationTimeArray = reservationTime.split(",")
    reservationDate = year + month + day
    reservationLength = len(reservationTimeArray)

    # 유저정보
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

    
            data = {
                'fnsuser':fnsuser,
                'notification':notification,
                'countNotification':countNotification,
                'notificationList': notificationList,
                'err_msg' : err_msg, 
                'id' : id
            }

            return render(request, 'reservation/tryReservation.html', data)  
        
    if err_msg != "duplicate reservation":
        err_msg = "try reservation"
        reserved_time = []

        for idx, reservation in enumerate(reservationTimeArray):
            print(reservation)
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
            "totalPrice" : totalPrice, 
            "reserved_time" : reserved_time, 
            "playground" : playground, 
            "playDate" : playDate, 
            "reservationLength" : reservationLength, 
            "reservationTime" : reservationTime, 
            "reservationDate" : reservationDate,
            'region':region,
            'city':city,
            'joinFee':joinFee,
            'content':content,
            'rank':rank
        }


        return render(request, 'teamMatching/tTryReservation.html', data)

# 대관 후 매칭 결과창
def tResultReservation(request):
    if not (request.session.get('userId')):
        errormessage = '로그인을 해주세요.'
        return render(request, 'login.html', {'errormessage':errormessage})

   
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


    playgroundId = request.POST.get('playgroundId', None)
    playground = get_object_or_404(PlaygroundList, id = playgroundId)
    reservationTime = request.POST.get('reservationTime', None)
    reservationDate = request.POST.get('reservationDate', None)
    reservationTimeArray = reservationTime.split(",")
    reservationLength = len(reservationTimeArray)
    reservationName = fnsuser.name
    reservationPhone = fnsuser.phone_number
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

    teamMatching =  TeamMatching()
    teamMatching.region = request.POST.get('region', None)
    teamMatching.city = request.POST.get('city', None)
    teamMatching.location = playground   

    year = reservationDate[0:4]
    month = reservationDate[4:6]
    date = reservationDate[6:8]
    startTime = year + '-' + month + '-' + date + ' ' + str(reserved_time[0]) + ':' + '00'

    teamMatching.time_from = startTime
    endTime = year + '-' + month + '-' + date + ' ' + str(reserved_time[1]) + ':' + '00'
    teamMatching.time_to = endTime
    teamMatching.joinFee = request.POST.get('joinFee', None)
    teamMatching.content = request.POST.get('content', None)
    teamMatching.rank = request.POST.get('rank', None)
    teamMatching.user = fnsuser
    teamMatching.myTeam = fnsuser.teamname
    teamMatching.isReserved = '대관완료'
    teamMatching.save()

    
    data = {
        'fnsuser':fnsuser,
        'notification':notification,
        'countNotification':countNotification,
        'notificationList': notificationList,
        'err_msg' : err_msg, 
        'playgroundId' : playgroundId, 
        "reserved_time" : reserved_time, 
        "reservationLength" : reservationLength, 
        "playground" : playground, 
        "totalPrice" : totalPrice,
        'teamMatching':teamMatching
    }  
    
    return render(request, 'teamMatching/tResultReservation.html', data)


def teamMatchingDetail(request, teamMatchingId):
    if not (request.session.get('userId')):
        errormessage = '로그인을 해주세요.'
        return render(request, 'login.html', {'errormessage':errormessage})
    
    if teamMatchingId == None:
        teamMatchingId = request.session.get('teamMatchingId')
    teamMatching = get_object_or_404(TeamMatching, pk=teamMatchingId)
    comments = TMComment.objects.filter(post = teamMatching.id).order_by('-created')
    # 객체를 한 페이지로 자르기
    commentPaginator = Paginator(comments, 15)
    # request에 담아주기
    commentPage = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    commentList = commentPaginator.get_page(commentPage)
    fnsuser = get_object_or_404(FNSUser, pk=request.session.get('userId'))
    errormessage = ''
    isApplied = False
    if not (fnsuser.teamname):
        errormessage = '팀에 먼저 가입해주세요'
        
    elif TmAppliedTeam.objects.filter(team=fnsuser.teamname, match=teamMatching).exists():
        isApplied = True

    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')[:20]
    # 객체를 한 페이지로 자르기
    paginator = Paginator(notification, 5)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    notificationList = paginator.get_page(page)
    return render(request, 'teamMatching/teamMatchingDetail.html', {'countNotification':countNotification, 'commentList':commentList,
    'notificationList':notificationList, 'isApplied':isApplied, 'fnsuser':fnsuser, 'comments':comments, 'teamMatching':teamMatching, 'errormessage':errormessage})

def tmcomment_write(request):    
    error = None
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
    if request.method == 'POST':
        teamMatching_id = request.POST.get('teamMatching_id', '').strip()
        teamMatching = get_object_or_404(TeamMatching, pk=teamMatching_id)
        comments = TMComment.objects.filter(post = teamMatching.id).order_by('-created')
        # 객체를 한 페이지로 자르기
        commentPaginator = Paginator(comments, 15)
        # request에 담아주기
        commentPage = request.GET.get('page')
        # request된 페이지를 얻어온 뒤 return 해 준다.
        commentList = commentPaginator.get_page(commentPage)
        content = request.POST.get('content', '').strip()

        if not content:
            error = '댓글을 입력해주세요.'

        if not error:
            comment = TMComment.objects.create(user=fnsuser, post_id= teamMatching_id, content= content)

            comments = TMComment.objects.filter(post = teamMatching.id).order_by('-created')
            # 객체를 한 페이지로 자르기
            commentPaginator = Paginator(comments, 15)
            # request에 담아주기
            commentPage = request.GET.get('page')
            # request된 페이지를 얻어온 뒤 return 해 준다.
            commentList = commentPaginator.get_page(commentPage)

            newNotification = Notification.objects.create(
            creator = get_object_or_404(FNSUser, pk=request.session.get('userId')),
            to = teamMatching.user,
            notification_type = Notification.teamComment,
            teamMatching = teamMatching
            )
            newNotification.teamCommentText()
            newNotification.save()
            # return redirect(reverse('teamMatching_detail', kwargs={'teamMatching_id':teamMatching_id}))

        return render(request, 'teamMatching/teamMatchingComment.html', {'error':error, 'countNotification':countNotification, 
        'notificationList':notificationList, 'countNotification':countNotification, 'fnsuser':fnsuser, 'commentList':commentList, 'teamMatching':teamMatching})

def deleteTC(request, teamComment_id):
    tmComment = get_object_or_404(TMComment, pk=teamComment_id)
    teamMatching = tmComment.post
    tmComment.delete()

    fnsuser = get_object_or_404(FNSUser, pk = request.session.get('userId'))
    comments = TMComment.objects.filter(post = teamMatching.id).order_by('-created')
    # 객체를 한 페이지로 자르기
    commentPaginator = Paginator(comments, 15)
    # request에 담아주기
    commentPage = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    commentList = commentPaginator.get_page(commentPage)
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')[:20]
    # 객체를 한 페이지로 자르기
    paginator = Paginator(notification, 5)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    notificationList = paginator.get_page(page)
    return render(request, 'teamMatching/teamMatchingComment.html', {'countNotification':countNotification, 
    'notificationList':notificationList, 'fnsuser':fnsuser, 'commentList':commentList, 'teamMatching':teamMatching})

def editTC(request, teamComment_id):
    error = None
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
    content = request.POST.get('content')
    tmComment = get_object_or_404(TMComment, pk = teamComment_id)

    if not content:
        error = '내용을 입력해주세요.'

    if not error:
        tmComment.content = content
        tmComment.save()
    
    teamMatching = tmComment.post
    comments = TMComment.objects.filter(post = teamMatching.id).order_by('-created')
    # 객체를 한 페이지로 자르기
    commentPaginator = Paginator(comments, 15)
    # request에 담아주기
    commentPage = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    commentList = commentPaginator.get_page(commentPage)
    return render(request, 'teamMatching/teamMatchingComment.html', {'teamMatching':teamMatching, 'error':error,
    'commentList':commentList, 'countNotification':countNotification, 'notificationList':notificationList, 'fnsuser':fnsuser})

def teamReply_write(request):
    error = None
    if request.method == 'POST':
        fnsuser = get_object_or_404(FNSUser, pk = request.session.get('userId'))    
        teamMatching_id = request.POST.get('teamMatching_id', '').strip()
        teamMatching = get_object_or_404(TeamMatching, pk=teamMatching_id)
        comment_id = request.POST.get('comment_id')
        tmComment = get_object_or_404(TMComment, pk = comment_id)

        comments = TMComment.objects.filter(post = teamMatching.id).order_by('-created')
        # 객체를 한 페이지로 자르기
        commentPaginator = Paginator(comments, 15)
        # request에 담아주기
        commentPage = request.GET.get('page')
        # request된 페이지를 얻어온 뒤 return 해 준다.
        commentList = commentPaginator.get_page(commentPage)
        content = request.POST.get('content', '').strip()

        if not content:
            error = '댓글을 입력해주세요.'

        if not error:
            commentReply = TeamReply.objects.create(user=fnsuser, post= teamMatching, 
            content= content, comment=tmComment)

            newNotification = Notification.objects.create(
            creator = get_object_or_404(FNSUser, pk=request.session.get('userId')),
            to = tmComment.user,
            notification_type = Notification.teamReply,
            teamMatching = teamMatching,
            tmComment = tmComment
            )
           
            newNotification.teamReplyText()
            newNotification.save()
            # return redirect(reverse('personalDetail', kwargs={'personal_id':personalMatching_id}))

    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')[:20]
    # 객체를 한 페이지로 자르기
    paginator = Paginator(notification, 5)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    notificationList = paginator.get_page(page)

    return render(request, 'teamMatching/teamMatchingComment.html', {'countNotification':countNotification, 
    'notificationList':notificationList, 'error':error, 'fnsuser':fnsuser, 'commentList':commentList, 'teamMatching':teamMatching})

def deleteTeamReply(request, reply_id):
    teamReply = get_object_or_404(TeamReply, pk=reply_id)
    teamMatching = teamReply.post
    teamReply.delete()

    fnsuser = get_object_or_404(FNSUser, pk = request.session.get('userId'))
    comments = TMComment.objects.filter(post = teamMatching.id).order_by('-created')
    # 객체를 한 페이지로 자르기
    commentPaginator = Paginator(comments, 15)
    # request에 담아주기
    commentPage = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    commentList = commentPaginator.get_page(commentPage)

    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')[:20]
    # 객체를 한 페이지로 자르기
    paginator = Paginator(notification, 5)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    notificationList = paginator.get_page(page)
    return render(request, 'teamMatching/teamMatchingComment.html', {'countNotification':countNotification, 
    'notificationList':notificationList, 'fnsuser':fnsuser, 'commentList':commentList, 'teamMatching':teamMatching})

def editTeamReply(request, reply_id):
    error = None
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
    content = request.POST.get('content')
    teamReply = get_object_or_404(TeamReply, pk = reply_id)

    if not content:
        error = '내용을 입력해주세요.'

    if not error:
        teamReply.content = content
        teamReply.save()

    teamMatching = teamReply.post
    comments = TMComment.objects.filter(post = teamMatching.id).order_by('-created')
    # 객체를 한 페이지로 자르기
    commentPaginator = Paginator(comments, 15)
    # request에 담아주기
    commentPage = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    commentList = commentPaginator.get_page(commentPage)

    return render(request, 'teamMatching/teamMatchingComment.html', {'teamMatching':teamMatching, 'error':error,
    'commentList':commentList, 'countNotification':countNotification, 'notificationList':notificationList, 'fnsuser':fnsuser})


def teamApplication(request, teamMatchingId):
    teamMatching = get_object_or_404(TeamMatching, pk=teamMatchingId)
    fnsuser = get_object_or_404(FNSUser, pk=request.session.get('userId'))
    message = ''
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')[:20]
    # 객체를 한 페이지로 자르기
    paginator = Paginator(notification, 5)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    notificationList = paginator.get_page(page)

    comments = TMComment.objects.filter(post = teamMatching.id).order_by('-created')
    # 객체를 한 페이지로 자르기
    commentPaginator = Paginator(comments, 15)
    # request에 담아주기
    commentPage = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    commentList = commentPaginator.get_page(commentPage)
    
    isApplied = False
    error = None

    if TmAppliedTeam.objects.filter(team=fnsuser.teamname, match=teamMatching).exists():
        isApplied = True

    data = {
        'countNotification':countNotification, 
        'commentList':commentList,
        'notificationList':notificationList, 
        'fnsuser':fnsuser, 
        'teamMatching':teamMatching, 
        'error':error,
        'isApplied':isApplied
    }

    if fnsuser.teamname.name == None:
        error = '먼저 팀에 가입해주세요.'
        return render(request, 'teamMatching/teamMatchingDetail.html', data)

    if teamMatching.myTeam == fnsuser.teamname:
        error = '자기 팀에게 매치신청을 할 수 없습니다.'
        return render(request, 'teamMatching/teamMatchingDetail.html',data)

    if TmAppliedTeam.objects.filter(match=teamMatching, team=fnsuser.teamname).exists():
        error = '이미 매치 신청을 하셨습니다.'
        return render(request, 'teamMatching/teamMatchingDetail.html', data)

    tmAppliedTeam = TmAppliedTeam.objects.create(team=fnsuser.teamname, match=teamMatching)
    isApplied = True
    error = '성공적으로 매치신청이 이루어졌습니다.'
    
    newNotification = Notification.objects.create(
        creator = get_object_or_404(FNSUser, pk=request.session.get('userId')),
        to = teamMatching.user,
        notification_type = Notification.teamMatchingApply,
        teamMatching = teamMatching
        )
           
    newNotification.teamMatchingApplyText()
    newNotification.save()
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.count()
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')[:20]
    # 객체를 한 페이지로 자르기
    paginator = Paginator(notification, 5)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    notificationList = paginator.get_page(page)
    
    data = {
        'countNotification':countNotification, 
        'commentList':commentList,
        'notificationList':notificationList, 
        'fnsuser':fnsuser, 
        'teamMatching':teamMatching, 
        'error':error,
        'isApplied':isApplied,
        'commentList':commentList, 
    }

    # redirectTo = reverse('teamMatchingDetail', kwargs = {'teamMatchingId':teamMatching.id, 'error':error})
    # return HttpResponseRedirect(redirectTo)
    return render(request, 'teamMatching/teamMatchingDetail.html', data)

def teamCancel(request, teamMatchingId):
    if not (request.session.get('userId')):
        errormessage = '로그인을 해주세요.'
        return render(request, 'login.html', {'errormessage':errormessage})

    fnsuser = get_object_or_404(FNSUser, pk=request.session.get('userId'))
    teamMatching = get_object_or_404(TeamMatching, pk = teamMatchingId)
    TmAppliedTeam.objects.filter(match=teamMatching, team=fnsuser.teamname).delete()
    comments = TMComment.objects.filter(post = teamMatching.id).order_by('-created')
    # 객체를 한 페이지로 자르기
    commentPaginator = Paginator(comments, 15)
    # request에 담아주기
    commentPage = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    commentList = commentPaginator.get_page(commentPage)
    isApplied = False
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')[:20]
    # 객체를 한 페이지로 자르기
    paginator = Paginator(notification, 5)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    notificationList = paginator.get_page(page)


    errormessage = '성공적으로 매치신청을 취소하셨습니다.'
    return render(request, 'teamMatching/teamMatchingDetail.html', {'countNotification':countNotification, 
    'notificationList':notificationList, 'isApplied':isApplied, 'fnsuser':fnsuser, 'commentList':commentList, 
    'teamMatching':teamMatching, 'errormessage':errormessage})


def appliedTeam(request, teamMatchingId):
    if not (request.session.get('userId')):
        errormessage = '로그인을 해주세요.'
        return render(request, 'login.html', {'errormessage':errormessage})

    teamMatching = get_object_or_404(TeamMatching, pk=teamMatchingId)
    fnsuser = get_object_or_404(FNSUser, pk=request.session.get('userId'))
    appliedTeams = TmAppliedTeam.objects.filter(match=teamMatching).all()
    comments = TMComment.objects.filter(post = teamMatching.id).order_by('-created')
    # 객체를 한 페이지로 자르기
    commentPaginator = Paginator(comments, 15)
    # request에 담아주기
    commentPage = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    commentList = commentPaginator.get_page(commentPage)
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
        'countNotification':countNotification, 
        'notificationList':notificationList,
        'commentList':commentList, 
        'fnsuser':fnsuser, 
        'appliedTeams':appliedTeams, 
        'teamMatching':teamMatching
    }
    return render(request, 'teamMatching/appliedTeam.html', data)

def matchApprove(request, teamMatchingId, teamId):
    teamMatching = get_object_or_404(TeamMatching, pk=teamMatchingId)
    team = get_object_or_404(Team, pk=teamId)
    fnsuser = get_object_or_404(FNSUser, pk = request.session.get('userId'))
    TmAppliedTeam.objects.filter(match=teamMatching, team=team).delete()
    teamMatching.vsTeam = team
    teamMatching.save()
    
    decidedMatch = DecidedMatch()
    decidedMatch.myTeam = teamMatching.myTeam
    decidedMatch.vsTeam = teamMatching.vsTeam
    decidedMatch.location = teamMatching.location
    decidedMatch.timeFrom = teamMatching.time_from
    decidedMatch.timeTo = teamMatching.time_to
    decidedMatch.match = teamMatching
    decidedMatch.save()

    newNotification = Notification.objects.create(
        creator = get_object_or_404(FNSUser, pk=request.session.get('userId')),
        to = teamMatching.user,
        teamMatching = teamMatching,
        notification_type = Notification.acceptSuggestion,
        team = fnsuser.teamname,
    )
    newNotification.acceptSuggestionText()
    newNotification.save()
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
    alarm = '성공적으로 매칭이 되었습니다.'

    data = {
        'countNotification':countNotification, 
        'notificationList':notificationList, 
        'fnsuser':fnsuser, 
        'alarm':alarm, 
        'teamMatching':teamMatching
    }
    return render(request, 'teamMatching/appliedTeam.html', data)

def matchDeny(request, teamMatchingId, teamId):
    teamMatching = get_object_or_404(TeamMatching, pk=teamMatchingId)
    team = get_object_or_404(Team, pk=teamId)
    fnsuser = get_object_or_404(FNSUser, pk = request.session.get('userId'))
    TmAppliedTeam.objects.filter(match=teamMatching, team=team).delete()
    
    newNotification = Notification.objects.create(
        creator = get_object_or_404(FNSUser, pk=request.session.get('userId')),
        to = teamMatching.user,
        teamMatching = teamMatching,
        notification_type = Notification.denySuggestion,
        team = fnsuser.teamname,
    )
    newNotification.denySuggestionText()
    newNotification.save()

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
    alarm = '매치신청을 거절하였습니다.'
    data = {
        'countNotification':countNotification, 
        'notificationList':notificationList, 
        'fnsuser':fnsuser, 
        'alarm':alarm, 
        'teamMatching':teamMatching
    }
    return render(request, 'teamMatching/appliedTeam.html', data)



def teamMatchingEditForm(request, teamMatchingId):
    teamMatching = get_object_or_404(TeamMatching, pk=teamMatchingId)
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

    isApplied = False
    if TmAppliedTeam.objects.filter(match=teamMatching, team=fnsuser.teamname).exists():
        isApplied = True

    if teamMatching.user != fnsuser:
        error = '글을 작성한 사용자만 수정할 수 있습니다.'
        return render(request, 'teamMatching/teamMatchingDetail.html', {'notificationList':notificationList, 'fnsuser':fnsuser, 'error':error, 'commentList':commentList,
        'countNotification':countNotification, 'isApplied':isApplied, 'teamMatching':teamMatching})
   
    data = {
        'countNotification':countNotification, 
        'notificationList':notificationList, 
        'fnsuser':fnsuser, 
        'teamMatching':teamMatching
    }
    if teamMatching.isReserved == '대관완료':
        if teamMatching.location.possibleReservation == True:
            return render(request, 'teamMatching/edit/editForBooker.html', data)
        else:
            return render(request, 'teamMatching/edit/editForNonPartner.html', data)
    elif teamMatching.isReserved == '매칭 후 대관':
        return render(request, 'teamMatching/edit/editForMatching.html', data)

# 매치먼저 시간수정
def tEditTime(request):

    if not (request.session.get('userId')):
        errormessage = '로그인을 해주세요.'
        return render(request, 'login.html', {'errormessage':errormessage})


    location = request.POST.get('location')
    teamMatchingId = request.POST.get('teamMatchingId', None)
    if location == 'playground':
        location = None
    else:
        ground = location.split(",")
        playground = get_object_or_404(PlaygroundList, pk = ground[0])
        
    reservationPossible = [["06"],["07"],["08"],["09"],["10"],["11"],["12"],["13"],["14"],["15"],["16"],["17"],["18"],["19"],["20"],["21"],["22"]]
    weekArray = []

    today = datetime.now()
    for i in range(0, 10):
        tomorrow = today + timedelta(days=i)
        tomorrow_format = tomorrow.strftime("%Y%m%d") 
        weekArray.append(tomorrow_format)

    selectedDay = request.GET.get('selectedDay')
    if not (selectedDay):
        selectedDay = datetime.now().strftime("%Y%m%d") 

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

    region = request.POST.get('region')

    if request.POST.get('seoul') != None:
        city = request.POST.get('seoul')
    
    elif request.POST.get('gyeonggi') != None:
        city = request.POST.get('gyeonggi')

    elif request.POST.get('north_chungcheong') != None:
        city = request.POST.get('north_chungcheong')
    
    elif request.POST.get('south_chungcheong') != None:
        city = request.POST.get('south_chungcheong')
    
    elif request.POST.get('north_jeolla') != None:
        city = request.POST.get('north_jeolla')

    elif request.POST.get('south_jeolla') != None:
        city = request.POST.get('south_jeolla')

    elif request.POST.get('north_gyeongsang') != None:
        city = request.POST.get('north_gyeongsang')

    elif request.POST.get('south_gyeongsang') != None:
        city = request.POST.get('south_gyeongsang')

    elif request.POST.get('jeju') != None:
        city = request.POST.get('jeju')

    elif request.POST.get('incheon') != None:
        city = request.POST.get('incheon')

    elif request.POST.get('daejeon') != None:
        city = request.POST.get('daejeon')
    
    elif request.POST.get('gwangju') != None:
        city = request.POST.get('gwangju')

    elif request.POST.get('daegu') != None:
        city = request.POST.get('daegu')

    elif request.POST.get('ulsan') != None:
        city = request.POST.get('ulsan')

    elif request.POST.get('busan') != None:
        city = request.POST.get('busan')

    elif request.POST.get('sejong') != None:
        city = request.POST.get('sejong')

    elif request.POST.get('gangwon') != None:
        city = request.POST.get('gangwon')

    rank = request.POST.get('rank')
    joinFee = request.POST.get('joinFee')
    content = request.POST.get('content')
    playDate = request.POST.get('playDate')

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
        'playground' : playground.id,
        "reservationPossible" : reservationPossible, 
        "today" : today, 
        "weekArray" : weekArray, 
        "selectedDay" : selectedDay,
        'region':region,
        'city':city,
        'rank':rank,
        'joinFee':joinFee,
        'content':content,
        'playDate':playDate,
        'teamMatchingId':teamMatchingId
    }

    return render(request, 'teamMatching/edit/tEditTime.html', data)

# 매칭만 글수정
def tMatchingEdit(request):
    if not (request.session.get('userId')):
        errormessage = '로그인을 해주세요.'
        return render(request, 'login.html', {'errormessage':errormessage})

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

    teamMatchingId = request.POST.get('teamMatchingId', None)
    teamMatching =  get_object_or_404(TeamMatching, pk = teamMatchingId)
    teamMatching.region = request.POST.get('region')
    teamMatching.city = request.POST.get('city')
    playgroundId = request.POST.get('playgroundId')
    playground = get_object_or_404(PlaygroundList, pk = playgroundId)
    teamMatching.location = playground
    playDate = request.POST.get('playDate')
    playTime = request.POST.get('reservationTime')
    timeValue = playTime.split(',')
    smallNum = 0;
    largeNum = 0;
    reservationTimeArray = []
    for i in timeValue:
        reservationTimeArray.append(i)
        if smallNum is 0 and largeNum is 0:
            smallNum = int(i)
            largeNum = int(i)

        elif int(i) > largeNum:
            smallNum = largeNum
            largeNum = int(i)
            
        elif (int(i) < largeNum):
            if int(i) < smallNum:
                smallNum = int(i)    

    year = playDate[0:4]
    month = playDate[6:8]
    date = playDate[10:12]
    if smallNum < 10:
        smallNum = '0' + str(smallNum)
    hour = str(smallNum)
    startDay = datetime(int(year), int(month), int(date))
    if int(hour) is 24:
        hour = '00'
        changedDate = startDay + timedelta(days=1)
        startMonth = changedDate.strftime('%m')
        startDate = changedDate.strftime('%d')
        startTime = year + '-' + startMonth + '-' + startDate + ' ' + hour + ':' + '00'
    else:
        startTime = year + '-' + month + '-' + date + ' ' + hour + ':' + '00'

    teamMatching.time_from = startTime
    

    if largeNum < 9:
        largeNum = '0' + str(largeNum+1)
    else:
        largeNum = int(largeNum) + 1
    endHour = str(largeNum)
    endMin = '00'
    day = datetime(int(year), int(month), int(date))
    if int(endHour) is 24 or int(endHour) is 25:
        if int(endHour) is 24:
            endHour = '00'
        elif int(endHour) is 25:
            endHour = '01'

        changedDate = day + timedelta(days=1)
        month = changedDate.strftime('%m')
        date = changedDate.strftime('%d')


    endTime = year + '-' + month + '-' + date + ' ' + endHour + ':' + endMin
    teamMatching.time_to = endTime
    teamMatching.isReserved = '매칭 후 대관'
    teamMatching.joinFee = request.POST.get('joinFee')
    teamMatching.content = request.POST.get('content')
    teamMatching.rank = request.POST.get('rank')
    teamMatching.user = fnsuser
    teamMatching.myTeam = fnsuser.teamname
    teamMatching.save()

    redirectTo = reverse('teamMatchingDetail', kwargs = {'teamMatchingId':teamMatching.id})
    return HttpResponseRedirect(redirectTo)

def teamMatchingDelete(request, teamMatchingId):
    teamMatching = get_object_or_404(TeamMatching, pk=teamMatchingId)
    fnsuser = get_object_or_404(FNSUser, pk=request.session.get('userId'))
    comments = TMComment.objects.filter(post = teamMatching.id).order_by('-created')
    # 객체를 한 페이지로 자르기
    commentPaginator = Paginator(comments, 15)
    # request에 담아주기
    commentPage = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    commentList = commentPaginator.get_page(commentPage)

    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')[:20]
    # 객체를 한 페이지로 자르기
    paginator = Paginator(notification, 5)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    notificationList = paginator.get_page(page)
    isApplied = False
    if TmAppliedTeam.objects.filter(match=teamMatching, team=fnsuser.teamname).exists():
        isApplied = True
    if teamMatching.user != fnsuser:
        error = '글을 작성한 사용자만 삭제할 수 있습니다.'
        return render(request, 'teamMatching/teamMatchingDetail.html', {'notificationList':notificationList, 'fnsuser':fnsuser, 'error':error, 'commentList':commentList,
        'countNotification':countNotification, 'isApplied':isApplied, 'teamMatching':teamMatching})
    
    teamMatching.delete()
    return redirect('/teamMatching')

def teamMatching_create(request):
    fnsuser = get_object_or_404(FNSUser, pk= request.session.get('userId'))
    team = get_object_or_404(Team, pk = fnsuser.teamname.id)
    
    teamMatching = TeamMatching()
    teamMatching.myteam = team
    teamMatching.user = fnsuser
    teamMatching.title = request.POST.get('title')
    teamMatching.sport = request.POST.get('sport')
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
    teamMatching.rank = request.POST.get('rank')
    teamMatching.content = request.POST.get('content')
    teamMatching.save()

    return redirect('/teamMatching')

def teamMatchingEdit(request, teamMatchingId):
   # 글 수정하기
    fnsuser = get_object_or_404(FNSUser, pk = request.session.get('userId'))
    teamMatching =  get_object_or_404(PersonalMatching, pk = teamMatchingId)

    # 이전 시간 구장 및 시간(예약삭제용)
    preTimeFrom = teamMatching.time_from
    preTimeTo = teamMatching.time_to
    prePlayground = teamMatching.location

    personalMatching.sport = request.POST.get('sport')
    personalMatching.content = request.POST.get('content')
    personalMatching.region = request.POST.get('region')

    if request.POST.get('seoul') != None:
        city = request.POST.get('seoul')
    
    elif request.POST.get('gyeonggi') != None:
        city = request.POST.get('gyeonggi')

    elif request.POST.get('north_chungcheong') != None:
        city = request.POST.get('north_chungcheong')
    
    elif request.POST.get('south_chungcheong') != None:
        city = request.POST.get('south_chungcheong')
    
    elif request.POST.get('north_jeolla') != None:
        city = request.POST.get('north_jeolla')

    elif request.POST.get('south_jeolla') != None:
        city = request.POST.get('south_jeolla')

    elif request.POST.get('north_gyeongsang') != None:
        city = request.POST.get('north_gyeongsang')

    elif request.POST.get('south_gyeongsang') != None:
        city = request.POST.get('south_gyeongsang')

    elif request.POST.get('jeju') != None:
        city = request.POST.get('jeju')

    elif request.POST.get('incheon') != None:
        city = request.POST.get('incheon')

    elif request.POST.get('daejeon') != None:
        city = request.POST.get('daejeon')
    
    elif request.POST.get('gwangju') != None:
        city = request.POST.get('gwangju')

    elif request.POST.get('daegu') != None:
        city = request.POST.get('daegu')

    elif request.POST.get('ulsan') != None:
        city = request.POST.get('ulsan')

    elif request.POST.get('busan') != None:
        city = request.POST.get('busan')

    elif request.POST.get('sejong') != None:
        city = request.POST.get('sejong')

    elif request.POST.get('gangwon') != None:
        city = request.POST.get('gangwon')

    personalMatching.city = city
    location = request.POST.get('location')
    if location == 'playground':
        personalMatching.location = None
    else:
        ground = location.split(",")
        playgroundList = get_object_or_404(PlaygroundList, pk = ground[0])
        personalMatching.location = playgroundList

    playDate = request.POST.get('playDate')
    playTime = request.POST.get('playTime')
    timeValue = playTime.split(',')
    smallNum = 0;
    largeNum = 0;
    reservationTimeArray = []
    for i in timeValue:
        reservationTimeArray.append(int(i))
        if smallNum is 0 and largeNum is 0:
            smallNum = int(i)
            largeNum = int(i)

        elif int(i) > largeNum:
            smallNum = largeNum
            largeNum = int(i)
            
        elif (int(i) < largeNum):
            if int(i) < smallNum:
                smallNum = int(i)
            
    

        year = playDate[0:4]
        month = playDate[6:8]
        date = playDate[10:12]
        hour = str(smallNum)
        startDay = datetime(int(year), int(month), int(date))
        if int(hour) is 24:
            hour = '00'
            changedDate = startDay + timedelta(days=1)
            startMonth = changedDate.strftime('%m')
            startDate = changedDate.strftime('%d')
            startTime = year + '-' + startMonth + '-' + startDate + ' ' + hour + ':' + '00'
        else:
            startTime = year + '-' + month + '-' + date + ' ' + hour + ':' + '00'

        personalMatching.time_from = startTime



        endHour = str(largeNum+1)
        endMin = '00'
        day = datetime(int(year), int(month), int(date))
        if int(endHour) is 24 or int(endHour) is 25:
            if int(endHour) is 24:
                endHour = '00'
            elif int(endHour) is 25:
                endHour = '01'

            changedDate = day + timedelta(days=1)
            month = changedDate.strftime('%m')
            date = changedDate.strftime('%d')


        endTime = year + '-' + month + '-' + date + ' ' + endHour + ':' + endMin
        personalMatching.time_to = endTime
        personalMatching.number = request.POST.get('number')
        personalMatching.joinFee = request.POST.get('joinFee')
        personalMatching.content = request.POST.get('content')
        user_id = request.session.get('userId')
        fnsUser = get_object_or_404(FNSUser, pk = user_id)
        personalMatching.user = fnsUser



        preYear = preTimeFrom.strftime("%Y")
        preMonth = preTimeFrom.strftime("%m")
        preDay = preTimeFrom.strftime("%d")
        preReservationDate = str(preYear) + str(preMonth) + str(preDay)
        preStartTime = preTimeFrom.strftime("%H")
        preEndTime = preTimeTo.strftime("%H")
        preReservation = []
        for i in range(int(preEndTime) - int(preStartTime)):
            preReservationTime = str(preStartTime) + '00'
            preReservation.append(preReservationTime)
            preStartTime = int(preStartTime) + 1
            if int(preStartTime) < 10:
                preStartTime = '0' + str(preStartTime)

        backupObject = []
        for i in preReservation:
            if prePlayground != None:
                reservation = prePlayground.reservation.filter(reservationTime = i).all()
                for reList in reservation:
                    preReservation = get_object_or_404(ReservationList, pk= reList.id)
                    if preReservation.reservationTime == i and preReservation.user == fnsuser and preReservation.playgroundName == prePlayground and preReservation.reservationDate == preReservationDate and preReservation.resercationUserId == "moonlit0130" and preReservation.reservationUserName == fnsuser.name and preReservation.resercationUserPhone == fnsuser.phone_number:
                        backupObject.append(preReservation)
                        preReservation.delete()            

        # check 예약 있는지 없는지  
        for idx, reservation in enumerate(reservationTimeArray):
            if personalMatching.location != None:
                reservationDate = str(year) + str(month) + str(date)
                if int(reservationTimeArray[idx]) < 10:
                    reservationTimeArray[idx] = '0' + str(reservationTimeArray[idx])
                reservationTime = str(reservationTimeArray[idx]) + "00"
                
                if playgroundList.reservation.filter(user = fnsuser, playgroundName = playgroundList, 
                reservationDate = reservationDate, reservationTime = reservationTime, 
                reservationUserName = fnsuser.name, resercationUserPhone = fnsuser.phone_number).exists():
                    error = '작성한 시간대는 이미 예약되어 있습니다.'
                    for i in backupObject:
                        i.save()
                    data = {
                        'error':error,
                        'personalMatching':personalMatching
                    }
                    return render(request, 'personalMatching/personalEdit.html', data)


        for idx, reservation in enumerate(reservationTimeArray):
            if personalMatching.location != None:
                reservationDate = str(year) + str(month) + str(date)
                if int(reservationTimeArray[idx]) < 10:
                    reservationTimeArray[idx] = '0' + str(reservationTimeArray[idx])
                reservationTime = str(reservationTimeArray[idx]) + "00"
                newReservation = ReservationList(user = fnsuser, playgroundName = playgroundList, 
                reservationDate = reservationDate, reservationTime = reservationTime, 
                resercationUserId = "moonlit0130", reservationUserName = fnsuser.name, 
                resercationUserPhone = fnsuser.phone_number)
                newReservation.save()

        
        personalMatching.save()
        return redirect(reverse('personal'))
    return render(request, 'personalMatching/personalDetail.html', {'countNotification':countNotification, 'notificationList':notificationList, 'fnsuser':fnsuser, 'personalMatching':personalMatching})


def teamMatchingComment(request, teamMatchingId):
    if not (request.session.get('userId')):
        errormessage = '로그인을 해주세요.'
        return render(request, 'login.html', {'errormessage':errormessage})

    fnsuser = get_object_or_404(FNSUser, pk = request.session.get('userId'))
    teamMatching = get_object_or_404(TeamMatching, pk = teamMatchingId)
    comments = PersonalComment.objects.filter(post = teamMatching.id).order_by('-created')
    # 객체를 한 페이지로 자르기
    commentPaginator = Paginator(comments, 15)
    # request에 담아주기
    commentPage = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    commentList = commentPaginator.get_page(commentPage)

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
        'countNotification':countNotification, 
        'notificationList':notificationList, 
        'fnsuser':fnsuser, 
        'teamMatching':teamMatching, 
        'comments':comments,
        'commentList':commentList
    }
    return render(request, 'teamMatching/teamMatchingComment.html', data)

def recruiting(request):
    if not (request.session.get('userId')):
        recruiting = Recruiting.objects.all().order_by('-created')
        # 객체를 한 페이지로 자르기
        paginator = Paginator(recruiting, 8)
        # request에 담아주기
        page = request.GET.get('page')
        # request된 페이지를 얻어온 뒤 return 해 준다.
        recruitingList = paginator.get_page(page)
        return render(request, 'recruiting/recruiting.html', {'recruitingList':recruitingList})

    else:
        recruiting = Recruiting.objects.all().order_by('-created')

        # 객체를 한 페이지로 자르기
        paginator = Paginator(recruiting, 8)
        # request에 담아주기
        page = request.GET.get('page')
        # request된 페이지를 얻어온 뒤 return 해 준다.
        recruitingList = paginator.get_page(page)

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
        return render(request, 'recruiting/recruiting.html', {'countNotification':countNotification, 
        'recruitingList':recruitingList, 'notificationList':notificationList, 'fnsuser':fnsuser, 'recruiting':recruiting})

def recruiting_new(request):
    if not (request.session.get('userId')):
        errormessage = '로그인을 해주세요.'
        return render(request, 'login.html', {'errormessage':errormessage})
    teams = Team.objects.all()
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
    if not (fnsuser.teamname):
        errormessage = '팀을 먼저 가입해주세요.'
        return render(request, 'recruiting/recruiting_new.html', {'notificationList':notificationList, 'fnsuser':fnsuser, 'teams':teams, 'errormessage':errormessage})

    return render(request, 'recruiting/recruiting_new.html', {'notificationList':notificationList, 'countNotification':countNotification, 
    'fnsuser':fnsuser, 'teams':teams})

def recruiting_create(request):
    recruiting = Recruiting()
    fnsuser = get_object_or_404(FNSUser, pk=request.session.get('userId'))
    recruiting.user = fnsuser
    recruiting.title = request.POST.get('title')
    recruiting.sport = request.POST.get('sport')
    vs_team_id = request.POST.get('vs_team')
    if vs_team_id == 'basic':
        errormessage = '상대팀을 선택해주세요'
        teams = Team.objects.all()
        notification = fnsuser.to.all()
        countNotification = notification.filter(userCheck = False).count()
        return render(request, 'recruiting/recruiting_new.html', {'teams':teams, 'errormessage':errormessage,
        'fnsuser':fnsuser, 'notification':notification, 'countNotification':countNotification}) 
    
    elif vs_team_id == '친선경기':
        vs_team_id = None
        

    elif vs_team_id != '친선경기':    
        vs_team = get_object_or_404(Team, pk=vs_team_id)
        if fnsuser.teamname == vs_team:
            errormessage = '자기 팀하고 시합을 할 수 없습니다. 친선경기로 선택해주세요.'
            teams = Team.objects.all()
            return render(request, 'recruiting/recruiting_new.html', {'teams':teams, 'errormessage':errormessage, 'fnsuser':fnsuser}) 
        else:
            recruiting.vs_team = vs_team

    
    recruiting.myteam = fnsuser.teamname
    recruiting.number = request.POST.get('number')
    recruiting.location = request.POST.get('location')
    time_from = request.POST.get('time_from')
    year = time_from[:4]
    month = time_from[5:7]
    date = time_from[8:10]
    hour = time_from[11:13]
    minute = time_from[14:16]
    startTime = year + '-' + month + '-' + date + ' ' + hour + ':' + minute
    recruiting.time_from = startTime
    time_to = request.POST.get('time_to')
    endHour = time_to[:2]
    endMin = time_to[3:5]
    endTime = year + '-' + month + '-' + date + ' ' + endHour + ':' + endMin
    recruiting.time_to = endTime
    recruiting.rank = request.POST.get('rank')
    recruiting.content = request.POST.get('content')
    recruiting.save()
    notification = fnsuser.to.all()
    countNotification = notification.filter(userCheck = False).count()
    return render(request, 'recruiting/recruiting_detail.html', {'fnsuser':fnsuser, 'recruiting':recruiting,
    'notification':notification, 'countNotification':countNotification})

def recruiting_detail(request, recruiting_id):
    if not (request.session.get('userId')):
        errormessage = '로그인을 해주세요.'
        return render(request, 'login.html', {'errormessage':errormessage})
    recruiting = get_object_or_404(Recruiting, pk = recruiting_id)
    fnsuser = get_object_or_404(FNSUser, pk=request.session.get('userId'))
    applied_players = recruiting.applied_player.all()
    accepted_players = recruiting.accepted_player.all()
    comments = REComment.objects.filter(post=recruiting).order_by('-created')
    # 객체를 한 페이지로 자르기
    commentPaginator = Paginator(comments, 15)
    # request에 담아주기
    commentPage = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    commentList = commentPaginator.get_page(commentPage)
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')[:20]
    # 객체를 한 페이지로 자르기
    paginator = Paginator(notification, 5)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    notificationList = paginator.get_page(page)
    is_writer = False
    if recruiting.user == fnsuser:
        is_writer = True

    is_applied = False
    if applied_players.filter(pk=fnsuser.id).exists():
        is_applied = True
    if accepted_players.filter(pk=fnsuser.id).exists():
        is_applied = True
    
    return render(request, 'recruiting/recruiting_detail.html', {'notificationList':notificationList, 'fnsuser':fnsuser, 'recruiting':recruiting, 'comments':comments,
    'countNotification':countNotification, 'applied_players':applied_players, 
    'commentList':commentList, 'accepted_players':accepted_players, 'is_writer':is_writer, 'is_applied':is_applied })

def recruiting_apply(request, recruiting_id):
    recruiting = get_object_or_404(Recruiting, pk=recruiting_id)
    pk = request.session.get('userId')
    fnsuser = get_object_or_404(FNSUser, pk=pk)
    is_applied = recruiting.applied_player.filter(pk=pk).exists()
    is_vsteam = False
    if recruiting.vs_team == fnsuser.teamname:
        is_vsteam = True
    accepted_players = recruiting.accepted_player.all()
    applied_players = recruiting.applied_player.all()
    members = recruiting.myteam.member.all()
    comments = REComment.objects.filter(post=recruiting).order_by('-created')
    # 객체를 한 페이지로 자르기
    commentPaginator = Paginator(comments, 15)
    # request에 담아주기
    commentPage = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    commentList = commentPaginator.get_page(commentPage)
    is_member = members.filter(pk=pk).exists()
    if is_member:
        message = '이미 팀 회원이십니다.'
        applied_players = recruiting.applied_player.all()
        return render(request, 'recruiting/recruiting_detail.html', {'recruiting': recruiting, 'commentList':commentList,
        'accepted_players': accepted_players, 'message':message, 'applied_players':applied_players 
        , 'countNotification':countNotification, 'notification':notification, 'fnsuser':fnsuser})

    if is_vsteam:
        message = '상대팀 회원이십니다.'
        applied_players = recruiting.applied_player.all()
        return render(request, 'recruiting/recruiting_detail.html', {'recruiting': recruiting, 'commentList':commentList,
        'accepted_players': accepted_players, 'message':message, 'applied_players':applied_players 
        , 'countNotification':countNotification, 'notification':notification, 'fnsuser':fnsuser})

    if is_applied:
        message = '이미 용병신청이 완료되었습니다.'    
    else:
        message = '용병신청이 완료되었습니다.'
        recruiting.applied_player.add(fnsuser)
        applied_players = recruiting.applied_player.all()
        newNotification = Notification.objects.create(
        creator = get_object_or_404(FNSUser, pk=request.session.get('userId')),
        to = recruiting.user,
        notification_type = Notification.recruitingApply,
        recruiting = recruiting
        )
           
        newNotification.recruitingApplyText()
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
    
    return render(request, 'recruiting/recruiting_detail.html', {'recruiting': recruiting, 'accepted_players': accepted_players, 
    'countNotification':countNotification, 'message':message, 'applied_players':applied_players, 'commentList':commentList, 'notificationList':notificationList, 'fnsuser':fnsuser})
    

def recruiting_list(request, recruiting_id):
    recruiting = get_object_or_404(Recruiting, pk=recruiting_id)
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
    members = recruiting.myteam.member.all()
    applied_players = recruiting.applied_player.all()
    accepted_players = recruiting.accepted_player.all()
    message = ''
    return render(request, 'recruiting/recruiting_list.html', {'notificationList':notificationList, 'fnsuser':fnsuser, 
    'countNotification':countNotification, 'recruiting': recruiting, 'applied_players': applied_players})

def recruiting_accept(request, recruiting_id, player_id):
    recruiting = get_object_or_404(Recruiting, pk=recruiting_id)
    fnsuser1 = get_object_or_404(FNSUser, pk=player_id)
    fnsuser = get_object_or_404(FNSUser, pk=request.session.get('userId'))
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    
    comments = REComment.objects.filter(post=recruiting).order_by('-created')
    # 객체를 한 페이지로 자르기
    commentPaginator = Paginator(comments, 15)
    # request에 담아주기
    commentPage = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    commentList = commentPaginator.get_page(commentPage)

    accepted = recruiting.accepted_player.count()
    if recruiting.number <= accepted:
        message = '참여인원보다 많은 인원을 수락할 수 없습니다.'
        applied_players = recruiting.applied_player.all()
        return render(request, 'recruiting/recruiting_list.html', {'notification':notification, 'fnsuser':fnsuser,
        'countNotification':countNotification, 'message':message, 'recruiting': recruiting, 'applied_players': applied_players})
    
    recruiting.applied_player.remove(fnsuser1)
    recruiting.accepted_player.add(fnsuser1)
    recruiting.save()
    
    applied_players = recruiting.applied_player.all()
    accepted_players = recruiting.accepted_player.all()

    newNotification = Notification.objects.create(
        creator = get_object_or_404(FNSUser, pk=request.session.get('userId')),
        to = fnsuser1,
        notification_type = Notification.recruitingAccepted,
        recruiting = recruiting
        )
           
    newNotification.recruitingAcceptedText()
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
    message = '성공적으로 용병수락이 되었습니다.'
    is_writer = False
    user = get_object_or_404(FNSUser, pk = request.session.get('userId'))
    if recruiting.user == user:
        is_writer = True
    return render(request, 'recruiting/recruiting_detail.html', {'notificationList':notificationList, 'fnsuser':fnsuser,
    'countNotification':countNotification, 'message':message, 'applied_players':applied_players, 
    'recruiting':recruiting, 'accepted_players':accepted_players, 'is_writer':is_writer, 'commentList':commentList})

def recruiting_deny(request, recruiting_id, player_id):
    recruiting = get_object_or_404(Recruiting, pk=recruiting_id)
    fnsuser1 = get_object_or_404(FNSUser, pk=player_id)
    fnsuser = get_object_or_404(FNSUser, pk=request.session.get('userId'))
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    comments = REComment.objects.filter(post=recruiting).order_by('-created')
    # 객체를 한 페이지로 자르기
    commentPaginator = Paginator(comments, 15)
    # request에 담아주기
    commentPage = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    commentList = commentPaginator.get_page(commentPage)

    recruiting.applied_player.remove(fnsuser1)
    recruiting.save()
    
    applied_players = recruiting.applied_player.all()
    accepted_players = recruiting.accepted_player.all()

    newNotification = Notification.objects.create(
        creator = get_object_or_404(FNSUser, pk=request.session.get('userId')),
        to = fnsuser1,
        notification_type = Notification.recruitingDenied,
        recruiting = recruiting
        )
           
    newNotification.recruitingDeniedText()
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
    message = '성공적으로 용병신청을 거절하였습니다.'
    is_writer = False
    user = get_object_or_404(FNSUser, pk = request.session.get('userId'))
    if recruiting.user == user:
        is_writer = True
    return render(request, 'recruiting/recruiting_detail.html', {'notificationList':notificationList, 'fnsuser':fnsuser,
    'countNotification':countNotification, 'message':message, 'applied_players':applied_players, 
    'recruiting':recruiting, 'accepted_players':accepted_players, 'is_writer':is_writer, 'commentList':commentList})


def recruiting_cancel(request, recruiting_id):
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
    recruiting = get_object_or_404(Recruiting, pk = recruiting_id)
    if recruiting.applied_player.filter(pk=fnsuser.id).exists():
        recruiting.applied_player.remove(fnsuser)
    elif recruiting.accepted_player.filter(pk=fnsuser.id).exists():
        recruiting.accepted_player.remove(fnsuser)
    
    applied_players = recruiting.applied_player.all()
    accepted_players = recruiting.accepted_player.all()
    comments = REComment.objects.filter(post=recruiting).order_by('-created')
    # 객체를 한 페이지로 자르기
    commentPaginator = Paginator(comments, 15)
    # request에 담아주기
    commentPage = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    commentList = commentPaginator.get_page(commentPage)

    is_writer = False
    if recruiting.user == fnsuser:
        is_writer = True

    is_applied = False
    message = '성공적으로 매치신청을 취소하셨습니다.'
    return render(request, 'recruiting/recruiting_detail.html', {'notificationList':notificationList, 'fnsuser':fnsuser,
    'countNotification':countNotification, 'message':message, 'recruiting':recruiting, 'commentList':commentList,
    'applied_players':applied_players, 'accepted_players':accepted_players, 'is_writer':is_writer, 'is_applied':is_applied })


    
    


def recruiting_editForm(request, recruiting_id):
    teams = Team.objects.all()
    recruiting = get_object_or_404(Recruiting, pk = recruiting_id)
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
    return render(request, 'recruiting/recruiting_editForm.html', {'notificationList':notificationList, 'fnsuser':fnsuser,
    'countNotification':countNotification, 'recruiting':recruiting, 'teams':teams})

def recruiting_edit(request, recruiting_id):
    recruiting = get_object_or_404(Recruiting, pk=recruiting_id)
    fnsuser = get_object_or_404(FNSUser, pk=request.session.get('userId'))
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    recruiting.title = request.POST.get('title')
    recruiting.sport = request.POST.get('sport')
    vs_team_id = request.POST.get('vs_team')
    if vs_team_id == 'basic':
        errormessage = '상대팀을 선택해주세요'
        teams = Team.objects.all()
        return render(request, 'recruiting/recruiting_editForm.html', {'notification':notification, 'fnsuser':fnsuser,
        'countNotification':countNotification, 'recruiting':recruiting, 'teams':teams, 'errormessage':errormessage}) 
    
    elif vs_team_id == '친선경기':
        vs_team_id = None
        
    elif vs_team_id != '친선경기':    
        vs_team = get_object_or_404(Team, pk=vs_team_id)
        if fnsuser.teamname == vs_team:
            errormessage = '자기 팀하고 시합을 할 수 없습니다. 친선경기로 선택해주세요.'
            teams = Team.objects.all()
            return render(request, 'recruiting/recruiting_editForm.html', {'notification':notification, 'fnsuser':fnsuser,
            'countNotification':countNotification, 'recruiting':recruiting, 'teams':teams, 'errormessage':errormessage}) 
        else:
            recruiting.vs_team = vs_team

    
    recruiting.myteam = fnsuser.teamname
    recruiting.number = request.POST.get('number')
    recruiting.location = request.POST.get('location')
    time_from = request.POST.get('time_from')
    year = time_from[:4]
    month = time_from[5:7]
    date = time_from[8:10]
    hour = time_from[11:13]
    minute = time_from[14:16]
    startTime = year + '-' + month + '-' + date + ' ' + hour + ':' + minute
    recruiting.time_from = startTime
    time_to = request.POST.get('time_to')
    endHour = time_to[:2]
    endMin = time_to[3:5]
    endTime = year + '-' + month + '-' + date + ' ' + endHour + ':' + endMin
    recruiting.time_to = endTime
    recruiting.rank = request.POST.get('rank')
    recruiting.content = request.POST.get('content')
    recruiting.save()
    return redirect('/recruiting')

def recruiting_delete(request, recruiting_id):
    recruiting = get_object_or_404(Recruiting, pk = recruiting_id)
    recruiting.delete()

    return redirect('recruiting')


def recomment_write(request):    
    error = None
    fnsuser = get_object_or_404(FNSUser, pk=request.session.get('userId'))
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    if request.method == 'POST':
        recruiting_id = request.POST.get('recruiting_id', '').strip()
        recruiting = get_object_or_404(Recruiting, pk=recruiting_id)
        comments = REComment.objects.filter(post = recruiting.id).order_by('-created')
       
        content = request.POST.get('content', '').strip()

        if not content:
            error = '댓글을 입력해주세요.'

        if not error:
            comment = REComment.objects.create(user=fnsuser, post_id= recruiting_id, content= content)

            newNotification = Notification.objects.create(
            creator = get_object_or_404(FNSUser, pk=request.session.get('userId')),
            to = recruiting.user,
            notification_type = Notification.recruitingComment,
            recruiting = recruiting
            )
           
            newNotification.recruitingCommentText()
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

    comments = REComment.objects.filter(post = recruiting.id).order_by('-created')
    # 객체를 한 페이지로 자르기
    commentPaginator = Paginator(comments, 15)
    # request에 담아주기
    commentPage = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    commentList = commentPaginator.get_page(commentPage)

    return render(request, 'recruiting/recruiting_detail.html', {'notificationList':notificationList, 'fnsuser':fnsuser,
    'countNotification':countNotification, 'error':error, 'fnsuser':fnsuser, 'commentList':commentList, 'recruiting':recruiting})

def deleteRC(request, recruitingComment_id):
    reComment = get_object_or_404(REComment, pk=recruitingComment_id)
    recruiting = reComment.post
    reComment.delete()

    fnsuser = get_object_or_404(FNSUser, pk = request.session.get('userId'))
    comments = REComment.objects.filter(post=recruiting).order_by('-created')
    # 객체를 한 페이지로 자르기
    commentPaginator = Paginator(comments, 15)
    # request에 담아주기
    commentPage = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    commentList = commentPaginator.get_page(commentPage)

    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')[:20]
    # 객체를 한 페이지로 자르기
    paginator = Paginator(notification, 5)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    notificationList = paginator.get_page(page)

    return render(request, 'recruiting/recruiting_detail.html', {'countNotification':countNotification, 
    'notificationList':notificationList, 'fnsuser':fnsuser, 'commentList':commentList, 'recruiting':recruiting})

def editRC(request, recruitingComment_id):
    error = None
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
    content = request.POST.get('content')
    reComment = get_object_or_404(REComment, pk = recruitingComment_id)

    if not content:
        error = '내용을 입력해주세요.'

    if not error:
        reComment.content = content
        reComment.save()
    
    recruiting = reComment.post
    comments = REComment.objects.filter(post=recruiting).order_by('-created')
    # 객체를 한 페이지로 자르기
    commentPaginator = Paginator(comments, 15)
    # request에 담아주기
    commentPage = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    commentList = commentPaginator.get_page(commentPage)

    return render(request, 'recruiting/recruiting_detail.html', {'recruiting':recruiting, 'error':error,
    'commentList':commentList, 'countNotification':countNotification, 'notificationList':notificationList, 'fnsuser':fnsuser})

def recruitingReply_write(request):
    error = None
    if  request.method == 'POST':
        fnsuser = get_object_or_404(FNSUser, pk = request.session.get('userId'))    
        recruiting_id = request.POST.get('recruiting_id', '').strip()
        recruiting = get_object_or_404(Recruiting, pk=recruiting_id)
        comment_id = request.POST.get('comment_id')
        reComment = get_object_or_404(REComment, pk = comment_id)

        comments = REComment.objects.filter(post = recruiting.id).order_by('-created')
        content = request.POST.get('content', '').strip()

        if not content:
            error = '댓글을 입력해주세요.'

        if not error:
            commentReply = RecruitingReply.objects.create(user=fnsuser, post= recruiting, 
            content= content, comment=reComment)

            newNotification = Notification.objects.create(
            creator = get_object_or_404(FNSUser, pk=request.session.get('userId')),
            to = reComment.user,
            notification_type = Notification.recruitingReply,
            recruiting = recruiting,
            reComment = reComment
            )
           
        newNotification.recruitingReplyText()
        newNotification.save()
        # return redirect(reverse('personalDetail', kwargs={'personal_id':personalMatching_id}))

        notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
        countNotification = notification.filter(userCheck = False).count()
        notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')[:20]
        # 객체를 한 페이지로 자르기
        paginator = Paginator(notification, 5)
        # request에 담아주기
        page = request.GET.get('page')
        # request된 페이지를 얻어온 뒤 return 해 준다.
        notificationList = paginator.get_page(page)

        comments = REComment.objects.filter(post = recruiting.id).order_by('-created')
        # 객체를 한 페이지로 자르기
        commentPaginator = Paginator(comments, 15)
        # request에 담아주기
        commentPage = request.GET.get('page')
        # request된 페이지를 얻어온 뒤 return 해 준다.
        commentList = commentPaginator.get_page(commentPage)

        return render(request, 'recruiting/recruiting_detail.html', {'countNotification':countNotification, 
        'notificationList':notificationList, 'error':error, 'fnsuser':fnsuser, 'commentList':commentList, 'recruiting':recruiting})

def deleteRecruitingReply(request, reply_id):
    recruitingReply = get_object_or_404(RecruitingReply, pk=reply_id)
    recruiting = recruitingReply.post
    recruitingReply.delete()

    fnsuser = get_object_or_404(FNSUser, pk = request.session.get('userId'))
    comments = REComment.objects.filter(post = recruiting.id).order_by('-created')
    # 객체를 한 페이지로 자르기
    commentPaginator = Paginator(comments, 15)
    # request에 담아주기
    commentPage = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    commentList = commentPaginator.get_page(commentPage)

    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')[:20]
    # 객체를 한 페이지로 자르기
    paginator = Paginator(notification, 5)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    notificationList = paginator.get_page(page)
    return render(request, 'recruiting/recruiting_detail.html', {'countNotification':countNotification, 
    'notificationList':notificationList, 'fnsuser':fnsuser, 'commentList':commentList, 'recruiting':recruiting})

def editRecruitingReply(request, reply_id):
    error = None
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
    content = request.POST.get('content')
    recruitingReply = get_object_or_404(RecruitingReply, pk = reply_id)

    if not content:
        error = '내용을 입력해주세요.'

    if not error:
        recruitingReply.content = content
        recruitingReply.save()

    recruiting = recruitingReply.post
    comments = REComment.objects.filter(post=recruiting).order_by('-created')
    # 객체를 한 페이지로 자르기
    commentPaginator = Paginator(comments, 15)
    # request에 담아주기
    commentPage = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    commentList = commentPaginator.get_page(commentPage)
    return render(request, 'recruiting/recruiting_detail.html', {'recruiting':recruiting, 'error':error,
    'commentList':commentList, 'countNotification':countNotification, 'notificationList':notificationList, 'fnsuser':fnsuser})




# League 관련 views
def league(request):
    if not (request.session.get('userId')):
        leagues = League.objects.all().order_by('-created')

        # 객체를 한 페이지로 자르기
        paginator = Paginator(leagues, 8)
        # request에 담아주기
        page = request.GET.get('page')
        # request된 페이지를 얻어온 뒤 return 해 준다.
        leagueList = paginator.get_page(page)
        return render(request, 'league/league.html', {'leagueList':leagueList})
    else:
        leagues = League.objects.all().order_by('-created')

        # 객체를 한 페이지로 자르기
        paginator = Paginator(leagues, 8)
        # request에 담아주기
        page = request.GET.get('page')
        # request된 페이지를 얻어온 뒤 return 해 준다.
        leagueList = paginator.get_page(page)

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
        if not (request.session.get('userId')):
            login = '로그인을 해주세요.'
            return render(request, 'league/league.html', {'leagueList':leagueList, 'countNotification':countNotification, 'notificationList':notificationList, 'fnsuser':fnsuser, 'leagues':leagues, 'login':login}) 
        return render(request, 'league/league.html', {'leagueList':leagueList, 'countNotification':countNotification, 'notificationList':notificationList, 'fnsuser':fnsuser, 'leagues':leagues})

def league_new(request):
    if not (request.session.get('userId')):
        errormessage = '로그인을 해주세요.'
        return render(request, 'login.html', {'errormessage':errormessage})
    
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
    if fnsuser.isStaff == True:
        return render(request, 'league/league_new.html', {'countNotification':countNotification, 'notificationList':notificationList, 'fnsuser':fnsuser})
    else:
        message = '매니저만 글을 작성할 수 있습니다.'
        leagues = League.objects.all().order_by('-created')
            # 객체를 한 페이지로 자르기
        paginator = Paginator(leagues, 8)
        # request에 담아주기
        page = request.GET.get('page')
        # request된 페이지를 얻어온 뒤 return 해 준다.
        leagueList = paginator.get_page(page)
        
        return render(request, 'league/league.html', {'countNotification':countNotification, 
        'leagueList':leagueList, 'notificationList':notificationList, 'fnsuser':fnsuser, 'leagues':leagues, 'message':message})

def league_create(request):
    league = League()
    fnsuser = get_object_or_404(FNSUser, pk=request.session.get('userId'))
    league.manager = fnsuser
    league.title = request.POST.get('title')
    league.location = request.POST.get('location')
    time_from = request.POST.get('time_from')
    year = time_from[:4]
    month = time_from[5:7]
    date = time_from[8:10]
    hour = time_from[11:13]
    minute = time_from[14:16]
    startTime = year + '-' + month + '-' + date + ' ' + hour + ':' + minute
    league.time_from = startTime
    time_to = request.POST.get('time_to')
    endHour = time_to[:2]
    endMin = time_to[3:5]
    endTime = year + '-' + month + '-' + date + ' ' + endHour + ':' + endMin
    league.time_to = endTime
    league.content = request.POST.get('content')
    league.save()
    return redirect('/league')

def league_detail(request, league_id):
    if not (request.session.get('userId')):
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
    league = get_object_or_404(League, pk=league_id)
    comments = LGComment.objects.filter(post = league).order_by('-created')
    # 객체를 한 페이지로 자르기
    commentPaginator = Paginator(comments, 15)
    # request에 담아주기
    commentPage = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    commentList = commentPaginator.get_page(commentPage)

    is_personal = LgPlayerAttendance.objects.filter(match=league, player=fnsuser).exists()
    is_team = False
    if fnsuser.teamname:
        is_team = LgTeamAttendance.objects.filter(match=league, team = fnsuser.teamname).exists()
    attended_players = LgPlayerAttendance.objects.filter(match=league).all()
    attended_teams = LgTeamAttendance.objects.filter(match=league).all()
    return render(request, 'league/league_detail.html', {'notificationList':notificationList, 'fnsuser':fnsuser, 'comments':comments, 'attended_players':attended_players, 'league':league,
    'countNotification':countNotification, 'attended_teams':attended_teams, 'is_team':is_team, 
    'commentList':commentList, 'is_personal':is_personal})

def league_editForm(request, league_id):
    league = get_object_or_404(League, pk = league_id)
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
    return render(request, 'league/league_editForm.html', {'notificationList':notificationList, 'fnsuser':fnsuser,
    'countNotification':countNotification, 'league':league})

def league_edit(request, league_id):
    league = get_object_or_404(League, pk=league_id)
    fnsuser = get_object_or_404(FNSUser, pk=request.session.get('userId'))
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    league.title = request.POST.get('title')
    league.location = request.POST.get('location')
    time_from = request.POST.get('time_from')
    year = time_from[:4]
    month = time_from[5:7]
    date = time_from[8:10]
    hour = time_from[11:13]
    minute = time_from[14:16]
    startTime = year + '-' + month + '-' + date + ' ' + hour + ':' + minute
    league.time_from = startTime
    time_to = request.POST.get('time_to')
    endHour = time_to[:2]
    endMin = time_to[3:5]
    endTime = year + '-' + month + '-' + date + ' ' + endHour + ':' + endMin
    league.time_to = endTime
    league.content = request.POST.get('content')
    league.save()
    return redirect('/league')

def league_delete(request, league_id):
    league = get_object_or_404(League, pk = league_id)
    league.delete()

    return redirect('/league')

def personal_apply(request, league_id):
    league = get_object_or_404(League, pk=league_id)
    comments = LGComment.objects.filter(post = league).order_by('-created')
    # 객체를 한 페이지로 자르기
    commentPaginator = Paginator(comments, 15)
    # request에 담아주기
    commentPage = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    commentList = commentPaginator.get_page(commentPage)

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
    attended_players = LgPlayerAttendance.objects.all().filter(match=league)
    attended_teams = LgTeamAttendance.objects.all().filter(match=league)
    is_personal = attended_players.filter(match=league, player=fnsuser).exists()
    is_team = False
    if fnsuser.teamname:
        # is_team = attended_teams.filter(match=league, team=fnsuser.teamname).exists()
        is_team = LgTeamAttendance.objects.filter(match=league, team = fnsuser.teamname).exists()

    if is_personal:
        message = '이미 참가신청을 했습니다.'
        return render(request, 'league/league_detail.html', {'notificationList':notificationList, 'fnsuser':fnsuser,
        'countNotification':countNotification, 'commentList':commentList, 'attended_players':attended_players, 'league':league,
        'attended_teams':attended_teams, 'is_team':is_team, 'is_personal':is_personal, 'message':message})
    else:
        message = '참가신청을 완료했습니다.'
        lgPlayerAttendance = LgPlayerAttendance.objects.create(player=fnsuser, match=league)
        is_personal = LgPlayerAttendance.objects.filter(match=league, player=fnsuser).exists()
        attended_players = LgPlayerAttendance.objects.filter(match=league).all()

        newNotification = Notification.objects.create(
        creator = get_object_or_404(FNSUser, pk=request.session.get('userId')),
        to = league.manager,
        notification_type = Notification.leaguePersonalApply,
        league = league
        )
           
        newNotification.leaguePersonalApplyText()
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
        return render(request, 'league/league_detail.html', {'notificationList':notificationList, 'fnsuser':fnsuser, 
        'countNotification':countNotification, 'attended_players':attended_players, 'league':league,
        'commentList':commentList, 'attended_teams':attended_teams, 'is_personal':is_personal, 'is_team':is_team, 'message':message})

def personal_cancel(request, league_id):
    league = get_object_or_404(League, pk=league_id)
    comments = LGComment.objects.filter(post = league).order_by('-created')
    # 객체를 한 페이지로 자르기
    commentPaginator = Paginator(comments, 15)
    # request에 담아주기
    commentPage = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    commentList = commentPaginator.get_page(commentPage)
    
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
    LgPlayerAttendance.objects.filter(match=league, player=fnsuser).delete()
    attended_players = LgPlayerAttendance.objects.filter(match=league).all()
    attended_teams = LgTeamAttendance.objects.filter(match=league).all()
    is_personal = LgPlayerAttendance.objects.filter(match=league, player=fnsuser).exists()
    message = '성공적으로 취소되었습니다.'
    is_team = False
    if fnsuser.teamname:
        is_team = LgTeamAttendance.objects.filter(match=league, team=fnsuser.teamname).exists()
    
    return render(request, 'league/league_detail.html', {'notificationList':notificationList, 'fnsuser':fnsuser, 
    'countNotification':countNotification, 'attended_players':attended_players, 'league':league,
    'commentList':commentList, 'attended_teams':attended_teams, 'is_personal':is_personal, 'is_team':is_team, 'message':message})


def team_apply(request, league_id):
    league = get_object_or_404(League, pk=league_id)
    comments = LGComment.objects.filter(post = league).order_by('-created')
    # 객체를 한 페이지로 자르기
    commentPaginator = Paginator(comments, 15)
    # request에 담아주기
    commentPage = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    commentList = commentPaginator.get_page(commentPage)

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
    attended_players = LgPlayerAttendance.objects.filter(match=league).all()
    attended_teams = LgTeamAttendance.objects.filter(match=league).all()
    is_personal = LgPlayerAttendance.objects.filter(match=league, player=fnsuser).exists()
    

    if not (fnsuser.teamname):
        message = '팀에 먼저 가입해주세요'
        is_team = False
        return render(request, 'league/league_detail.html', {'countNotification':countNotification, 'attended_players':attended_players, 'league':league,
        'notificationList':notificationList, 'fnsuser':fnsuser, 'commentList':commentList, 'attended_teams':attended_teams, 'is_personal':is_personal, 'is_team':is_team, 'message':message})
   
    is_team = LgTeamAttendance.objects.filter(match=league, team=fnsuser.teamname).exists()  
    if fnsuser != fnsuser.teamname.teamleader:
        message = '팀대표만 신청할 수 있습니다.'
        return render(request, 'league/league_detail.html', {'countNotification':countNotification, 'attended_players':attended_players, 'league':league,
        'notificationList':notificationList, 'fnsuser':fnsuser, 'commentList':commentList, 'attended_teams':attended_teams, 'is_personal':is_personal, 'is_team':is_team, 'message':message})

    else:
        if is_team:
            message = '이미 신청하셨습니다.'
            return render(request, 'league/league_detail.html', {'countNotification':countNotification, 'attended_players':attended_players, 'league':league,
            'notificationList':notificationList, 'fnsuser':fnsuser, 'commentList':commentList, 'attended_teams':attended_teams, 'is_personal':is_personal, 'is_team':is_team, 'message':message})
        else:
            lgTeamAttendance = LgTeamAttendance.objects.create(team = fnsuser.teamname, match=league)
            attended_teams = LgTeamAttendance.objects.filter(match=league).all()
            is_team = True
            message = '성공적으로 신청이 되었습니다.'

            newNotification = Notification.objects.create(
            creator = get_object_or_404(FNSUser, pk=request.session.get('userId')),
            to = league.manager,
            notification_type = Notification.leagueTeamApply,
            league = league
            )
                
            newNotification.leagueTeamApplyText()
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
            return render(request, 'league/league_detail.html', {'countNotification':countNotification, 'attended_players':attended_players, 'league':league,
            'notificationList':notificationList, 'fnsuser':fnsuser, 'commentList':commentList, 'attended_teams':attended_teams, 'is_personal':is_personal, 'is_team':is_team, 'message':message})

def team_cancel(request, league_id):
    league = get_object_or_404(League, pk=league_id)
    comments = LGComment.objects.filter(post = league).order_by('-created')
    # 객체를 한 페이지로 자르기
    commentPaginator = Paginator(comments, 15)
    # request에 담아주기
    commentPage = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    commentList = commentPaginator.get_page(commentPage)

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
    attended_players = LgPlayerAttendance.objects.filter(match=league).all()
    attended_teams = LgTeamAttendance.objects.filter(match=league).all()
    is_personal = LgPlayerAttendance.objects.filter(player=fnsuser).exists()
    

    if not (fnsuser.teamname):
        message = '팀에 먼저 가입해주세요'
        is_team = False
        return render(request, 'league/league_detail.html', {'countNotification':countNotification, 'attended_players':attended_players, 'league':league,
        'notificationList':notificationList, 'fnsuser':fnsuser, 'commentList':commentList, 'attended_teams':attended_teams, 'is_personal':is_personal, 'is_team':is_team, 'message':message})
   
    is_team = LgTeamAttendance.objects.filter(match=league, team = fnsuser.teamname).exists()  
    if fnsuser != fnsuser.teamname.teamleader:
        message = '팀대표만 취소할 수 있습니다.'
        return render(request, 'league/league_detail.html', {'countNotification':countNotification, 'attended_players':attended_players, 'league':league,
        'notificationList':notificationList, 'fnsuser':fnsuser, 'commentList':commentList, 'attended_teams':attended_teams, 'is_personal':is_personal, 'is_team':is_team, 'message':message})

    else:
        message = '성공적으로 취소되었습니다.'
        LgTeamAttendance.objects.filter(match=league, team=fnsuser.teamname).delete()
        attended_teams = LgTeamAttendance.objects.filter(match=league).all()
        is_team = LgTeamAttendance.objects.filter(match=league, team = fnsuser.teamname).exists()
        return render(request, 'league/league_detail.html', {'countNotification':countNotification, 'attended_players':attended_players, 'league':league,
        'notificationList':notificationList, 'fnsuser':fnsuser, 'commentList':commentList, 'attended_teams':attended_teams, 'is_personal':is_personal, 'is_team':is_team, 'message':message})
    
def lgcomment_write(request):    
    error = None
    fnsuser = get_object_or_404(FNSUser, pk=request.session.get('userId'))
    
    if request.method == 'POST':
        league_id = request.POST.get('league_id', '').strip()
        league = get_object_or_404(League, pk=league_id)
        comments = LGComment.objects.filter(post = league).order_by('-created')
        # 객체를 한 페이지로 자르기
        commentPaginator = Paginator(comments, 15)
        # request에 담아주기
        commentPage = request.GET.get('page')
        # request된 페이지를 얻어온 뒤 return 해 준다.
        commentList = commentPaginator.get_page(commentPage)
       
        content = request.POST.get('content', '').strip()

        if not content:
            error = '댓글을 입력해주세요.'

        if not error:
            comment = LGComment.objects.create(user=fnsuser, post_id= league_id, content= content)

            newNotification = Notification.objects.create(
            creator = get_object_or_404(FNSUser, pk=request.session.get('userId')),
            to = league.manager,
            notification_type = Notification.leagueComment,
            league = league
            )
           
            newNotification.leagueCommentText()
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

        return render(request, 'league/league_detail.html', {'countNotification':countNotification, 'notificationList':notificationList, 'fnsuser':fnsuser,
        'error':error, 'fnsuser':fnsuser, 'commentList':commentList, 'league':league})


def deleteLC(request, leagueComment_id):
    lgComment = get_object_or_404(LGComment, pk=leagueComment_id)
    league = lgComment.post
    lgComment.delete()

    fnsuser = get_object_or_404(FNSUser, pk = request.session.get('userId'))
    comments = LGComment.objects.filter(post = league).order_by('-created')
    # 객체를 한 페이지로 자르기
    commentPaginator = Paginator(comments, 15)
    # request에 담아주기
    commentPage = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    commentList = commentPaginator.get_page(commentPage)

    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')[:20]
    # 객체를 한 페이지로 자르기
    paginator = Paginator(notification, 5)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    notificationList = paginator.get_page(page)
    return render(request, 'league/league_detail.html', {'countNotification':countNotification, 
    'notificationList':notificationList, 'fnsuser':fnsuser, 'commentList':commentList, 'league':league})

def editLC(request, leagueComment_id):
    error = None
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
    content = request.POST.get('content')
    lgComment = get_object_or_404(LGComment, pk = leagueComment_id)

    if not content:
        error = '내용을 입력해주세요.'

    if not error:
        lgComment.content = content
        lgComment.save()
    
    league = lgComment.post
    comments = LGComment.objects.filter(post = league).order_by('-created')
    # 객체를 한 페이지로 자르기
    commentPaginator = Paginator(comments, 15)
    # request에 담아주기
    commentPage = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    commentList = commentPaginator.get_page(commentPage)
    return render(request, 'league/league_detail.html', {'league':league, 'error':error,
    'commentList':commentList, 'countNotification':countNotification, 'notificationList':notificationList, 'fnsuser':fnsuser})

def leagueReply_write(request):
    error = None
    if request.method == 'POST':
        fnsuser = get_object_or_404(FNSUser, pk = request.session.get('userId'))    
        league_id = request.POST.get('league_id', '').strip()
        league = get_object_or_404(League, pk=league_id)
        comment_id = request.POST.get('comment_id')
        lgComment = get_object_or_404(LGComment, pk = comment_id)

        comments = LGComment.objects.filter(post = league.id).order_by('-created')
        content = request.POST.get('content', '').strip()

        if not content:
            error = '댓글을 입력해주세요.'

        if not error:
            commentReply = LeagueReply.objects.create(user=fnsuser, post= league, 
            content= content, comment=lgComment)

            newNotification = Notification.objects.create(
            creator = get_object_or_404(FNSUser, pk=request.session.get('userId')),
            to = lgComment.user,
            notification_type = Notification.leagueReply,
            league = league,
            lgComment = lgComment
            )
           
            newNotification.leagueReplyText()
            newNotification.save()

            
            # return redirect(reverse('personalDetail', kwargs={'personal_id':personalMatching_id}))

    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')[:20]
    # 객체를 한 페이지로 자르기
    paginator = Paginator(notification, 5)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    notificationList = paginator.get_page(page)

    comments = LGComment.objects.filter(post = league).order_by('-created')
    # 객체를 한 페이지로 자르기
    commentPaginator = Paginator(comments, 15)
    # request에 담아주기
    commentPage = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    commentList = commentPaginator.get_page(commentPage)

    return render(request, 'league/league_detail.html', {'countNotification':countNotification, 
    'notificationList':notificationList, 'error':error, 'fnsuser':fnsuser, 'commentList':commentList, 'league':league})

def deleteLeagueReply(request, reply_id):
    leagueReply = get_object_or_404(LeagueReply, pk=reply_id)
    league = leagueReply.post
    leagueReply.delete()

    fnsuser = get_object_or_404(FNSUser, pk = request.session.get('userId'))
    comments = LGComment.objects.filter(post = league).order_by('-created')
    # 객체를 한 페이지로 자르기
    commentPaginator = Paginator(comments, 15)
    # request에 담아주기
    commentPage = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    commentList = commentPaginator.get_page(commentPage)

    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')[:20]
    # 객체를 한 페이지로 자르기
    paginator = Paginator(notification, 5)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    notificationList = paginator.get_page(page)   
    return render(request, 'league/league_detail.html', {'countNotification':countNotification, 
    'notificationList':notificationList, 'fnsuser':fnsuser, 'commentList':commentList, 'league':league})

def editLeagueReply(request, reply_id):
    error = None
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
    content = request.POST.get('content')
    leagueReply = get_object_or_404(LeagueReply, pk = reply_id)

    if not content:
        error = '내용을 입력해주세요.'

    if not error:
        leagueReply.content = content
        leagueReply.save()

    league = leagueReply.post
    comments = LGComment.objects.filter(post = league).order_by('-created')
    # 객체를 한 페이지로 자르기
    commentPaginator = Paginator(comments, 15)
    # request에 담아주기
    commentPage = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    commentList = commentPaginator.get_page(commentPage)
    return render(request, 'league/league_detail.html', {'league':league, 'error':error,
    'commentList':commentList, 'countNotification':countNotification, 'notificationList':notificationList, 'fnsuser':fnsuser})

        

    
        