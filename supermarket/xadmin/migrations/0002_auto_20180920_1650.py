# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-09-20 08:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('xadmin', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='types',
            name='add_user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='xadmin.members'),
        ),
    ]
