from django.shortcuts import render
from xadmin.models import floor_goods,floor,types,goods
from user.models import shop_cart
from django.core.paginator import Paginator
from django.db.models import Q,F
from django.http import HttpResponse
import json
# Create your views here.

def base(request):
    return render(request,'goods/base.html')


def index(request):
    data = floor.objects.filter()
    return render(request,'goods/index.html',{'list':data})

# 列表
def goods_list(request):
    p = request.GET.get('p',1)

    # 检索
    name = request.GET.get('name', '')
    type_id = request.GET.get('tid', 0)
    # 转成整型  传到前台进行比对
    ttid = int(type_id)

    two_datas = []#设置这个是为了type_id不存在的时候 不出错
    # 用于前台 列表 分类 在商品列表里面
    if type_id != 0:
        types_lists = types.objects.filter(id=ttid).first()
        two_types = types.objects.filter(parent_id=types_lists.id)
        two_datas = []
        for two_type in two_types:
            lis = {}
            lis['name'] = two_type.name
            lis['id'] = two_type.id
            three_list = types.objects.filter(parent_id=two_type.id)
            lis['list'] = three_list
            two_datas.append(lis)
    # print(two_datas)
    # 用于拼接检索条件
    q = Q()
    q.connector = 'and'
    q.children.append(('disabled', 0))  # 删除的不再显示
    where_page = []  # 记录搜索条件，用于拼接分页链接

    if name != '':
        q.children.append(('name', name))  #
        where_page.append('name=' + name)
    if type_id != 0:
        q.children.append(('types_id', type_id))
        where_page.append('tid=' + type_id)

    page_url = '&'.join(where_page)  # 拼接
    data = goods.objects.filter(q)

    # 分页
    page = Paginator(data,8)
    goods_data = page.page(p)
    return render(request,'goods/list.html',{'goods_data':goods_data,'page_url':page_url,'ttid':ttid,'two_datas':two_datas})



# def gettypeid(ttid):
#     types_lists = types.objects.filter(id=ttid).order_by('id')
#     print(types_lists)



# 面包屑    在商品详情里面
def gettype(tid,list):
    data = types.objects.filter(id=tid).first()
    if data.parent_id != 0:
        list.append({'id':data.id,'name':data.name})
        gettype(data.parent_id,list)
    else:
        # 此处使用插入的话  就不会有颠倒了
        list.append({'id': data.id, 'name': data.name})
    return list

def showdetails(request):
    gid = request.GET.get('gid',0)
    # print(gid)
    # return HttpResponse('kkkkkkk')
    data = goods.objects.filter(id=gid).first()
    # 顺序是颠倒的
    crumbs = reversed(gettype(data.types_id,[]))
    # print(crumbs)
    return render(request,'goods/show_details.html',{'data':data,'crumbs':crumbs})


# 添加购物车
def addshoppingcart(request):
    gid = request.POST.get('gid',0)
    number = request.POST.get('number',1)
    print(gid)
    print(number)
    userid = request.session.get('user_id',0)

    data = {}
    data['status'] = 0
    data['msg'] = '请登录'
    if userid == 0:
        return HttpResponse(json.dumps(data))

    info = shop_cart.objects.filter(goods_id=gid, users_id=userid).first()
    # 如果数据库有相同数据 数量叠加
    if info != None:
        bool = shop_cart.objects.filter(goods_id=gid, users_id=userid).update(number=F('number') + number)
    else:
        carobj = shop_cart()
        carobj.goods_id = gid
        carobj.number = number
        carobj.checked = 1  # F Q
        carobj.users_id = request.session.get('user_id')
        carobj.save()
    # 返回结果
    data = {}
    data['status'] = 1
    data['msg'] = '添加成功'
    return HttpResponse(json.dumps(data))


def carlist(request):
    userid = request.session.get('user_id', 0)
    car_list = shop_cart.objects.filter(users_id=userid,checked=1)
    number = len(car_list)
    # print(car_list.count())
    return render(request, 'user/car_list.html', {'car_list': car_list,'number':number})