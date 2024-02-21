from django.db import models


# Create your models here.

class UserInfo(models.Model):
    userid = models.CharField(max_length=18, primary_key=True, unique=True, null=False, verbose_name='身份证')
    username = models.CharField(max_length=10, verbose_name='姓名')
    password = models.CharField(max_length=16, verbose_name='密码')
    email = models.EmailField(max_length=465, verbose_name='邮箱')
    phone = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    gender = models.IntegerField(choices=((0, '男'), (1, '女')), default=0, verbose_name='性别')
    address = models.ForeignKey('AddressInfo', on_delete=models.CASCADE, verbose_name='住房号码')

    class Meta:
        db_table = 'user_info'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.userid


class AddressInfo(models.Model):
    address = models.IntegerField(primary_key=True, null=False, unique=True, default=0, verbose_name='住房号码')
    water = models.IntegerField(verbose_name='水费')
    electricity = models.IntegerField(verbose_name='电费')
    gas = models.IntegerField(verbose_name='燃气费')

    class Meta:
        db_table = 'address_info'
        verbose_name = '住房信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.address}号住房'
