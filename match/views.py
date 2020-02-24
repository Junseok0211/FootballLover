from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import PersonalMatching, TeamMatching, Recruiting, PersonalComment, PersonalReply, TMComment, REComment, League, LGComment, LgPlayerAttendance, LgTeamAttendance, TmAppliedTeam
from .models import TeamReply, RecruitingReply, LeagueReply
from django.views.decorators.http import require_POST
from account.models import FNSUser
from decidedMatch.models import DecidedMatch
from team.models import Team
from notification.models import Notification
from django.core.paginator import Paginator
from datetime import datetime, date
from django.utils.dateformat import DateFormat

# Create your views here.
def home(request):
    today = date.today()
    personalMatching = PersonalMatching.objects.filter(time_from__gt = today).order_by('-time_from')
    teamMatching = TeamMatching.objects.filter(time_from__gt = today, is_applied=False).order_by('-time_from')
    recruiting = Recruiting.objects.filter(time_from__gt = today).order_by('-time_from')
    league = League.objects.order_by('-created').first()
    personal_notice = PersonalMatching.objects.order_by('-created').first()
    user_id = request.session.get('userId')
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

def personal(request):
    if not (request.session.get('userId')):
        personal = PersonalMatching.objects.all().order_by('-created')
        # 객체를 한 페이지로 자르기
        paginator = Paginator(personal, 8)
        # request에 담아주기
        page = request.GET.get('page')
        # request된 페이지를 얻어온 뒤 return 해 준다.
        personalList = paginator.get_page(page)
    
  
        return render(request, 'personal.html', {'personal':personal, 
        'personalList':personalList})

    else:
        personal = PersonalMatching.objects.all().order_by('-created')
        # 객체를 한 페이지로 자르기
        paginator = Paginator(personal, 8)
        # request에 담아주기
        page = request.GET.get('page')
        # request된 페이지를 얻어온 뒤 return 해 준다.
        personalList = paginator.get_page(page)
        
        errormessage = ''
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
        return render(request, 'personal.html', {'countNotification':countNotification, 'personal':personal, 
        'personalList':personalList, 'errormessage':errormessage, 'notificationList':notificationList, 'fnsuser':fnsuser})

def personal_detail(request, personal_id):
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
    is_liked = False

    if personalMatching.attendance.filter(id=request.session.get('userId')).exists():
        is_liked = True

    attendance = personalMatching.attendance.all()
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')[:20]
    # 객체를 한 페이지로 자르기
    paginator = Paginator(notification, 5)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    notificationList = paginator.get_page(page)
    return render(request, 'personal_detail.html', {'countNotification':countNotification, 'commentList':commentList,
    'notificationList':notificationList, 'fnsuser':fnsuser, 'comments':comments, 'personalMatching':personalMatching, 
    'is_liked': is_liked, 'total_attendance': personalMatching.total_attendance(), 'attendance':attendance})

@require_POST
def personalcm_write(request):
    errormessage = None
    if request.method == 'POST':
        fnsuser = get_object_or_404(FNSUser, pk = request.session.get('userId'))    
        personalMatching_id = request.POST.get('personalMatching_id', '').strip()
        personalMatching = get_object_or_404(PersonalMatching, pk=personalMatching_id)
        comments = PersonalComment.objects.filter(post = personalMatching.id).order_by('-created')
        # 객체를 한 페이지로 자르기
        commentPaginator = Paginator(comments, 15)
        # request에 담아주기
        commentPage = request.GET.get('page')
        # request된 페이지를 얻어온 뒤 return 해 준다.
        commentList = commentPaginator.get_page(commentPage)
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
            # return redirect(reverse('personal_detail', kwargs={'personal_id':personalMatching_id}))

    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')[:20]
    # 객체를 한 페이지로 자르기
    paginator = Paginator(notification, 5)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    notificationList = paginator.get_page(page)

    return render(request, 'personal_detail.html', {'countNotification':countNotification, 
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
    return render(request, 'personal_detail.html', {'countNotification':countNotification, 
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
    return render(request, 'personal_detail.html', {'personalMatching':personalMatching, 'errormessage':errormessage,
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
            errormessage = '댓글을 입력해주세요.'

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
            # return redirect(reverse('personal_detail', kwargs={'personal_id':personalMatching_id}))

    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')[:20]
    # 객체를 한 페이지로 자르기
    paginator = Paginator(notification, 5)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    notificationList = paginator.get_page(page)

    return render(request, 'personal_detail.html', {'countNotification':countNotification, 
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
    return render(request, 'personal_detail.html', {'countNotification':countNotification, 
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
    return render(request, 'personal_detail.html', {'personalMatching':personalMatching, 'errormessage':errormessage,
    'commentList':commentList, 'countNotification':countNotification, 'notificationList':notificationList, 'fnsuser':fnsuser})

def personal_new(request):
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
    return render(request, 'personal_new.html', {'countNotification':countNotification, 'notificationList':notificationList, 'fnsuser':fnsuser})

def personal_create(request):
    personalMatching =  PersonalMatching()
    personalMatching.title = request.POST.get('title')
    personalMatching.location = request.POST.get('location')
    time_from = request.POST.get('time_from')
    year = time_from[:4]
    month = time_from[5:7]
    date = time_from[8:10]
    hour = time_from[11:13]
    minute = time_from[14:16]
    startTime = year + '-' + month + '-' + date + ' ' + hour + ':' + minute
    personalMatching.time_from = startTime
    time_to = request.POST.get('time_to')
    endHour = time_to[:2]
    endMin = time_to[3:5]
    endTime = year + '-' + month + '-' + date + ' ' + endHour + ':' + endMin
    personalMatching.time_to = endTime
    personalMatching.number = request.POST.get('number')
    personalMatching.rank = request.POST.get('rank')
    personalMatching.content = request.POST.get('content')
    user_id = request.session.get('userId')
    fnsUser = get_object_or_404(FNSUser, pk = user_id)
    personalMatching.user = fnsUser
    personalMatching.save()

    return redirect(reverse('personal'))

def personal_editForm(request, personal_id):
    personalMatching = get_object_or_404(PersonalMatching, pk = personal_id)
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
        error = '글을 작성한 사용자만 수정할 수 있습니다.'
        return render(request, 'personal.html', {'countNotification':countNotification, 'notificationList':notificationList, 'fnsuser':fnsuser, 'personalList':personalList, 'error':error})
    return render(request, 'personal_editForm.html', {'countNotification':countNotification, 'notificationList':notificationList, 'fnsuser':fnsuser, 'personalMatching':personalMatching})

def personal_edit(request, personal_id):
    personalMatching = get_object_or_404(PersonalMatching, pk=personal_id)
    personalMatching.title = request.POST.get('title')
    personalMatching.location = request.POST.get('location')    
    time_from = request.POST.get('time_from')
    year = time_from[:4]
    month = time_from[5:7]
    date = time_from[8:10]
    hour = time_from[11:13]
    minute = time_from[14:16]
    startTime = year + '-' + month + '-' + date + ' ' + hour + ':' + minute
    personalMatching.time_from = startTime
    time_to = request.POST.get('time_to')
    endHour = time_to[:2]
    endMin = time_to[3:5]
    endTime = year + '-' + month + '-' + date + ' ' + endHour + ':' + endMin
    personalMatching.time_to = endTime
    personalMatching.number = request.POST.get('number')
    personalMatching.rank = request.POST.get('rank')
    personalMatching.content = request.POST.get('content')
    personalMatching.save()

    return redirect('/personal')

def personal_delete(request, personal_id):
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
        return render(request, 'personal.html', {'countNotification':countNotification, 
        'notificationList':notificationList, 'fnsuser':fnsuser, 'personalList':personalList, 'error':error})
    personalMatching.delete()
    return redirect('/personal')
    
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
        return render(request, 'personal_detail.html', {'personalMatching':personalMatching, 
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
        

    return HttpResponseRedirect(reverse('personal_detail', kwargs={'personal_id':personalMatching.id}))


def teamMatching(request):
    if not (request.session.get('userId')):
        teamMatching = TeamMatching.objects.all().filter(is_applied=False).order_by('-created')
        # 객체를 한 페이지로 자르기
        paginator = Paginator(teamMatching, 8)
        # request에 담아주기
        teamPage = request.GET.get('page')
        # request된 페이지를 얻어온 뒤 return 해 준다.
        teamList = paginator.get_page(teamPage)
        return render(request, 'teamMatching/teamMatching.html', {'teamList':teamList})

    else:
        teamMatching = TeamMatching.objects.all().filter(is_applied=False).order_by('-created')

        # 객체를 한 페이지로 자르기
        paginator = Paginator(teamMatching, 8)
        # request에 담아주기
        teamPage = request.GET.get('page')
        # request된 페이지를 얻어온 뒤 return 해 준다.
        teamList = paginator.get_page(teamPage)

        errormessage = ''
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
        if not (request.session.get('userId')):
            errormessage = '로그인을 해주세요.'

        return render(request, 'teamMatching/teamMatching.html', {'countNotification':countNotification, 
        'teamList':teamList, 'notificationList':notificationList, 'fnsuser':fnsuser, 'teamMatching':teamMatching, 'errormessage':errormessage})

def teamMatching_new(request):
    if not (request.session.get('userId')):
        errormessage = '로그인을 해주세요.'
        return render(request, 'login.html', {'errormessage':errormessage})
    fnsuser = get_object_or_404(FNSUser, pk=request.session.get('userId'))
    errormessage = ''
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
        errormessage = '팀에 가입해야 글을 작성할 수 있습니다.'
        
    return render(request, 'teamMatching/teamMatching_new.html', {'countNotification':countNotification, 
    'errormessage':errormessage, 'notificationList':notificationList, 'fnsuser':fnsuser})

def teamMatching_detail(request, teamMatching_id):
    if not (request.session.get('userId')):
        errormessage = '로그인을 해주세요.'
        return render(request, 'login.html', {'errormessage':errormessage})
    teamMatching = get_object_or_404(TeamMatching, pk=teamMatching_id)
    comments = TMComment.objects.filter(post = teamMatching.id).order_by('-created')
    # 객체를 한 페이지로 자르기
    commentPaginator = Paginator(comments, 15)
    # request에 담아주기
    commentPage = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    commentList = commentPaginator.get_page(commentPage)
    fnsuser = get_object_or_404(FNSUser, pk=request.session.get('userId'))
    applied_teams = TmAppliedTeam.objects.filter(match=teamMatching).all()
    errormessage = ''
    is_applied = False
    if not (fnsuser.teamname):
        errormessage = '팀에 먼저 가입해주세요'
        
    elif TmAppliedTeam.objects.filter(team=fnsuser.teamname, match=teamMatching).exists():
        is_applied = True

    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')[:20]
    # 객체를 한 페이지로 자르기
    paginator = Paginator(notification, 5)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    notificationList = paginator.get_page(page)
    return render(request, 'teamMatching/teamMatching_detail.html', {'countNotification':countNotification, 'commentList':commentList,
    'notificationList':notificationList, 'is_applied':is_applied, 'fnsuser':fnsuser, 'comments':comments, 'applied_teams':applied_teams, 'teamMatching':teamMatching, 'errormessage':errormessage})

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
            comments = TMComment.objects.create(user=fnsuser, post_id= teamMatching_id, content= content)
            # 객체를 한 페이지로 자르기
            commentPaginator = Paginator(comments, 15)
            # request에 담아주기
            commentPage = request.GET.get('page')
            # request된 페이지를 얻어온 뒤 return 해 준다.
            commentList = commentPaginator.get_page(commentPage)

            newNotification1 = Notification.objects.create(
            creator = get_object_or_404(FNSUser, pk=request.session.get('userId')),
            to = teamMatching.user,
            notification_type = Notification.teamComment,
            teamMatching = teamMatching
            )
            newNotification1.teamCommentText()
            newNotification1.save()
            # return redirect(reverse('teamMatching_detail', kwargs={'teamMatching_id':teamMatching_id}))

        return render(request, 'teamMatching/teamMatching_detail.html', {'error':error, 'countNotification':countNotification, 
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
    return render(request, 'teamMatching/teamMatching_detail.html', {'countNotification':countNotification, 
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
    return render(request, 'teamMatching/teamMatching_detail.html', {'teamMatching':teamMatching, 'error':error,
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
            # return redirect(reverse('personal_detail', kwargs={'personal_id':personalMatching_id}))

    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')[:20]
    # 객체를 한 페이지로 자르기
    paginator = Paginator(notification, 5)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    notificationList = paginator.get_page(page)

    return render(request, 'teamMatching/teamMatching_detail.html', {'countNotification':countNotification, 
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
    return render(request, 'teamMatching/teamMatching_detail.html', {'countNotification':countNotification, 
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

    return render(request, 'teamMatching/teamMatching_detail.html', {'teamMatching':teamMatching, 'error':error,
    'commentList':commentList, 'countNotification':countNotification, 'notificationList':notificationList, 'fnsuser':fnsuser})


def teamApplication(request, teamMatching_id):
    teamMatching = get_object_or_404(TeamMatching, pk=teamMatching_id)
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

    if fnsuser.teamname.name == None:
        message = '먼저 팀에 가입해주세요.'
        return render(request, 'teamMatching/teamMatching_detail.html', {'countNotification':countNotification, 'commentList':commentList,
        'notificationList':notificationList, 'fnsuser':fnsuser, 'teamMatching':teamMatching, 'message':message})

    if teamMatching.myteam == fnsuser.teamname:
        message = '자기 팀에게 매치신청을 할 수 없습니다.'
        return render(request, 'teamMatching/teamMatching_detail.html', {'countNotification':countNotification, 'commentList':commentList, 
        'notificationList':notificationList, 'fnsuser':fnsuser, 'teamMatching':teamMatching, 'message':message})

    if TmAppliedTeam.objects.filter(match=teamMatching, team=fnsuser.teamname).exists():
        message = '이미 매치 신청을 하셨습니다.'
        return render(request, 'teamMatching/teamMatching_detail.html', {'countNotification':countNotification, 'commentList':commentList,
        'notificationList':notificationList, 'fnsuser':fnsuser, 'teamMatching':teamMatching, 'message':message})

    tmAppliedTeam = TmAppliedTeam.objects.create(team=fnsuser.teamname, match=teamMatching)
    applied_teams = TmAppliedTeam.objects.filter(match=teamMatching).all()
    is_applied = False

    if TmAppliedTeam.objects.filter(match=teamMatching, team=fnsuser.teamname).exists():
        is_applied = True
    message = '성공적으로 매치신청이 이루어졌습니다.'
    
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
    return render(request, 'teamMatching/teamMatching_detail.html', {'countNotification':countNotification, 'commentList':commentList, 
    'notificationList':notificationList, 'fnsuser':fnsuser, 'is_applied':is_applied, 'teamMatching':teamMatching, 'applied_teams':applied_teams, 'message':message})

def teamCancel(request, teamMatching_id):
    fnsuser = get_object_or_404(FNSUser, pk=request.session.get('userId'))
    teamMatching = get_object_or_404(TeamMatching, pk = teamMatching_id)
    TmAppliedTeam.objects.filter(match=teamMatching, team=fnsuser.teamname).delete()
    applied_teams = TmAppliedTeam.objects.filter(match=teamMatching).all()
    comments = TMComment.objects.filter(post = teamMatching.id).order_by('-created')
    # 객체를 한 페이지로 자르기
    commentPaginator = Paginator(comments, 15)
    # request에 담아주기
    commentPage = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    commentList = commentPaginator.get_page(commentPage)
    is_applied = False
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    notification = fnsuser.to.all().exclude(creator=fnsuser).order_by('-created')[:20]
    # 객체를 한 페이지로 자르기
    paginator = Paginator(notification, 5)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    notificationList = paginator.get_page(page)

    if TmAppliedTeam.objects.filter(match=teamMatching, team=fnsuser.teamname).exists():
        is_applied = True

    message = '성공적으로 매치신청을 취소하셨습니다.'
    return render(request, 'teamMatching/teamMatching_detail.html', {'countNotification':countNotification, 
    'notificationList':notificationList, 'is_applied':is_applied, 'fnsuser':fnsuser, 'commentList':commentList, 'applied_teams':applied_teams, 'teamMatching':teamMatching, 'message':message})


def applied_team(request, teamMatching_id):
    teamMatching = get_object_or_404(TeamMatching, pk=teamMatching_id)
    fnsuser = get_object_or_404(FNSUser, pk=request.session.get('userId'))
    applied_teams = TmAppliedTeam.objects.filter(match=teamMatching).all()
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
    is_applied = False
    if applied_teams.filter(team=fnsuser.teamname).exists():
        is_applied = True
    if teamMatching.user != fnsuser:
        error = '글 작성자만 확인할 수 있습니다.'
        return render(request, 'teamMatching/teamMatching_detail.html', {'notificationList':notificationList, 
        'fnsuser':fnsuser, 'error':error, 'commentList':commentList,
        'countNotification':countNotification, 'is_applied':is_applied, 'applied_teams':applied_teams, 'teamMatching':teamMatching})
    
    return render(request, 'teamMatching/applied_team.html', {'countNotification':countNotification, 'notificationList':notificationList,
    'commentList':commentList, 'fnsuser':fnsuser, 'applied_teams':applied_teams, 'teamMatching':teamMatching})

def match_approve(request, teamMatching_id, team_id):
    teamMatching = get_object_or_404(TeamMatching, pk=teamMatching_id)
    team = get_object_or_404(Team, pk=team_id)
    fnsuser = get_object_or_404(FNSUser, pk = request.session.get('userId'))
    TmAppliedTeam.objects.filter(match=teamMatching, team=team).delete()
    applied_team = TmAppliedTeam.objects.filter(match=teamMatching).all()
    teamMatching.vs_team = team
    teamMatching.save()
    
    decidedMatch = DecidedMatch()
    decidedMatch.myTeam = teamMatching.myteam
    decidedMatch.vsTeam = teamMatching.vs_team
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
    message = '성공적으로 매칭이 되었습니다.'

    return render(request, 'teamMatching/applied_team.html', {'countNotification':countNotification, 'notificationList':notificationList, 'fnsuser':fnsuser, 'message':message, 'applied_team':applied_team, 'teamMatching':teamMatching})

def match_deny(request, teamMatching_id, team_id):
    teamMatching = get_object_or_404(TeamMatching, pk=teamMatching_id)
    team = get_object_or_404(Team, pk=team_id)
    fnsuser = get_object_or_404(FNSUser, pk = request.session.get('userId'))
    TmAppliedTeam.objects.filter(match=teamMatching, team=team).delete()
    applied_team = TmAppliedTeam.objects.filter(match=teamMatching).all()
    
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
    message = '매치신청을 거절하였습니다.'

    return render(request, 'teamMatching/applied_team.html', {'countNotification':countNotification, 'notificationList':notificationList, 'fnsuser':fnsuser, 'message':message, 'applied_team':applied_team, 'teamMatching':teamMatching})



def teamMatching_editForm(request, teamMatching_id):
    teamMatching = get_object_or_404(TeamMatching, pk=teamMatching_id)
    fnsuser = get_object_or_404(FNSUser, pk=request.session.get('userId'))
    applied_teams = TmAppliedTeam.objects.filter(match=teamMatching).all()
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
    is_applied = False
    if TmAppliedTeam.objects.filter(match=teamMatching, team=fnsuser.teamname).exists():
        is_applied = True
    if teamMatching.user != fnsuser:
        error = '글을 작성한 사용자만 수정할 수 있습니다.'
        return render(request, 'teamMatching/teamMatching_detail.html', {'notificationList':notificationList, 'fnsuser':fnsuser, 'error':error, 'commentList':commentList,
        'countNotification':countNotification, 'is_applied':is_applied, 'applied_teams':applied_teams, 'teamMatching':teamMatching})
    
   
    return render(request, 'teamMatching/teamMatching_editForm.html', {'countNotification':countNotification, 
    'notificationList':notificationList, 'fnsuser':fnsuser, 'teamMatching':teamMatching})

def teamMatching_delete(request, teamMatching_id):
    teamMatching = get_object_or_404(TeamMatching, pk=teamMatching_id)
    fnsuser = get_object_or_404(FNSUser, pk=request.session.get('userId'))
    applied_teams = TmAppliedTeam.objects.filter(match=teamMatching).all()
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
    is_applied = False
    if TmAppliedTeam.objects.filter(match=teamMatching, team=fnsuser.teamname).exists():
        is_applied = True
    if teamMatching.user != fnsuser:
        error = '글을 작성한 사용자만 삭제할 수 있습니다.'
        return render(request, 'teamMatching/teamMatching_detail.html', {'notificationList':notificationList, 'fnsuser':fnsuser, 'error':error, 'commentList':commentList,
        'countNotification':countNotification, 'is_applied':is_applied, 'applied_teams':applied_teams, 'teamMatching':teamMatching})
    
    teamMatching.delete()
    return redirect('/teamMatching')

def teamMatching_create(request):
    fnsuser = get_object_or_404(FNSUser, pk= request.session.get('userId'))
    team = get_object_or_404(Team, pk = fnsuser.teamname.id)
    
    teamMatching = TeamMatching()
    teamMatching.myteam = team
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
    teamMatching.rank = request.POST.get('rank')
    teamMatching.content = request.POST.get('content')
    teamMatching.save()

    return redirect('/teamMatching')

def teamMatching_edit(request, team_id):
    fnsuser = get_object_or_404(FNSUser, pk= request.session.get('userId'))
    teamMatching = get_object_or_404(TeamMatching, pk=team_id)
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
    teamMatching.rank = request.POST.get('rank')
    teamMatching.content = request.POST.get('content')
    teamMatching.save()

    return redirect('/teamMatching')

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
            return render(request, 'recruiting/recruiting_new.html', {'teams':teams, 'errormessage':errormessage}) 
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
        # return redirect(reverse('personal_detail', kwargs={'personal_id':personalMatching_id}))

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

            
            # return redirect(reverse('personal_detail', kwargs={'personal_id':personalMatching_id}))

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

        

    
        