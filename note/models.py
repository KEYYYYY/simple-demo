from datetime import datetime

from django.db import models


class Note(models.Model):
    title = models.CharField(max_length=128, verbose_name='标题')
    author = models.ForeignKey(
        'auth.User', related_name='notes', verbose_name='作者')
    note_book = models.ForeignKey(
        'NoteBook', related_name='notes', verbose_name='属于的笔记本')
    content = models.TextField(null=True, blank=True, verbose_name='正文')
    content_html = models.TextField(
        null=True, blank=True, verbose_name='正文HTML')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')
    update_time = models.DateTimeField(
        default=datetime.now, verbose_name='更新时间')
    private = models.BooleanField(default=True, verbose_name='是否私有')

    class Meta:
        ordering = ('-update_time',)
        verbose_name = '笔记'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class NoteBook(models.Model):
    name = models.CharField(max_length=128, verbose_name='名称')
    author = models.ForeignKey(
        'auth.User', related_name='notebooks', verbose_name='作者')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    private = models.BooleanField(default=True, verbose_name='是否私有')

    class Meta:
        ordering = ('-add_time',)
        verbose_name = '笔记本'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
