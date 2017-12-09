from django.db import models

class UserInfo(models.Model):
    '''
    用户表
    '''
    name = models.CharField(verbose_name="姓名",max_length=32)
    pwd = models.CharField(verbose_name="密码",max_length=32)


class Room(models.Model):
    '''
    会议室
    '''
