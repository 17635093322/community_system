import psutil
import subprocess
import speedtest
from network.models import *


def network_task():
    IP_ADDRESS = ['192.168.1.1', '192.168.1.24']
    # 测网速
    try:
        st = speedtest.Speedtest()
        download_speed = st.download() / (1024 * 1024)
        upload_speed = st.upload() / (1024 * 1024)
    except:
        download_speed = 0
        upload_speed = 0
    Bandwidth.objects.create(download_speed=download_speed, upload_speed=upload_speed)

    # 保存CPU数据
    cpu_percent = psutil.cpu_percent()
    Cpu.objects.create(percent=cpu_percent)

    # 保存内存利用率数据
    mem_percent = psutil.virtual_memory().percent
    Memory.objects.create(percent=mem_percent)

    print('=' * 100)
    # print(f'下载速度度:{download_speed}')
    # print(f'上传速度：{upload_speed}')
    print(f'cpu利用率：{cpu_percent}')
    print(f'内存利用率：{mem_percent}')

    for ip_address in IP_ADDRESS:
        # 检测网络延迟
        try:
            result = subprocess.check_output(['/sbin/ping', '-c', '1', ip_address], universal_newlines=True)
            # On Windows, you might need to use 'ping -n 4' instead of 'ping -c 4'
        except subprocess.CalledProcessError:
            result = "Ping failed. Check the IP address."
        PingResult.objects.create(host=ip_address, content=result)
        print(f'检测IP：{ip_address}，结果：{result}')
    print('=' * 100)
