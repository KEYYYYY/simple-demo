from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    """用户"""
    mobile = models.CharField(max_length=11, null=False, verbose_name='电话')
    gender = models.CharField(
        max_length=4,
        choices=(('M', '男'), ('F', '女')),
        default='M',
        verbose_name='性别'
    )

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
