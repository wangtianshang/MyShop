# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-09-30 12:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('xadmin', '0009_floor_floor_goods'),
        ('user', '0003_shop_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='user_order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_code', models.CharField(max_length=50, unique=True)),
                ('money', models.DecimalField(decimal_places=2, max_digits=10)),
                ('add_time', models.DateTimeField(auto_now_add=True)),
                ('pay_status', models.BooleanField(default=False)),
                ('pay_money', models.DecimalField(decimal_places=2, max_digits=10)),
                ('pay_time', models.DateTimeField(null=True)),
                ('order_status', models.BooleanField(default=False)),
                ('users', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='user.users')),
            ],
        ),
        migrations.CreateModel(
            name='user_order_details',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(default=1)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='xadmin.goods')),
                ('order', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='user.user_order')),
            ],
        ),
    ]
