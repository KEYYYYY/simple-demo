# Generated by Django 2.0.1 on 2018-01-31 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_learn', '0012_ordergoods'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='sn',
            field=models.CharField(max_length=32, null=True, verbose_name='订单号'),
        ),
    ]