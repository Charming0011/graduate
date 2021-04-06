from django.db import models



class Admin(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    adid = models.IntegerField(db_column='adID')
    aduser = models.CharField(max_length=50)
    adpwd = models.CharField(max_length=50, blank=True, null=True)
    authority = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'admin'


class Equinfo(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    model = models.CharField(max_length=50, blank=True, null=True)
    systype = models.CharField(max_length=50, blank=True, null=True)
    outdate = models.CharField(max_length=50, blank=True, null=True)
    location = models.CharField(max_length=50, blank=True, null=True)
    beizhu = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'equinfo'


class Errormach(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    ma = models.ForeignKey('Mainfo', models.DO_NOTHING, blank=True, null=True)
    stat = models.CharField(max_length=50, blank=True, null=True)
    explain = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'errormach'


class Mainfo(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    # subtime=models.DateTimeField(auto_now_add=True)
    # maid=models.ForeignKey
    id_ma=models.ForeignKey('Equinfo',models.DO_NOTHING,db_column='id_ma',blank=True,null=True)#设置外键对应设备id
    subtime=models.CharField(max_length=20,blank=True,null=True)
    systemrun = models.CharField(max_length=50, blank=True, null=True) #整体是否正常，是否运行
    adout = models.CharField(max_length=50, blank=True, null=True)  #广告是否去除
    othset = models.CharField(max_length=50, blank=True, null=True) #其他的设置
    mouse = models.CharField(max_length=50, blank=True, null=True) #鼠标是否正常
    keyboard = models.CharField(max_length=50, blank=True, null=True) #键盘是否正常
    screen = models.CharField(max_length=50, blank=True, null=True) #屏幕是否正常
    engine = models.CharField(max_length=50, blank=True, null=True) #主机是否正常
    note = models.CharField(max_length=200, blank=True, null=True) #学生备注
    beizhu = models.CharField(max_length=200, blank=True, null=True) #管理员备注
    stat = models.CharField(max_length=50, blank=True, null=True) #处理状态，是否处理

    class Meta:
        db_table = 'mainfo'


class Reminder(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    # subtime=models.DateField(auto_now_add=True)
    date = models.CharField(max_length=50, blank=True, null=True)
    who = models.CharField(max_length=50, blank=True, null=True)
    content = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'reminder'


class Stu(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    stuser = models.CharField(max_length=50, blank=True, null=True)
    stuname = models.CharField(max_length=50, blank=True, null=True)
    stpwd = models.CharField(max_length=50, blank=True, null=True)
    lastime = models.CharField(max_length=50, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)


    class Meta:
        db_table = 'stu'

class Recent(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    userid = models.CharField(db_column='userID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(max_length=20, blank=True, null=True)
    logindate = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'recent'



