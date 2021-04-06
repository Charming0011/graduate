from django.shortcuts import render,HttpResponse,redirect
from .models import *
from django.contrib import messages
import datetime
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.db.models import Q
from equipment import views

###################设备信息管理######################

def equinfo(request):
    username = request.session.get('username', '')
    if not username:
        messages.warning(request, '请登录！')
        return render(request, 'adlogin.html')
    equ_list=Equinfo.objects.all()
    stat_content=views.fenye(request,equ_list,10)
    stat_content['username']=username

    # paginator = Paginator(equ_list, 10)
    # pag_num = paginator.num_pages
    # curuent_page_num = int(request.GET.get('page', 1))  # 获取当前页数,默认为1
    # curuent_page = paginator.page(curuent_page_num)
    # # print(curuent_page)
    # if pag_num < 11:  # 判断当前页是否小于11个
    #     pag_range = paginator.page_range
    # elif pag_num > 11:
    #     if curuent_page_num < 6:
    #         pag_range = range(1, 11)
    #     elif curuent_page_num > (paginator.num_pages) - 5:
    #         pag_range = range(pag_num - 9, pag_num + 1)
    #     else:
    #         pag_range = range(curuent_page_num - 5, curuent_page_num + 5)  # 当前页+5大于最大页数时
    # # print(type(remind.get(id=1).content))
    # # 进行分页操作
    # # 定义返回字典
    # stat_content = {'username': username,'equ_list':equ_list,"pagintor": paginator, "current_Page": curuent_page, "current_Page_num": curuent_page_num,"pag_range": pag_range}

    return render(request, 'equinfo.html', stat_content)

def equinfosearch(request):
    username = request.session.get('username', '')
    if not username:
        messages.warning(request, '请登录！')
        return render(request, 'adlogin.html')
    searchad=request.GET.get('searchad')
    print(searchad)
    equ_list=Equinfo.objects.filter(model=searchad)
    stat_content=views.fenye(request,equ_list,10)
    stat_content['username']=username
    # paginator = Paginator(equ_list, 10)
    # pag_num = paginator.num_pages
    # curuent_page_num = int(request.GET.get('page', 1))  # 获取当前页数,默认为1
    # curuent_page = paginator.page(curuent_page_num)
    # # print(curuent_page)
    # if pag_num < 11:  # 判断当前页是否小于11个
    #     pag_range = paginator.page_range
    # elif pag_num > 11:
    #     if curuent_page_num < 6:
    #         pag_range = range(1, 11)
    #     elif curuent_page_num > (paginator.num_pages) - 5:
    #         pag_range = range(pag_num - 9, pag_num + 1)
    #     else:
    #         pag_range = range(curuent_page_num - 5, curuent_page_num + 5)  # 当前页+5大于最大页数时
    # # print(type(remind.get(id=1).content))
    # # 进行分页操作
    # # 定义返回字典
    # stat_content = {'username': username, 'equ_list': equ_list, "pagintor": paginator, "current_Page": curuent_page,
    #                 "current_Page_num": curuent_page_num, "pag_range": pag_range}

    return render(request, 'equinfo.html', stat_content)




def equmansearch(request):
    username = request.session.get('username', '')
    if not username:
        messages.warning(request, '请登录！')
        return render(request, 'adlogin.html')
    if request.method=='GET':
        nid=request.GET.get('nid')
        man_list = Mainfo.objects.filter(id_ma=nid).values(
            'id',
            'id_ma__id',
            'id_ma__location',
            'id_ma__model',
            'subtime',
            'systemrun',
            'adout',
            'othset',
            'mouse',
            'keyboard',
            'screen',
            'engine',
            'note'
        )
        stat=views.fenye(request,man_list,10)
        stat['username']=username
        # paginator = Paginator(man_list, 10)
        # pag_num = paginator.num_pages
        # curuent_page_num = int(request.GET.get('page', 1))  # 获取当前页数,默认为1
        # curuent_page = paginator.page(curuent_page_num)
        # if pag_num < 11:  # 判断当前页是否小于11个
        #     pag_range = paginator.page_range
        # elif pag_num > 11:
        #     if curuent_page_num < 6:
        #         pag_range = range(1, 11)
        #     elif curuent_page_num > (paginator.num_pages) - 5:
        #         pag_range = range(pag_num - 9, pag_num + 1)
        #     else:
        #         pag_range = range(curuent_page_num - 5, curuent_page_num + 5)
        # stat = {
        #     'username': username,
        #     'man_list': man_list,
        #     "pagintor": paginator,
        #     "current_Page": curuent_page,
        #     "current_Page_num": curuent_page_num,
        #     "pag_range": pag_range
        # }
        return render(request, 'equman.html', stat)


def equinfodel(request):
    equid=request.GET.get('nid')
    equ=Equinfo.objects.filter(id=equid).delete()
    return redirect('/index/equinfo/')

def equinfoch(request):
    if request.method=='GET':
        return render(request,'equinfo.html')
    else:
        equid=request.POST.get('equid')
        model = request.POST.get('model')
        sys = request.POST.get('systype')
        outdate = request.POST.get('outdate')
        location = request.POST.get('location')
        beizhu = request.POST.get('beizhu')
        # print(type(sys))
        # print(sys)
        # print(equid)
        ret={'status':True,'errormsg':None}
        try:
            equinfo=Equinfo.objects.filter(id=equid).update(model=model,systype=sys,outdate=outdate,location=location,beizhu=beizhu)

        except Exception as e:
            ret['status']=False
            # ret['errormsg']=e
            ret['errormsg']='处理异常！'
        return HttpResponse(str(ret))


def addequinfo(request):
    username = request.session.get('username', '')
    if not username:
        messages.warning(request, '请登录！')
        return render(request, 'adlogin.html')
    if request.method=='GET':
        return render(request,'addequinfo.html',{'username':username})
    else:
        model=request.POST.get('model')
        sys=request.POST.get('systype')
        outdate=request.POST.get('outdate')
        location=request.POST.get('location')
        beizhu=request.POST.get('beizhu')
        # print(model+sys+outdate+location+beizhu)
        try:
            equinfo=Equinfo.objects.create(model=model,systype=sys,outdate=outdate,location=location,beizhu=beizhu)
            return redirect('/index/equinfo/')
        except Exception as e:
            return render(request,'addequinfo.html',{'msg':'处理异常，请重试！'})

###################设备维护记录管理######################

def equman(request):
    username = request.session.get('username', '')
    if not username:
        messages.warning(request, '请登录！')
        return render(request, 'adlogin.html')

    man_list=Mainfo.objects.values(
        'id',
        'id_ma__id',
        'id_ma__location',
        'id_ma__model',
        'subtime',
        'systemrun',
        'adout',
        'othset',
        'mouse',
        'keyboard',
        'screen',
        'engine',
        'note'
    ).order_by('-id')
    stat=views.fenye(request,man_list,10)
    stat['username']=username
    # paginator = Paginator(man_list, 10)
    # pag_num = paginator.num_pages
    # curuent_page_num = int(request.GET.get('page', 1))  # 获取当前页数,默认为1
    # curuent_page = paginator.page(curuent_page_num)
    # if pag_num < 11:  # 判断当前页是否小于11个
    #     pag_range = paginator.page_range
    # elif pag_num > 11:
    #     if curuent_page_num < 6:
    #         pag_range = range(1, 11)
    #     elif curuent_page_num > (paginator.num_pages) - 5:
    #         pag_range = range(pag_num - 9, pag_num + 1)
    #     else:
    #         pag_range = range(curuent_page_num - 5, curuent_page_num + 5)
    # stat={
    #     'username': username,
    #     'man_list':man_list,
    #     "pagintor": paginator,
    #     "current_Page": curuent_page,
    #     "current_Page_num": curuent_page_num,
    #     "pag_range": pag_range
    # }
    return render(request,'equman.html',stat)

def equmanbeizhu(request):

    manid=request.POST.get('manid')
    beizhu=request.POST.get('beizhu')
    print(manid)
    print(beizhu)
    flag=True
    try:
        man=Mainfo.objects.filter(id_ma=manid).update(beizhu=beizhu)
        print(man[0].beizhu)
        return HttpResponse(flag)
    except Exception as e:
        flag=False
        return HttpResponse(flag)


def equmandel(request):
    manid = request.GET.get('nid')
    # print(manid)
    man = Mainfo.objects.filter(id_ma=manid).delete()
    return redirect('/index/equman/')

def mansearch(request):
    username = request.session.get('username', '')
    if not username:
        messages.warning(request, '请登录！')
        return render(request, 'adlogin.html')
    date=request.GET.get('date')
    man=Mainfo.objects.filter(subtime__contains=date).values(
            'id_ma__id',
            'id_ma__location',
            'id_ma__model',
            'subtime',
            'systemrun',
            'adout',
            'othset',
            'mouse',
            'keyboard',
            'screen',
            'engine',
            'note'
        )
    stat_content=views.fenye(request,man,10)
    stat_content['username']=username
    # paginator = Paginator(man, 10)
    # pag_num = paginator.num_pages
    # curuent_page_num = int(request.GET.get('page', 1))  # 获取当前页数,默认为1
    # curuent_page = paginator.page(curuent_page_num)
    # # print(curuent_page)
    # if pag_num < 11:  # 判断当前页是否小于11个
    #     pag_range = paginator.page_range
    # elif pag_num > 11:
    #     if curuent_page_num < 6:
    #         pag_range = range(1, 11)
    #     elif curuent_page_num > (paginator.num_pages) - 5:
    #         pag_range = range(pag_num - 9, pag_num + 1)
    #     else:
    #         pag_range = range(curuent_page_num - 5, curuent_page_num + 5)  # 当前页+5大于最大页数时
    # # print(type(remind.get(id=1).content))
    # # 进行分页操作
    # # 定义返回字典
    # stat_content = {'username': username, "pagintor": paginator, "current_Page": curuent_page,
    #                 "current_Page_num": curuent_page_num, "pag_range": pag_range}

    return render(request, 'equman.html', stat_content)

###################问题设备记录管理######################

def badequ(request):
    username = request.session.get('username', '')
    if not username:
        messages.warning(request, '请登录！')
        return render(request, 'adlogin.html')
    bad_list=Mainfo.objects.filter(stat='1').values(
        'id',
        'id_ma__id',
        'id_ma__model',
        'id_ma__location',
        'note'
    ).order_by('-id')
    stat=views.fenye(request,bad_list,10)
    stat['username']=username
    # paginator = Paginator(bad_list, 10)
    # pag_num = paginator.num_pages
    # curuent_page_num = int(request.GET.get('page', 1))  # 获取当前页数,默认为1
    # curuent_page = paginator.page(curuent_page_num)
    # if pag_num < 11:  # 判断当前页是否小于11个
    #     pag_range = paginator.page_range
    # elif pag_num > 11:
    #     if curuent_page_num < 6:
    #         pag_range = range(1, 11)
    #     elif curuent_page_num > (paginator.num_pages) - 5:
    #         pag_range = range(pag_num - 9, pag_num + 1)
    #     else:
    #         pag_range = range(curuent_page_num - 5, curuent_page_num + 5)
    # stat = {
    #     'username': username,
    #     'bad_list': bad_list,
    #     "pagintor": paginator,
    #     "current_Page": curuent_page,
    #     "current_Page_num": curuent_page_num,
    #     "pag_range": pag_range
    # }
    return render(request, 'badequ.html', stat)

def badequdel(request):
    nid=request.GET.get('nid')

    # print(nid)
    man=Mainfo.objects.filter(id_ma=nid).update(stat='2')
    return redirect('/index/badequ/')

def badsearch(request):
    username = request.session.get('username', '')
    if not username:
        messages.warning(request, '请登录！')
        return render(request, 'adlogin.html')
    nid=request.GET.get('modelid')
    bad=Mainfo.objects.filter(id_ma=nid).values(
        'id_ma__id',
        'id_ma__model',
        'id_ma__location',
        'id_ma__mainfo__note'
    )
    stat=views.fenye(request,bad,10)
    stat['username']=username

    # paginator = Paginator(bad, 10)
    # pag_num = paginator.num_pages
    # curuent_page_num = int(request.GET.get('page', 1))  # 获取当前页数,默认为1
    # curuent_page = paginator.page(curuent_page_num)
    # if pag_num < 11:  # 判断当前页是否小于11个
    #     pag_range = paginator.page_range
    # elif pag_num > 11:
    #     if curuent_page_num < 6:
    #         pag_range = range(1, 11)
    #     elif curuent_page_num > (paginator.num_pages) - 5:
    #         pag_range = range(pag_num - 9, pag_num + 1)
    #     else:
    #         pag_range = range(curuent_page_num - 5, curuent_page_num + 5)
    # stat = {
    #     'username': username,
    #     "pagintor": paginator,
    #     "current_Page": curuent_page,
    #     "current_Page_num": curuent_page_num,
    #     "pag_range": pag_range
    # }
    return render(request, 'badequ.html', stat)