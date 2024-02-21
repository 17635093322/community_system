# jinja2_env.py
from jinja2 import Environment
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse


def jinja2_environment(**options):
    # 创建环境对象
    env = Environment(**options)
    # 自定义语法:{{ static('静态文件相对路径') }} {{url('路由的命名空间')}}
    env.globals.update({
        # 获取静态文件的相对路径
        'static': staticfiles_storage.url,
        # 重定向
        'url': reverse,
    })
    return env