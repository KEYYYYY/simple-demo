# Generated by Django 2.0.1 on 2018-01-30 18:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rest_learn', '0011_auto_20180130_1745'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nums', models.IntegerField(verbose_name='商品数量')),
                ('goods', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='rest_learn.Goods', verbose_name='商品')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rest_learn.Order', verbose_name='订单')),
            ],
            options={
                'verbose_name': '订单商品',
                'verbose_name_plural': '订单商品',
            },
        ),
    ]
