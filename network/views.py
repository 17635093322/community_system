from django.shortcuts import render
from django.views import View
from network.models import *
from django_redis import get_redis_connection
from django.http import HttpResponse
import json
from datetime import timedelta

redis_conn_session = get_redis_connection('session')
pl_session = redis_conn_session.pipeline()

redis_conn_network = get_redis_connection('network')
pl_network = redis_conn_network.pipeline()


def get_data():
    try:
        datetimes = redis_conn_network.get('datetimes').decode()
        download_speed = redis_conn_network.get('download_speed').decode()
        upload_speed = redis_conn_network.get('upload_speed').decode()
        cpu_data = redis_conn_network.get('cpu_data').decode()
        memory_data = redis_conn_network.get('memory_data').decode()
        dictionary = eval(redis_conn_network.get('dictionary').decode())
    except:
        # 获取最近3个小时的监测数据
        bandwidth_data = Bandwidth.objects.filter(datetime__gte=timezone.now() - timedelta(hours=24)).order_by(
            'datetime')
        cpu_data = Cpu.objects.filter(datetime__gte=timezone.now() - timedelta(hours=24)).order_by('datetime')
        memory_data = Memory.objects.filter(datetime__gte=timezone.now() - timedelta(hours=24)).order_by('datetime')
        # 数据处理
        datetimes = f"{[f'{bandwidth_data.datetime}' for bandwidth_data in bandwidth_data]}"
        download_speed = f'{[bandwidth_data.download_speed for bandwidth_data in bandwidth_data]}'
        upload_speed = f'{[bandwidth_data.upload_speed for bandwidth_data in bandwidth_data]}'
        cpu_data = f'{[cpu_data.percent for cpu_data in cpu_data]}'
        memory_data = f'{[memory_data.percent for memory_data in memory_data]}'

        unique_host = PingResult.objects.values_list('host', flat=True).distinct()
        dictionary = {}
        for host in unique_host:
            # print('当前调查的对象IP：' + host)
            ping_data = PingResult.objects.filter(host=host, datetime__gte=timezone.now() - timedelta(hours=24)).order_by('datetime')
            ping_content = [ping_data.content for ping_data in ping_data]
            dictionary[host] = ping_content
            # print(ping_content)

        # 存入缓存数据
        # 这里采用管道的方式来处理图形验证码的存储
        pl_network.setex(name=f'datetimes', time=300, value=datetimes)  # 设置键名，值，过期时间
        pl_network.setex(name=f'download_speed', time=300, value=download_speed)  # 设置键名，值，过期时间
        pl_network.setex(name=f'upload_speed', time=300, value=upload_speed)  # 设置键名，值，过期时间
        pl_network.setex(name=f'cpu_data', time=300, value=cpu_data)  # 设置键名，值，过期时间
        pl_network.setex(name=f'memory_data', time=300, value=memory_data)  # 设置键名，值，过期时间
        pl_network.setex(name=f'dictionary', time=300, value=f'{dictionary}')  # 设置键名，值，过期时间
        pl_network.execute()  # 执行

        # print(datetimes)
        # print(bandwidth_data)
        # print(download_speed)
        # print(upload_speed)
        # print(cpu_data)
        # print(memory_data)

    return {'datetimes': datetimes, 'download_speed': download_speed, 'upload_speed': upload_speed, 'cpu_data': cpu_data, 'memory_data': memory_data, 'dictionary': dictionary}


def verify(request, HTML):
    userid = request.COOKIES.get('userid')
    if redis_conn_session.get(f'userid_{userid}') is not None and request.COOKIES.get('userid') is not None:
        if redis_conn_session.get(f'userid_{userid}').decode() == request.COOKIES.get('userid'):
            response = render(request, HTML, get_data())
            return response
    return HttpResponse('请登陆后重试！')


class LoginView(View):
    def get(self, request):
        return render(request, 'NetworkLogin.html')


class InfoView(View):
    def get(self, request):
        return verify(request, 'NetworkInfo.html')

    def post(self, request):
        userid = request.POST.get('userid')
        password = request.POST.get('password')
        try:
            user_id = AdminInfo.objects.get(userid=userid)
            if userid is not None and password is not None and user_id is not None:
                password_id = user_id.password
                if password_id == password:
                    response = render(request, 'NetworkInfo.html', get_data())
                    response.set_cookie(key='userid', value=userid, max_age=60 * 60 * 24)
                    pl_session.setex(name=f'userid_{userid}', value=userid, time=60 * 60 * 24)
                    pl_session.execute()
                    return response
            return HttpResponse('请输入正确的账户和密码！', status=401)
        except AdminInfo.DoesNotExist:
            return HttpResponse('请输入正确的账户和密码！', status=401)
