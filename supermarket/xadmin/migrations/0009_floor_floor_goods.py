# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-09-26 08:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('xadmin', '0008_roles_add_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='floor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('img_path', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=200)),
                ('add_time', models.IntegerField(default=1)),
                ('disabled', models.BooleanField(default=False)),
                ('add_user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='xadmin.members')),
            ],
        ),
        migrations.CreateModel(
            name='floor_goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort', models.IntegerField(default=0)),
                ('floor', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='xadmin.floor')),
                ('goods', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='xadmin.goods')),
            ],
        ),
    ]
