# Generated by Django 2.0.1 on 2018-01-28 16:59

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rest_learn', '0007_favorite'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='favorite',
            unique_together={('goods', 'user')},
        ),
    ]
