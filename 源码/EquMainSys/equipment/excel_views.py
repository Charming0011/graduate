from django.shortcuts import render,HttpResponse,redirect
from django.http import FileResponse
from django.db import transaction
from .models import *
import xlwt
import xlrd
import time
from datetime import datetime
from django.contrib import messages
from io import BytesIO


"""
#上传excel存入本地
url = settings.BASE_DIR + '/static/files/' + file.name
    with open(url, 'wb')as f:
        for data in file.chunks():
            f.write(data)
"""
def turnstr(sheet):
    result=[]
    nrows=sheet.nrows
    ncols=sheet.ncols
    for i in range(1, nrows):  # 指定从1开始，到最后一列，跳过表头
        for j in range(ncols):
            ctype = sheet.cell(i,j).ctype  # 判断python读取的返回类型  0 --empty,1 --string, 2 --number(都是浮点), 3 --date, 4 --boolean, 5 --error
            con = sheet.cell(i, j).value  # 获取单元格的值
            if ctype == 2:
                con = str(int(con))# 将浮点转换成整数再转换成字符串
                # print(con)
            result.append(con)
    return result


def download(request):
    filename=request.GET.get('filename')
    file = open('static/files/'+filename, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename='+filename
    return response





###############操作数据导入导出excel##################

def adminexcadd(request):
    file=request.FILES.get('file')
    count=0
    if file:
        readbook = xlrd.open_workbook(filename=None, file_contents=file.read())
        # 打开第一张表（一个Excel文件可以有多张表）
        sheet = readbook.sheet_by_index(0)
        #获取行数
        nrows = sheet.nrows
        #获取列数
        ncols=sheet.ncols
        if ncols!=4:
            messages.warning(request,'请按要求添加,详情按帮助。')
            return redirect('/index/addadmin/')
        try:

            with transaction.atomic():
                for x in range(1, nrows):#跳过表头
                    admin=[]
                    row = sheet.row_values(x)#一行的值，列表
                    for y in range(ncols):
                        ctype = sheet.cell(x, y).ctype# 判断python读取的返回类型  0 --empty,1 --string, 2 --number(都是浮点), 3 --date, 4 --boolean, 5 --error
                        con=sheet.cell(x,y).value
                        if ctype==2:
                            con=str(int(con))
                        admin.append(con)
                    Admin.objects.create(
                        adid=admin[0],
                        aduser=admin[1],
                        adpwd=admin[2],
                        authority=admin[3]
                    )
                    count+=1
        except Exception as e:
                messages.warning(request, e)
                return redirect('/index/addadmin/')
        messages.success(request,'添加成功！共插入%d行数据'%(count))
        return redirect('/index/adminman/')
    else:
        messages.warning(request,'导入文件不能为空！')
        return redirect('/index/addstu/')


def stuexcadd(request):
    stat = {}
    # if request.method=="post":
    file = request.FILES.get('file')
    count=0
    if file:
        readbook = xlrd.open_workbook(filename=None, file_contents=file.read())
        # 打开第一张表（一个Excel文件可以有多张表）
        sheet = readbook.sheet_by_index(0)
        #获取行数
        nrows = sheet.nrows
        #获取列数
        ncols=sheet.ncols
        if ncols!=3:
            messages.warning(request,'请按要求添加,详情按帮助。')
            return redirect('/index/addstu/')
        try:

            with transaction.atomic():
                for x in range(1, nrows):#跳过表头
                    stu=[]
                    row = sheet.row_values(x)#一行的值，列表
                    for y in range(ncols):
                        ctype = sheet.cell(x, y).ctype# 判断python读取的返回类型  0 --empty,1 --string, 2 --number(都是浮点), 3 --date, 4 --boolean, 5 --error
                        con=sheet.cell(x,y).value
                        if ctype==2:
                            con=str(int(con))
                        stu.append(con)
                    Stu.objects.create(
                        stuser=stu[0],
                        stuname=stu[1],
                        stpwd=stu[2]
                    )
                    count+=1
        except Exception as e:
                messages.warning(request, e)
                return redirect('/index/addstu/')
        messages.success(request,'添加成功！共插入%d行数据'%(count))
        return redirect('/index/stuman/')
    else:
        messages.warning(request,'导入文件不能为空！')
        return redirect('/index/addstu/')

def equinfoexcadd(request):
    file = request.FILES.get('file')
    count = 0
    if file:
        readbook = xlrd.open_workbook(filename=None, file_contents=file.read())
        # 打开第一张表（一个Excel文件可以有多张表）
        sheet = readbook.sheet_by_index(0)
        # 获取行数
        nrows = sheet.nrows
        # 获取列数
        ncols = sheet.ncols
        if ncols !=5:
            messages.warning(request, '请按要求添加,详情按帮助。')
            return redirect('/index/addequinfo/')
        try:

            with transaction.atomic():
                for x in range(1, nrows):  # 跳过表头
                    equ = []
                    row = sheet.row_values(x)  # 一行的值，列表
                    for y in range(ncols):
                        ctype = sheet.cell(x,y).ctype  # 判断python读取的返回类型  0 --empty,1 --string, 2 --number(都是浮点), 3 --date, 4 --boolean, 5 --error
                        con = sheet.cell(x, y).value
                        if ctype == 2:
                            con = str(int(con))
                        equ.append(con)
                    Equinfo.objects.create(
                        model=equ[0],
                        systype=equ[1],
                        outdate=equ[2],
                        location=equ[3],
                        beizhu=equ[4]
                    )
                    count += 1
        except Exception as e:
            messages.warning(request, e)
            return redirect('/index/addequinfo/')
        messages.success(request, '添加成功！共插入%d行数据' % (count))
        return redirect('/index/equinfo/')
    else:
        messages.warning(request, '导入文件不能为空！')
        return redirect('/index/addequinfo/')


# 导出excel数据
def export_excel(request):
    # 设置HTTPResponse的类型
    filename=request.GET.get('filename')
    response = HttpResponse(content_type='application/vnd.ms-excel')
    # response = HttpResponse(content_type='.xlsx,.xls,.csv')
    response['Content-Disposition'] = 'attachment;filename='+filename+'.xls'
    # 创建一个文件对象
    wb = xlwt.Workbook(encoding='utf8')
    # 创建一个sheet对象
    sheet = wb.add_sheet('order-sheet')
    # 设置文件头的样式,这个不是必须的可以根据自己的需求进行更改
    style_heading = xlwt.easyxf("""
            font:
                name Arial,
                colour_index white,
                bold on,
                height 0xA0;
            align:
                wrap off,
                vert center,
                horiz center;
            pattern:
                pattern solid,
                fore-colour 0x19;
            borders:
                left THIN,
                right THIN,
                top THIN,
                bottom THIN;
            """
                                )
    if filename=='stu':
        # 写入文件标题
        sheet.write(0,0,'编号',style_heading)
        sheet.write(0,1,'学号',style_heading)
        sheet.write(0,2,'姓名',style_heading)
        sheet.write(0,3,'密码',style_heading)
        sheet.write(0,4,'上次登陆时间',style_heading)
        sheet.write(0,5,'总计提交次数',style_heading)

        # 写入数据
        data_row = 1
        stu=Stu.objects.all()
        for i in stu:
            # lastime=i.lastime.strftime('%Y-%m-%d')
            sheet.write(data_row, 0, i.id)
            sheet.write(data_row, 1, i.stuser)
            sheet.write(data_row, 2, i.stuname)
            sheet.write(data_row, 3, i.stpwd)
            sheet.write(data_row, 4, i.lastime)
            sheet.write(data_row, 5, i.total)
            data_row+=1

        # 写出到IO
        output = BytesIO()
        wb.save(output)
        # 重新定位到开始
        output.seek(0)
        response.write(output.getvalue())
        return response
    elif filename=='equ':
        sheet.write(0, 0, '编号', style_heading)
        sheet.write(0, 1, '型号', style_heading)
        sheet.write(0, 2, '系统类型', style_heading)
        sheet.write(0, 3, '出厂日期', style_heading)
        sheet.write(0, 4, '摆放地点', style_heading)
        sheet.write(0, 5, '备注', style_heading)
        data_row = 1
        equ=Equinfo.objects.all()
        for i in equ:
            sheet.write(data_row, 0, i.id)
            sheet.write(data_row, 1, i.model)
            sheet.write(data_row, 2, i.systype)
            sheet.write(data_row, 3, i.outdate)
            sheet.write(data_row, 4, i.location)
            sheet.write(data_row, 5, i.beizhu)
            data_row += 1
        output = BytesIO()
        wb.save(output)
        # 重新定位到开始
        output.seek(0)
        response.write(output.getvalue())
        return response
    else:
        sheet.write(0, 0, '编号', style_heading)
        sheet.write(0, 1, '用户工号', style_heading)
        sheet.write(0, 2, '姓名', style_heading)
        sheet.write(0, 3, '密码', style_heading)
        sheet.write(0, 4, '用户权限', style_heading)
        data_row = 1
        admin=Admin.objects.all()
        for i in admin:
            sheet.write(data_row, 0, i.id)
            sheet.write(data_row, 1, i.adid)
            sheet.write(data_row, 2, i.aduser)
            sheet.write(data_row, 3, i.adpwd)
            sheet.write(data_row, 4, i.authority)
            data_row += 1
        output = BytesIO()
        wb.save(output)
        # 重新定位到开始
        output.seek(0)
        response.write(output.getvalue())
        return response