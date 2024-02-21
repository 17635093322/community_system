# Generated by Django 5.0.1 on 2024-01-12 06:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_userinfo_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addressinfo',
            name='address',
            field=models.IntegerField(default=0, primary_key=True, serialize=False, unique=True, verbose_name='住房号码'),
        ),
        migrations.AlterField(
            model_name='addressinfo',
            name='electricity',
            field=models.IntegerField(verbose_name='电费'),
        ),
        migrations.AlterField(
            model_name='addressinfo',
            name='gas',
            field=models.IntegerField(verbose_name='燃气费'),
        ),
        migrations.AlterField(
            model_name='addressinfo',
            name='water',
            field=models.IntegerField(verbose_name='水费'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.addressinfo', verbose_name='住房号码'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='email',
            field=models.EmailField(max_length=465, verbose_name='邮箱'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='gender',
            field=models.IntegerField(choices=[(0, '男'), (1, '女')], default=0, verbose_name='性别'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='password',
            field=models.CharField(max_length=16, verbose_name='密码'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='phone',
            field=models.CharField(max_length=11, unique=True, verbose_name='手机号'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='userid',
            field=models.CharField(max_length=18, primary_key=True, serialize=False, unique=True, verbose_name='身份证'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='username',
            field=models.CharField(max_length=10, verbose_name='姓名'),
        ),
    ]
