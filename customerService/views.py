from django.shortcuts import render, get_object_or_404
from account.models import FNSUser
from notification.models import Notification
from django.core.paginator import Paginator
from .models import CS
# Create your views here.

def cs(request):
    fnsuser = get_object_or_404(FNSUser, pk = request.session.get('userId'))
    notification = fnsuser.to.all().order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    cs = CS.objects.all().order_by('-created')
    # 객체를 한 페이지로 자르기
    paginator = Paginator(cs, 10)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    csList = paginator.get_page(page)

    return render(request, 'cs.html', {'fnsuser':fnsuser, 'notification':notification, 
    'csList':csList, 'cs':cs , 'countNotification':countNotification})

def csEditform(request, cs_id):
    fnsuser = get_object_or_404(FNSUser, pk = request.session.get('userId'))
    notification = fnsuser.to.all().order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    cs = get_object_or_404(CS, pk=cs_id)
    return render(request, 'csEdit.html', {'cs':cs, 'fnsuser':fnsuser, 'notification':notification,'countNotification':countNotification})
        
def csEdit(request, cs_id):
    fnsuser = get_object_or_404(FNSUser, pk = request.session.get('userId'))
    notification = fnsuser.to.all().order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    cs = CS()
    cs.title = request.POST.get('title')
    cs.content = request.POST.get('content')
    cs.user = fnsuser
    cs.email = fnsuser.email
    cs.save()
    cs = CS.objects.all().order_by('-created')
    paginator = Paginator(cs, 10)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    csList = paginator.get_page(page)
    message = '성공적으로 글이 수정되었습니다.'
    return render(request, 'cs.html', {'fnsuser':fnsuser,'notification':notification,
    'cs':cs, 'countNotification':countNotification, 'csList':csList, 'message':message})
    

def csNew(request):
    fnsuser = get_object_or_404(FNSUser, pk = request.session.get('userId'))
    notification = fnsuser.to.all().order_by('-created')
    countNotification = notification.filter(userCheck = False).count()

    if request.method == 'GET':
        return render(request, 'csNew.html', {'fnsuser':fnsuser,'notification':notification,'countNotification':countNotification})
    if request.method == 'POST':
        cs = CS()
        cs.title = request.POST.get('title')
        cs.content = request.POST.get('content')
        cs.user = fnsuser
        cs.email = fnsuser.email
        cs.save()
        cs = CS.objects.all().order_by('-created')
        paginator = Paginator(cs, 10)
        # request에 담아주기
        page = request.GET.get('page')
        # request된 페이지를 얻어온 뒤 return 해 준다.
        csList = paginator.get_page(page)
        message = '성공적으로 글이 작성되었습니다.'
        return render(request, 'cs.html', {'fnsuser':fnsuser,'notification':notification,
        'cs':cs, 'countNotification':countNotification, 'csList':csList, 'message':message})
    
def csDetail(request, cs_id):
    fnsuser = get_object_or_404(FNSUser, pk = request.session.get('userId'))
    notification = fnsuser.to.all().order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    cs = get_object_or_404(CS, pk = cs_id)
    if cs.user != fnsuser:
        cs = CS.objects.all().order_by('-created')
        paginator = Paginator(cs, 10)
        # request에 담아주기
        page = request.GET.get('page')
        # request된 페이지를 얻어온 뒤 return 해 준다.
        csList = paginator.get_page(page)
        message = '글 작성자만 확인할 수 있습니다.'
        return render(request, 'cs.html', {'fnsuser':fnsuser,'notification':notification,
        'cs':cs, 'countNotification':countNotification, 'csList':csList, 'message':message})
    
    

    return render(request, 'csDetail.html', {'fnsuser':fnsuser,'notification':notification,
    'countNotification':countNotification, 'cs':cs})

def csDelete(request, cs_id):
    fnsuser = get_object_or_404(FNSUser, pk = request.session.get('userId'))
    notification = fnsuser.to.all().order_by('-created')
    countNotification = notification.filter(userCheck = False).count()
    cs = get_object_or_404(CS, pk = cs_id)
    cs.delete()
    cs = CS.objects.all().order_by('-created')
    paginator = Paginator(cs, 10)
    # request에 담아주기
    page = request.GET.get('page')
    # request된 페이지를 얻어온 뒤 return 해 준다.
    csList = paginator.get_page(page)
    message = '성공적으로 삭제하셨습니다.'
    return render(request, 'cs.html', {'fnsuser':fnsuser,'notification':notification, 'message':message,
    'countNotification':countNotification, 'cs':cs, 'csList':csList})

    
