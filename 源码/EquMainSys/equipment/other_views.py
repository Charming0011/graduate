from django.shortcuts import render,HttpResponse,redirect
from .models import *
import datetime
from equipment import views



###################处理近期登陆情况#####################
def recent(request):
    username = request.session.get('username', '')
    if not username:
        return render(request, 'Login.html', {'msg': '请登陆！'})
    rec=Recent.objects.order_by('-id')
    stat_content=views.fenye(request,rec,10)
    stat_content['username']=username

    return render(request,'recent.html',stat_content)

def recentdel(request):
    nid=request.GET.get('nid')
    rc=Recent.objects.filter(id=nid).delete()
    return redirect('/index/recent/')


def recentsearch(request):
    username = request.session.get('username', '')
    if not username:
        return render(request, 'Login.html', {'msg': '请登陆！'})
    user=request.GET.get('username')
    rec=Recent.objects.filter(username=user)
    stat_content=views.fenye(request,rec,10)
    stat_content['username']=username
    return render(request, 'recent.html', stat_content)

###################处理提醒事项#####################

def remindman(request):
    username = request.session.get('username', '')
    if not username:
        return render(request, 'Login.html', {'msg': '请登陆！'})

    rem_list = Reminder.objects.order_by('-id')
    stat_content=views.fenye(request,rem_list,10)
    stat_content['username']=username

    return render(request, 'remindman.html', stat_content)


def remindch(request):
    nid=request.POST.get('nid')
    content=request.POST.get('content')
    print(nid)
    print(content)
    rem=Reminder.objects.filter(id=nid).update(content=content)
    return HttpResponse('ok')

def remindel(request):
    nid=request.GET.get('nid')
    rem=Reminder.objects.filter(id=nid).delete()
    return redirect('/index/remindman/')

def addremind(request):
    username = request.session.get('username', '')
    if not username:
        return render(request, 'Login.html', {'msg': '请登陆！'})
    if request.method=='GET':
        return render(request,'addremind.html',{'username':username})
    d = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    content=request.POST.get('content')
    if not content:
        return render(request,'addremind.html',{'msg':'字段不能为空！'})
    try:
        rem=Reminder.objects.create(date=d,who=username,content=content)
        return redirect('/index/remindman/')
    except Exception as e:

        return render(request,'addremind.html',{'msg':'处理异常！'})

def remindsearch(request):
    username = request.session.get('username', '')
    if not username:
        return render(request, 'Login.html', {'msg': '请登陆！'})
    searchd=request.GET.get('date')
    # print(searchd)
    rem=Reminder.objects.filter(date__contains=searchd)

    stat_content=views.fenye(request,rem,10)
    stat_content['username']=username

    return render(request, 'remindman.html', stat_content)