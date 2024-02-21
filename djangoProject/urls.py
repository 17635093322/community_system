from django.contrib import admin
from django.urls import path
import user.views as UV
import main.views as MV
import network.views as NV

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MV.MainView.as_view(), name='main'),
    path('parking_login', MV.ParkingLoginView.as_view(), name='parking_login'),
    path('parking_info', MV.ParkingInfoView.as_view(), name='parking_info'),
    path('parking_add', MV.Add.as_view(), name='parking_add'),
    path('parking_sub', MV.Sub.as_view(), name='parking_sub'),
    path('user_login/', UV.LoginView.as_view(), name='user_login'),
    path('user_info/', UV.InfoView.as_view(), name='user_info'),
    path('user_pay/', UV.PayView.as_view(), name='user_pay'),
    path('network_login/', NV.LoginView.as_view(), name='network_login'),
    path('network_info/', NV.InfoView.as_view(), name='network_info')
]
