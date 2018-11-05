from django.db import models




# Create your models here.
# 管理员表
class members(models.Model):
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=32)
    realname = models.CharField(max_length=20)
    add_time = models.IntegerField(default=0)
    disabled = models.BooleanField(default=True)
    roles = models.ForeignKey('roles', default=1)

# 分类表
# 建立外键表名是user_users 但是要写成user.users
class types(models.Model):
    name = models.CharField(max_length=30)
    parent_id = models.IntegerField(default=0)
    add_time = models.DateTimeField(auto_now=True)
    add_user = models.ForeignKey('members', default=1)

# 商品信息表
class goods(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    types = models.ForeignKey('types', default=1)
    number = models.IntegerField(default=0)
    status = models.SmallIntegerField(default=0)
    disabled = models.BooleanField(default=False)

# 商品描述表
class goods_introduce(models.Model):
    goods = models.OneToOneField('goods', default=1)  # 一对一关系
    introduce = models.TextField(default='')
    add_time = models.DateTimeField()
    add_user = models.ForeignKey('members')
    disabled = models.BooleanField(default=False)

# 商品图片表
class goods_img(models.Model):
    goods = models.ForeignKey('goods', default=1)
    img_path = models.CharField(max_length=100)
    add_time = models.DateTimeField()
    add_user = models.ForeignKey('members', default=1)
    disabled = models.BooleanField(default=False)

# 权限表
class powers(models.Model):
    name = models.CharField(max_length=100)
    parent_id = models.IntegerField(default=0)
    # control = models.CharField(max_length=100)
    # fun = models.CharField(max_length=100)
    add_time = models.DateTimeField()
    url_name = models.CharField(max_length=50,default='')
    add_user = models.ForeignKey('members', default=1)


#角色
class roles(models.Model):
    name = models.CharField(max_length=100)
    add_time = models.DateTimeField()
    add_user = models.CharField(max_length=30, default='')
    disabled = models.BooleanField(default=False)

# 角色和权限对应表
class role_power(models.Model):
    role = models.ForeignKey('roles', default=1)
    power = models.ForeignKey('powers', default=1)


# 前台楼层表
class floor(models.Model):
    name = models.CharField(max_length=20)
    img_path = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    add_user = models.ForeignKey('members', default=1)
    add_time = models.IntegerField(default=1)
    disabled = models.BooleanField(default=False)


# 楼层跟商品关系表
class floor_goods(models.Model):
    goods = models.ForeignKey('goods', default=1)
    floor = models.ForeignKey('floor', default=1)
    sort = models.IntegerField(default=0)
