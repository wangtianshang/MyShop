# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-09-25 14:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xadmin', '0007_auto_20180925_1915'),
    ]

    operations = [
        migrations.AddField(
            model_name='roles',
            name='add_user',
            field=models.CharField(default='', max_length=30),
        ),
    ]