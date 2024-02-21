from django.db import models
from django.utils import timezone


class AdminInfo(models.Model):
    userid = models.CharField(max_length=18, primary_key=True, unique=True, null=False, verbose_name='身份证')
    username = models.CharField(max_length=10, verbose_name='姓名')
    password = models.CharField(max_length=16, verbose_name='密码')
    phone = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    gender = models.IntegerField(choices=((0, '男'), (1, '女')), default=0, verbose_name='性别')

    class Meta:
        db_table = 'network_admin_info'
        verbose_name = '管理员信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.userid


class Bandwidth(models.Model):
    datetime = models.DateTimeField('创建时间', default=timezone.now)
    download_speed = models.FloatField()
    upload_speed = models.FloatField()

    class Meta:
        db_table = 'tb_Bandwidth'
        verbose_name = '流量宽带'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.datetime}:{self.upload_speed}/{self.download_speed}'


class Cpu(models.Model):
    datetime = models.DateTimeField('创建时间', default=timezone.now)
    percent = models.FloatField()

    class Meta:
        db_table = 'tb_CPU'
        verbose_name = 'CPU利用率'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.datetime}: {self.percent}'


class Memory(models.Model):
    datetime = models.DateTimeField('创建时间', default=timezone.now)
    percent = models.FloatField()

    class Meta:
        db_table = 'tb_Memory'
        verbose_name = '内存利用率'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.datetime}: {self.percent}'


class PingResult(models.Model):
    host = models.CharField(max_length=20)
    content = models.TextField()
    datetime = models.DateTimeField('创建时间', default=timezone.now)

    class Meta:
        db_table = 'tb_Ping'
        verbose_name = 'Ping值检测'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.host} - {self.content} - {self.datetime}'
