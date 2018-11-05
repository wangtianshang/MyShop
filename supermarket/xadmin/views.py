from django.shortcuts import render,reverse
from django.http import HttpResponse,HttpResponseRedirect
from xadmin.models import members,types,goods,goods_introduce,goods_img,powers,roles,role_power,floor,floor_goods
import json
from datetime import datetime
from django.core.paginator import Paginator
from django.db.models import Q
from django.conf import settings
import os
import uuid
import time
# Create your views here.

# 登录
def login(request):
    if 'username'in request.POST:
        name = request.POST.get('username')
        # print(name)
        password = request.POST.get('password')
        info = members.objects.filter(name=name).first()
        # print(info.roles.role_power_set.filter())
        user_powers=[]
        for user_power in info.roles.role_power_set.filter():
            user_powers.append(user_power.power_id)
        # print(user_powers)
        # return HttpResponse('tijiao')
        if info == None:
            return HttpResponse('用户名错误')
        if password != info.password:
            return HttpResponse('密码错误')
        request.session['uid'] = info.id
        request.session['user_powers'] = user_powers
        return HttpResponseRedirect(reverse('admin_index'))
    else:
        # return HttpResponse('登录失败')
        return render(request,'admin/login.html')
# 主页
def index(request):

    return render(request,'admin/index.html')

# 添加
def addtype(request):
    lis = types.objects.filter().extra({'pId':'parent_id'}).values('id','pId','name')
    # print(list)
    # a = types.objects.filter().values('name')
    # print(a)
    json_str=json.dumps(list(lis))
    # print(json_str)
    return render(request,'admin/add_type.html',{'json_str':json_str})

# 执行添加
def doaddtype(request):
    # print(request.POST)
    # 保存
    typeobj = types()
    typeobj.name = request.POST.get('name')
    typeobj.parent_id = request.POST.get('parent_id')
    typeobj.add_time = datetime.now()
    typeobj.add_user_id = request.session['uid']
    typeobj.save()
    return HttpResponseRedirect(reverse('addtype'))

# 显示列表  分页  搜索
def addtype_list(request):
    # 从前台获取页数
    p = request.GET.get('p',1)

    name = request.GET.get("name",'')
    pid = request.GET.get('parent_id',0)

    q = Q()#实例化Q
    q.connector='and'#设立连接关系

    page=[]#用来记录id和name数据
    if name != '':
        q.children.append(('name', name))#判断是否检索name
        page.append('name='+name)
    if pid !=0 and pid != '' :
        q.children.append(('parent_id', pid))#判断是否检索parent_id
        page.append('parent_id=' + pid)

    page_url = '&'.join(page)

    print(page)
    list = types.objects.filter(q)#查询
    print(list.query)
    page = Paginator(list,4)
    new_list = page.page(p)#参数为需要显示的页数

    return render(request,'admin/add_type_bak.html',{'list':new_list,'page_url':page_url})

# 修改
def edittype(request):
    # 接受ID
    id = request.GET.get('tid', 0)
    # 查询ID对应的数据
    info = types.objects.filter(id=id).first()

    # 查询所有分类数据
    lis = types.objects.filter().extra({'pId': 'parent_id'}).values('id', 'pId', 'name')
    json_str = json.dumps(list(lis))

    return render(request, 'admin/edit_type.html', {'info': info, 'json_str': json_str})

# 修改保存
def doedittype(request):
    id = request.POST.get('id')
    name = request.POST.get('name')
    parent_id = request.POST.get('parent_id')
    add_time = datetime.now()
    add_user_id = request.session['uid']
    types.objects.filter(id=id).update(name=name,parent_id=parent_id,
                   add_time=add_time,add_user_id=add_user_id
                   )
    return HttpResponseRedirect(reverse('admin_addtype_list'))

# 添加信息
def goodsadd(request):
    lis = types.objects.filter().extra({'pId': 'parent_id'}).values('id', 'pId', 'name')
    json_str = json.dumps(list(lis))
    return render(request,'admin/goodsadd.html',{'json_str':json_str})

# 执行添加商品
def dogoodsadd(request):
    # 商品表数据
    goodsobj = goods()
    goodsobj.name = request.POST.get('name')
    goodsobj.price = request.POST.get('price')
    goodsobj.number = request.POST.get('number')
    goodsobj.types_id = request.POST.get('type_id')
    goodsobj.status=0
    goodsobj.disabled=0
    goodsobj.save()

    #商品介绍数据
    introbj = goods_introduce()
    introbj.introduce = request.POST.get('introduce')
    introbj.add_time = datetime.now()
    introbj.add_user_id = request.session.get('uid')
    introbj.goods_id = goodsobj.id
    introbj.save()
    # 或者使用这个保存
    # introbj.goods = goodsobj

    # 保存图片
    files = request.FILES.getlist('img')  # 获取到上传的文件 img为页面file控件的name属性
    for file in files:  # 循环遍历获取到的文件
        file_suffix = file.name.split(".")[-1]  # 获取文件后缀
        new_filename = str(uuid.uuid1()) + '.' + file_suffix  # 生成新的文件名，防止文件重名
        file_path = os.path.join(settings.MEDIA_URL, new_filename)  # 拼接文件路径，用于存入数据
        new_file = open(os.path.join(settings.MEDIA_ROOT, new_filename), 'wb+')  # 创建一个新文件
        for chunk in file.chunks():  # 遍历将上传的文件写入新文件
            new_file.write(chunk)
        # 将数据存入数据库
        new_file.close()
        imgobj = goods_img()
        imgobj.img_path = file_path
        imgobj.goods_id = goodsobj.id
        imgobj.add_user_id = request.session.get('uid')
        imgobj.add_time = datetime.now()
        imgobj.save()
    return HttpResponseRedirect(reverse('admin_goodsadd'))

# 商品列表
def goodslist(request):
    # 接收参数
    p = request.GET.get('p', 1)
    name = request.GET.get('name', '')
    price = request.GET.get('price', '')

    # 用于拼接检索条件
    q = Q()
    q.connector = 'and'
    q.children.append(('disabled', 0))
    where_page = []  # 记录搜索条件，用于拼接分页链接

    if name != '':
        q.children.append(('name', name))  #
        where_page.append('name=' + name)
    if price != '':
        q.children.append(('price', price))
        where_page.append('price=' + price)

    page_url = '&'.join(where_page)  # 拼接

    list = goods.objects.filter(q)  # 查询

    # 分页
    page = Paginator(list, 5)
    list = page.page(p)
    return render(request,'admin/goods_list.html',{'list':list, "page_url": page_url})

# 删除
def goodsdel(request):
    id = request.GET.get('id')
    # bool=goods.objects.filter(id=id).delete()

    bool = goods.objects.filter(id=id).update(disabled=1)
    goods_img.objects.filter(goods_id=id).update(disabled=1)
    goods_introduce.objects.filter(goods_id=id).update(disabled=1)
    data = {}
    if bool:
        data['msg'] = '删除成功'
        data['status'] = 1
    else:
        data['msg'] = '删除失败'
        data['status'] = 0
    return HttpResponse(json.dumps(data))


# 编辑商品
def goodsedit(request):
    gid = request.GET.get('id')

    # 查询商品数据
    info = goods.objects.filter(id=gid).first()
    print(info)
    # 查询分类数据
    lis = types.objects.filter().extra({'pId': 'parent_id'}).values('id', 'pId', 'name')
    json_str = json.dumps(list(lis))
    return render(request,'admin/goods_edit.html', {'json_str': json_str, 'info': info})


def goodsImgDel(request):
    id = request.GET.get('id')
    bool = goods_img.objects.filter(id=id).delete()
    data = {}
    if bool:
        data['msg'] = '删除成功'
        data['status'] = 1
    else:
        data['msg'] = '删除失败'
        data['status'] = 0

    return HttpResponse(json.dumps(data))


def doGoodsEdit(request):

    goodsObj = goods()
    goodsObj.id = request.POST.get('id')
    goodsObj.name = request.POST.get('name')
    goodsObj.price = request.POST.get('price')
    goodsObj.number = request.POST.get('number')
    goodsObj.types_id = request.POST.get('types_id')
    goodsObj.status = 0
    goodsObj.disabled = 0
    goodsObj.save()  # 有id的save是修改

    # 保存 goods_introduce 表数据
    intrObj = goods_introduce()
    intrObj.id=request.POST.get('introduce_id')
    intrObj.introduce = request.POST.get('introduce')
    intrObj.add_time = '2018-09-20 11:19:55'
    intrObj.add_user_id = request.session.get('uid')
    intrObj.goods_id = goodsObj.id
    # intrObj.goods=goodsObj
    intrObj.save()

    # 保存图片
    file_list = request.FILES.getlist('img')  # 获取上传图片列表
    for file in file_list:
        hz = file.name.split('.')  # 拆分文件名
        new_name = str(uuid.uuid1()) + '.' + hz[-1]  # 生成新的文件名，防止重复
        new_file = open(os.path.join(settings.MEDIA_ROOT, new_name), 'wb+')  # 创建新文件
        for chunk in file.chunks():
            new_file.write(chunk)  # 将文件存入新的文件内
        new_file.close()  # 关闭文件
        # 将数据存入数据库
        imgObj = goods_img()
        imgObj.img_path = os.path.join(settings.MEDIA_URL, new_name)
        imgObj.add_time = datetime.now()
        imgObj.add_user_id = request.session.get('uid')
        imgObj.goods_id = goodsObj.id
        # imgObj.goods=goodsObj
        imgObj.save()
    # 实例化模型 ，添加数据
    return HttpResponse('提交成功了')



# 添加权限
def addpower(request):
    lis = powers.objects.filter().extra({'pId': 'parent_id'}).values('id', 'pId', 'name')
    # print(list)
    # a = types.objects.filter().values('name')
    # print(a)
    json_str = json.dumps(list(lis))
    # print(json_str)
    return render(request,'admin/addpower.html',{'json_str':json_str})
# 执行添加
def doaddpower(request):
    # name = request.POST.get('name')
    # url_name = request.POST.get('url_name')
    # pid = request.POST.get('parent_id')
    # print(request.POST)
    powersObj = powers()
    powersObj.name = request.POST.get('name')
    powersObj.parent_id = request.POST.get('parent_id')
    powersObj.add_time = datetime.now()
    powersObj.add_user_id = request.session.get('uid')
    # powersObj.control = request.POST.get('control')
    # powersObj.fun = request.POST.get('fun')
    powersObj.url_name = request.POST.get('url_name')
    powersObj.save()

    # return HttpResponseRedirect(reverse('admin_index'))

    return HttpResponseRedirect(reverse('admin_addpower'))

# 添加角色
def addrole(request):
    lis = powers.objects.filter().extra({'pId': 'parent_id'}).values('id', 'pId', 'name')
    json_str = json.dumps(list(lis))
    return render(request,'admin/addrole.html',{'json_str':json_str})

# 执行添加
def doaddrole(request):
    # print(request.POST)
    print(request.POST)
    roleObj = roles()
    roleObj.name = request.POST.get('name')
    roleObj.add_time = datetime.now()
    roleObj.add_user = request.session.get('uid')  # 没有建立外键
    roleObj.disabled = 0
    roleObj.save()

    powers_list = request.POST.getlist('powers_id')

    for power_id in powers_list:
        prObj = role_power()
        prObj.power_id = power_id
        prObj.role_id = roleObj.id
        prObj.save()
    return HttpResponse('nihao')


# 添加楼层
def addfloor(request):
    return render(request,'admin/addfloor.html')

# 执行
def doaddfloor(request):
    file = request.FILES.get('img')  # 获取上传图片

    hz = file.name.split('.')  # 拆分文件名
    new_name = str(uuid.uuid1()) + '.' + hz[-1]  # 生成新的文件名，防止重复
    new_file = open(os.path.join(settings.MEDIA_ROOT, new_name), 'wb+')  # 创建新文件
    for chunk in file.chunks():
        new_file.write(chunk)  # 将文件存入新的文件内
    new_file.close()  # 关闭文件
    # 将数据存入数据库
    floorobj = floor()
    floorobj.name = request.POST.get('name')
    floorobj.img_path = os.path.join(settings.MEDIA_URL, new_name)
    floorobj.url = request.POST.get('url')
    floorobj.add_time = time.time()
    floorobj.add_user_id = request.session.get('uid')
    floorobj.disabled = 0
    # imgObj.goods=goodsObj
    floorobj.save()
    return HttpResponseRedirect(reverse('admin_addfloor'))

# 添加楼层商品
def addfloorgoods(request):
    info = floor.objects.filter()
    list = goods.objects.filter(disabled=0)
    return render(request,'admin/addfloorgoods.html',{'floor_lis':info,'goods_lis':list})
def doaddfloorgoods(request):

    goods_list = request.POST.getlist('goods_id')
    print(goods_list)
    # 一次添加多个商品
    for i in goods_list:
        flgobj = floor_goods()
        flgobj.goods_id = i
        flgobj.floor_id = request.POST.get('floor_id')
        flgobj.sort = request.POST.get('sort')
        flgobj.save()
    return HttpResponseRedirect(reverse('admin_addfloorgoods'))