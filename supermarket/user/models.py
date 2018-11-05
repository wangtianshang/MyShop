from django.db import models

# Create your models here.
class users(models.Model):
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=32)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=12)

# 用户购物车表
class shop_cart(models.Model):
    # 商品 数量 用户  添加时间 是否选中
    goods = models.ForeignKey('xadmin.goods')
    number = models.IntegerField(default=1)
    users = models.ForeignKey('users', default=1)
    add_time = models.DateTimeField(auto_now=True)
    checked = models.BooleanField(default=True)


# 订单表
class user_order(models.Model):
    order_code = models.CharField(max_length=50, unique=True)
    users = models.ForeignKey('users', default=1)
    money = models.DecimalField(max_digits=10, decimal_places=2)
    add_time = models.DateTimeField(auto_now_add=True)
    pay_status = models.BooleanField(default=False)
    pay_money = models.DecimalField(max_digits=10, decimal_places=2)
    pay_time = models.DateTimeField(null=True)
    order_status = models.BooleanField(default=False)


# 订单详情表
class user_order_details(models.Model):
    order = models.ForeignKey('user_order', default=1)
    goods = models.ForeignKey('xadmin.goods')
    number = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # 商品价格
