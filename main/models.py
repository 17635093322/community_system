from django.db import models


class Messages(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    sender_name = models.CharField(max_length=40)
    content = models.TextField(null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    is_delete = models.BooleanField(default=False, verbose_name="删除标记")

    class Meta:
        db_table = 'messages'
        verbose_name = '社区消息通知'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.sender_name}-{self.create_time}'


class AdminInfo(models.Model):
    userid = models.CharField(max_length=18, primary_key=True, unique=True, null=False, verbose_name='身份证')
    username = models.CharField(max_length=10, verbose_name='姓名')
    password = models.CharField(max_length=16, verbose_name='密码')
    phone = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    gender = models.IntegerField(choices=((0, '男'), (1, '女')), default=0, verbose_name='性别')

    class Meta:
        db_table = 'parking_admin_info'
        verbose_name = '管理员信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.userid
