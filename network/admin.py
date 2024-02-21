from django.contrib import admin
from network.models import *

# Register your models here.

admin.site.register(Cpu)
admin.site.register(Memory)
admin.site.register(AdminInfo)
admin.site.register(PingResult)
admin.site.register(Bandwidth)