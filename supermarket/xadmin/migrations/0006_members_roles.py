# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-09-25 08:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('xadmin', '0005_auto_20180925_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='members',
            name='roles',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='xadmin.roles'),
        ),
    ]
