from django.contrib.sites import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from main.models import *
from django_redis import get_redis_connection

redis_conn = get_redis_connection('session')
pl = redis_conn.pipeline()
number = 0


class Add(View):
    def get(self, request):
        global number
        number += 1
        return verify(request, 'ParkingInfo.html')


class Sub(View):
    def get(self, request):
        global number
        number -= 1
        return verify(request, 'ParkingInfo.html')


class MainView(View):
    def get(self, request):
        messages = Messages.objects.all()
        dictionary = {}
        for message in messages:
            dictionary[message.sender_name] = message.content
        return render(request, 'Main.html', {'contents': dictionary, 'number': number})


def verify(request, HTML):
    userid = request.COOKIES.get('userid')
    if redis_conn.get(f'userid_{userid}') is not None and request.COOKIES.get('userid') is not None:
        if redis_conn.get(f'userid_{userid}').decode() == request.COOKIES.get('userid'):
            response = render(request, HTML, {'number': number})
            return response
    return HttpResponse('请登陆后重试！')


class ParkingLoginView(View):
    def get(self, request):
        return render(request, 'ParkingLogin.html')


class ParkingInfoView(View):
    def get(self, request):
        return verify(request, 'ParkingInfo.html')

    def post(self, request):
        userid = request.POST.get('userid')
        password = request.POST.get('password')
        try:
            user_id = AdminInfo.objects.get(userid=userid)
            if userid is not None and password is not None and user_id is not None:
                password_id = user_id.password
                if password_id == password:
                    response = render(request, 'ParkingInfo.html', {'number': number})
                    response.set_cookie(key='userid', value=userid, max_age=60 * 60 * 24)
                    pl.setex(name=f'userid_{userid}', value=userid, time=60 * 60 * 24)
                    pl.execute()
                    return response
            return HttpResponse('请输入正确的账户和密码！', status=401)
        except AdminInfo.DoesNotExist:
            return HttpResponse('请输入正确的账户和密码！', status=401)
