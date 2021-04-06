from django.shortcuts import render,HttpResponse,redirect
from .models import *
import datetime
from django.db.models import F
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


def adlogin(request):
    return render(request, 'adlogin.html')

#验证用户登陆
#用户登陆

def user_login(request):
    # 模型操作数据库
    if request.method == 'GET':
        return render(request, 'adlogin.html')
    else:

        # 没有session验证的登陆验证

        # u = request.POST.get('user')
        # p = request.POST.get('pwd')
        # t = request.POST.get('logintype')
        # # print(t)
        # if t == 'admin':
        #     #必须加入异常处理，不然会报错终止程序：报错为：admin query DoesNotExist，就是没有在数据库中找到数据从而报错，下面验证学生登陆一样
        #     #或者使用get_object_or_404方法，但是我要自定义异常所以自定义
        #     try:
        #         admin = Admin.objects.get(aduser=u)
        #     except Admin.DoesNotExist:
        #         return render(request, 'Login.html', {'msg': '用户不存在！'})
        #     if admin.adpwd != p:
        #         return render(request,'Login.html',{'msg':'密码错误！'})
        #     else:
        #         return redirect('/index')
        # elif  t=='stu':
        #     try:
        #         stu = Stu.objects.get(stuser=u)
        #     except Stu.DoesNotExist:
        #         return render(request, 'Login.html', {'msg': '用户不存在！'})
        #     if stu.stpwd != p:
        #         # return HttpResponse('用户名或密码错误！')
        #         return render(request, 'Login.html', {'msg': '密码错误！'})
        #     else:
        #         return redirect('/index')
        nid=request.POST.get('userid')
        p = request.POST.get('pwd')
        # t = request.POST.get('logintype')
        # if t=='admin':
        user=Admin.objects.filter(adid=nid,adpwd=p)#相较于上面使用了模型更加简介的处理

        # elif t=='stu':
        # user=Stu.objects.filter(stuser=nid,stpwd=p)

        if user:
            #如果找到user，将名字存入session
            name=user[0].aduser
            request.session['username'] = name
            request.session.set_expiry(0)
            return redirect('/index')
        else:
            messages.warning(request,'用户名或密码错误！')
            return render(request,'adlogin.html')



# 用户登出
def user_logout(request):

    logout(request)
    # return redirect('/login')
    messages.success(request,'登出成功！')
    return render(request, 'adlogin.html')


def stu_login(request):
    if request.method=='GET':
        return render(request,'stulogin.html')
    else:
        userid=request.POST.get('user')
        pwd=request.POST.get('pwd')
        user=Stu.objects.filter(stuser=userid,stpwd=pwd)
        d = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if user:
            request.session['userid']=userid
            username = user[0].stuname
            request.session['stuname'] = username
            Stu.objects.filter(stuser=userid).update(lastime=d)
            #存入近期登陆
            Recent.objects.create(userid=userid,username=username,logindate=d)
            #设置关闭浏览器清除session
            request.session.set_expiry(0)
            return redirect('/submaninfo')
        else:
            messages.warning(request,'用户名或密码错误！')
            return render(request,'stulogin.html')

def submaninfo(request):
    username=request.session.get('stuname','')
    if not username:
        messages.warning(request,'请登录！')
        return render(request,'stulogin.html')
    if request.method=='GET':
        equlist=Equinfo.objects.all()
        stat={'equlist':equlist,'username':username}
        return render(request,'submaninfo.html',stat)

def subadd(request):
    ret={'status':True,'error':None}
    equid=request.POST.get('equid')
    systemrun=request.POST.get('sytemrun')
    adout=request.POST.get('adout')
    otherset=request.POST.get('otherset')
    mouse=request.POST.get('mouse')
    keyboard=request.POST.get('keyboard')
    screen=request.POST.get('screen')
    engine=request.POST.get('engine')
    note=request.POST.get('note')
    d = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    stat=2

    if mouse!='正常' or keyboard!='正常' or screen!='正常' or engine!='正常':
        stat=1
    try:

        man = Mainfo.objects.create(
            id_ma_id=equid,
            systemrun=systemrun,
            adout=adout,
            subtime=d,
            othset=otherset,
            mouse=mouse,
            keyboard=keyboard,
            screen=screen,
            note=note,
            engine=engine,
            stat=stat
        )
        #增加一次提交次数
        nid = request.session.get('userid', '')
        stu = Stu.objects.filter(stuser=nid)
        total=stu[0].total
        total = total + 1
        Stu.objects.filter(stuser=nid).update(total=total)
        return HttpResponse('提交成功！可继续提交其他机器维护记录！')
    except Exception as e:
        ret['status']=False
        ret['error']=e
        return HttpResponse(str(ret))
