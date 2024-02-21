# Generated by Django 5.0.1 on 2024-02-19 00:20

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminInfo',
            fields=[
                ('userid', models.CharField(max_length=18, primary_key=True, serialize=False, unique=True, verbose_name='身份证')),
                ('username', models.CharField(max_length=10, verbose_name='姓名')),
                ('password', models.CharField(max_length=16, verbose_name='密码')),
                ('phone', models.CharField(max_length=11, unique=True, verbose_name='手机号')),
                ('gender', models.IntegerField(choices=[(0, '男'), (1, '女')], default=0, verbose_name='性别')),
            ],
            options={
                'verbose_name': '管理员信息',
                'verbose_name_plural': '管理员信息',
                'db_table': 'network_admin_info',
            },
        ),
        migrations.CreateModel(
            name='Bandwidth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('download_speed', models.FloatField()),
                ('upload_speed', models.FloatField()),
            ],
            options={
                'verbose_name': '流量宽带',
                'verbose_name_plural': '流量宽带',
                'db_table': 'tb_Bandwidth',
            },
        ),
        migrations.CreateModel(
            name='Cpu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('percent', models.FloatField()),
            ],
            options={
                'verbose_name': 'CPU利用率',
                'verbose_name_plural': 'CPU利用率',
                'db_table': 'tb_CPU',
            },
        ),
        migrations.CreateModel(
            name='Memory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('percent', models.FloatField()),
            ],
            options={
                'verbose_name': '内存利用率',
                'verbose_name_plural': '内存利用率',
                'db_table': 'tb_Memory',
            },
        ),
        migrations.CreateModel(
            name='PingResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host', models.CharField(max_length=20)),
                ('content', models.TextField()),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': 'Ping值检测',
                'verbose_name_plural': 'Ping值检测',
                'db_table': 'tb_Ping',
            },
        ),
    ]