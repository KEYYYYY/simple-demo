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
    identity = models.CharField(
        max_length=1,
        choices=(('S', '学生'), ('T', '老师')),
        default='S',
        verbose_name='身份'
    )
    relations = models.ManyToManyField('UserProfile', verbose_name='关系')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
