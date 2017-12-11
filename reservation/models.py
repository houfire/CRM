from django.db import models

class UserInfo(models.Model):
    '''
    用户表
    '''
    name = models.CharField(verbose_name="姓名",max_length=32)
    pwd = models.CharField(verbose_name="密码",max_length=32)

    def __str__(self):
        return self.name


class Room(models.Model):
    '''
    会议室
    '''
    title = models.CharField(verbose_name="会议室名字",max_length=32)
    def __str__(self):
        return self.title

class Time(models.Model):
    '''
    时间段表
    '''
    title = models.CharField(verbose_name="时间段",max_length=32)

    def __str__(self):
        return self.title


class Date(models.Model):
    '''
    日期表
    '''
    datetime = models.DateTimeField(verbose_name="日期")
    def __str__(self):
        return self.datetime.strftime("%H-%m-%d")

class Select(models.Model):
    '''
    选择
    '''
    user = models.ForeignKey(to=UserInfo)
    room = models.ForeignKey(to=Room)
    time = models.ForeignKey(to=Time)
    data = models.ForeignKey(to=Date)

    def __str__(self):
        return  self.user.name
