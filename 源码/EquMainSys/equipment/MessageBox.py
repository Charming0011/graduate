from django.contrib import messages

#########后端控制弹窗提醒#############

def success(request,str):
    messages.warning(request, str)




