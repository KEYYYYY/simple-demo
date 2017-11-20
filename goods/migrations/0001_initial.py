# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-19 11:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GoodsProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='商品名')),
                ('price', models.FloatField(verbose_name='价格')),
                ('img', models.ImageField(upload_to='', verbose_name='展示图')),
            ],
            options={
                'verbose_name': '商品',
                'verbose_name_plural': '商品',
            },
        ),
    ]