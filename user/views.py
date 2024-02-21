from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection
from user.models import *


# Create your views here.
redis_conn = get_redis_connection('session')
pl = redis_conn.pipeline()


def getinfo(user_id=None, requests=None):
    if user_id is not None:
        # 个人信息的获取
        personal = UserInfo.objects.get(userid=user_id)
    elif requests is not None:
        # 个人信息的获取
        personal = UserInfo.objects.get(userid=requests.COOKIES.get('userid'))
        user_id = personal.userid
    else:
        return HttpResponse('不存在账户信息')
    name = personal.username
    phone = personal.phone
    email = personal.email
    gender = {0: '男', 1: '女'}[personal.gender]
    address_id = personal.address
    # 住房水电费信息的获取
    water = AddressInfo.objects.get(address=str(address_id)[0]).water
    electricity = AddressInfo.objects.get(address=str(address_id)[0]).electricity
    gas = AddressInfo.objects.get(address=str(address_id)[0]).gas
    return {'user_id': user_id, 'name': name, 'phone': phone, 'email': email, 'gender': gender, 'address': address_id, 'water': water,
            'electricity': electricity, 'gas': gas}


def verify(request, HTML, func=None):
    userid = request.COOKIES.get('userid')
    if redis_conn.get(f'userid_{userid}') is not None and request.COOKIES.get('userid') is not None:
        if redis_conn.get(f'userid_{userid}').decode() == request.COOKIES.get('userid'):
            if func is None:
                response = render(request, HTML)
            else:
                response = render(request, HTML, func(requests=request))
            return response
    return HttpResponse('请登陆后重试！')


class LoginView(View):
    def get(self, request):
        return render(request, 'UserLogin.html')
        # return render(request, 'index.html')


class InfoView(View):
    def get(self, request):
        return verify(request, 'UserInfo.html', getinfo)

    def post(self, request):
        userid = request.POST.get('userid')
        password = request.POST.get('password')
        try:
            user_id = UserInfo.objects.get(userid=userid)
            if userid is not None and password is not None and user_id is not None:
                password_id = user_id.password
                if password_id == password:
                    response = render(request, 'UserInfo.html', getinfo(user_id=userid))
                    response.set_cookie(key='userid', value=userid, max_age=60 * 60 * 24)
                    pl.setex(name=f'userid_{userid}', value=userid, time=60 * 60 * 24)
                    pl.execute()
                    return response
            return HttpResponse('请输入正确的账户和密码！')
        except UserInfo.DoesNotExist:
            return HttpResponse('请输入正确的账户和密码！')


class PayView(View):
    def get(self, request):
        return verify(request, 'UserPay.html')

    def post(self, request):
        water = request.POST.get('water')
        electricity = request.POST.get('electricity')
        gas = request.POST.get('gas')
        if not (water or electricity or gas):
            water = electricity = gas = 0
        # 缴费后数据更新
        INFO = getinfo(requests=request)
        INFO['water'] = INFO['water'] + int(float(water))
        INFO['electricity'] = INFO['electricity'] + int(float(electricity))
        INFO['gas'] = INFO['gas'] + int(float(gas))
        AddressInfo_save = AddressInfo.objects.get(address=str(INFO['address'])[0])
        AddressInfo_save.water = INFO['water']
        AddressInfo_save.electricity = INFO['electricity']
        AddressInfo_save.gas = INFO['gas']
        AddressInfo_save.save()
        response = render(request, 'UserInfo.html', INFO)
        return response
