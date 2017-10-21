from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    mobile = models.CharField(max_length=11, verbose_name='电话号码')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='加入时间')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __repr__(self):
        return self.mobile


class VerifyCode(models.Model):
    mobile = models.CharField(max_length=11, verbose_name='电话号码')
    code = models.CharField(max_length=6, verbose_name='验证码')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='发送时间')

    class Meta:
        verbose_name = '验证码'
        verbose_name_plural = verbose_name

    def __repr__(self):
        return self.mobile
