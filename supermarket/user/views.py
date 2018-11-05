from django.shortcuts import render,reverse
from django.http import HttpResponse,HttpResponseRedirect
import json
from user.models import users
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from random import randint
import re
import uuid
from user.models import shop_cart,user_order_details,user_order

from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest
# Create your views here.

def login(request):
    return render(request,'user/login.html')

def dologin(request):
    name = request.POST.get('username')
    password = request.POST.get('password')
    print(name)
    print(password)
    info = users.objects.filter(name=name).first()
    if info == None:
        return HttpResponse('用户名错误')
    if password != info.password:
        return HttpResponse('密码错误')

    request.session['user_id'] = info.id  # 记录session,标记用户登录状态
    request.session['user_name'] = info.name # 记录session,标记用户登录状态

    code = request.POST.get('code')
    print(type(code))
    # 获取session数据
    session_code = request.session['verify_code']
    print(type(session_code))
    # 判断 是否相同
    if code.lower() != session_code.lower():
        return HttpResponse('验证码错误')

    return HttpResponseRedirect(reverse('goods_index'))

# 注册
def sign(request):
    return render(request,'user/sign.html')

# 注销
def exit(request):
    if request.session["user_id"]:
        del request.session["user_id"]
    if request.session["user_name"]:
        del request.session["user_name"]
    return render(request,'goods/index.html')
def checkuser(request):
    # 后面的空字符为默认值
    username = request.POST.get('username', '')
    user = users.objects.filter(name = username).first()
    data = {}
    if user == None:
        data['msg'] = '用户名可用'
        data['status'] = 0
        # print(json.dumps(data))
        return HttpResponse(json.dumps(data))
    else:
        data['msg'] = '用户名已经存在'
        data['status'] = 1
        # print(json.dumps(data))
        return HttpResponse(json.dumps(data))

# 生成验证码
def verify_code(request):
    im = Image.new('RGB',(69,38),(181,181,181))
    dram = ImageDraw.Draw(im)
    str_list = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
    code = ''
    # 生成五个随机字符
    for i in range(5):
        num = randint(0,61)
        font = ImageFont.truetype('simfang.ttf', 25)
        code += str_list[num]
        dram.text((i * 13, 5), str_list[num], font=font, fill=(randint(0, 255), randint(50, 255), 50))
    # 生成120个点
    for y in range(0, 120):
        dram.point((randint(0, 69), randint(0, 38)), fill=(randint(0, 255), randint(50, 255), 50))

    io = BytesIO()
    im.save(io, 'png')
    request.session['verify_code'] = code;
    return HttpResponse(io.getvalue(), 'image/png')

#字符比对
def check_code(request):
    # 接受数据
    code = request.POST.get('code')
    # 获取session数据
    session_code = request.session['verify_code']
    # 判断 是否相同
    data = {}
    if code.lower() == session_code.lower():
        data['msg'] = '验证码正确'
        data['status'] = 1
        return HttpResponse(json.dumps(data))
    else:
        data['msg'] = '验证码错误'
        data['status'] = 0
        return HttpResponse(json.dumps(data))

# 输入密码
def subpassword(request):
    password = request.POST.get('password')
    data = {}
    try:
        re.match(r'^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,20}$', password).group()
        data['msg'] = '密码格式正确'
        data['status'] = 1
        return HttpResponse(json.dumps(data))
    except:
        data['msg'] = '密码格式为6-20位字母数组组合'
        data['status'] = 0
        return HttpResponse(json.dumps(data))


# 注册执行函数
def reg(request):
    name = request.POST.get('username')
    password = request.POST.get('password')
    users.objects.create(name=name,password=password)
    return render(request,'user/sign2.html')


# 显示购物车列表
def showlist(request):
    userid = request.session.get('user_id')
    car_goods_list = shop_cart.objects.filter(users_id=userid)
    total = 0

    for car in car_goods_list:
        if car.checked == 1:
            total += car.number * car.goods.price
    return render(request,'user/order_step1.html',{'car_goods_list':car_goods_list,'total':total})

# 同步数据库数量 与状态
def compute(request):
    num = request.POST.get('num')
    idd = request.POST.get('id')
    shop_cart.objects.filter(id=idd).update(number=num)
    data = {}
    data['msg'] = '成功'
    data['status']=1
    return HttpResponse(json.dumps(data))

# 显示提交订单页
def dingdan(request):
    checked = request.POST.getlist('checked')

    total = 0
    data = shop_cart.objects.filter(id__in=checked)
    for car in data:
        total += car.number * car.goods.price
    return render(request,'user/order_step2.html',{'data':data,'total':total})

# 支付页
def pay(request):
    carid = request.POST.getlist('car_id')
    user_id = request.session.get('user_id')

    # if user_id == 0:
    #     return HttpResponse('先去登陆')

    data = shop_cart.objects.filter(id__in=carid, users_id=user_id)
    total = 0
    for car in data:
        total += car.goods.price * car.number


    # 创建订单
    userorder = user_order()
    userorder.order_code = str(uuid.uuid1())
    # request.session['order_code'] = userorder.order_code
    userorder.users_id = user_id
    userorder.money = total
    userorder.pay_status = 0
    userorder.pay_money = 0
    userorder.order_status = 0
    userorder.save()
    # 保存订单详情

    for car in data:
        userorderInfo = user_order_details()
        userorderInfo.order_id = userorder.id
        userorderInfo.goods_id = car.goods.id
        userorderInfo.number = car.number
        userorderInfo.price = car.goods.price
        # print(userOrderInfo.__dict__)
        userorderInfo.save()
    # 删除购物车
    # return HttpResponse('tijiaole')
    shop_cart.objects.filter(id__in=carid, users_id=user_id).delete()

    # 支付请求

    """
       设置配置，包括支付宝网关地址、app_id、应用私钥、支付宝公钥等，其他配置值可以查看AlipayClientConfig的定义。
       """
    alipay_client_config = AlipayClientConfig()
    alipay_client_config.server_url = 'https://openapi.alipaydev.com/gateway.do'  # 网关
    alipay_client_config.app_id = '2016092100565292'
    alipay_client_config.app_private_key = 'MIIEowIBAAKCAQEA8gP51OX3pOtUvAMykIqZquj8gK+oAyOsQlnL/S4iU4FhOvoizV2uadzLlAvN22trmuRh5JO5bbR9sH/ZYrBi3lfCT1hV5E791QnLYXlXIHWqijn7VV5htOmjNUAtXXoVBjtUAEzMSZZPEh+uJK7WzoBBMWKyN1Jeyj1dLA17jJp6rnYfXHVfy7AodZR6d80WfmevQB/TfqpzWLgMSwE0YJzKIGymCq/bNkABVY3CnnpK8mEIvNjl7e3IIpd2rTFM1gMju9y+k6B2/toN/wGghYU99pefTdR8HWUlPVpo8uhLcIGXmyMikusO3BKJ3AV5iAcYZ3QJ6oGlOrd3SKrpWQIDAQABAoIBAC46ADBgNKs1oBvBaJkfQDbbBc/2vVrMJ40M5d/YPgpBPjcrrBYZ/MSPvfrrPkjY/da6JNCqPtLrlM5vvTASjO/3R1AsiUtwox9cHZLiwHecwhRg+tbVjkgmEFyNg5zFQtrL3kGoaaTspvHJR1QOaU1MRieOuIfEngJ3MiLF+IFkaU+vZ/GHSfOqIlknKqFwMD9lwC/nIio8Nv3xqFcgr+Hmaa1J7tSDJ1shnkw5iQQPEPqBjNQROXYC7yZBx+pBk8ctdl+/RJgn1QpbSFSxU2xwGZf5PktFHwt4M1FI/MlVQKht2RkkaEcmoQfG+CSNEXaE4xtKFC1aY4EJl5Uc1NkCgYEA+g78AdjSD9YXg+g5BcWw8OSNgNj2ayaKeEQ76vU5AbCG5FG7FzuqUQZ+9es9dd5JRvT53uLqT6IEYtX8ox61EFOdcdnFtl/At5a07lvmTO3SfS6IEyc0HJFaDkO37rma73SWq/gwiCzLDvuP6zVI/x18Zlw+SzwqaKEFvWfjMLMCgYEA98QRnt2Da4xQqBWRXjARj1a7zNxl8JlFyglOO727SyJ62ap2k3ZZL2vRYDTb/hsx2nFtuKUWMGL4yqswpMPUqfH9sUkrBpQQjyPAc7B9CXGWklD7AnefYppAXidQogOZJjSjG5ffownAc2oPhpID+Rhnu5H0b8tedWx54ia2a8MCgYAH1kxjqm36/RTDl5Wh7q46/o7IyQQAG7cfSdQu6vycZvHzWfRpJ/+QhomYH4VPmmXliWwDZk09rbBBgL9oRWAbYOOAW/jsXFfn6RtGlS7EnneIYNr27rWdZ5jQ9aJgIwUOGDNYtHCg8/ZxQ8Ug9AyTolLxylZReVNC8DkD1Ku0LQKBgAULEqi/LYuk4YdqWPkn1VOrmksDOXf6RrdkFRmWNRfEbee8VomN4Sbb9PkWWlwDxbICmQ8nHRqDCTlm3qib69pBuL5BFQUfQm8HdUVllEX67+uuhk14jd/9781602NY22cxrxhCsSSqcCZpREOi+T26x3HD+MvFwfh16s01qITtAoGBAOwpK4Dccbp0V7xgL5FsCPe5q1Ez17EV4Ix0lc5jUNZ/2llG4Hngrf2ohiAHPnDTAEVpFPjd1wc95VwoEYzdcqzlu6T7N9B3VEVNa6Bp52c1lAblJeMvsi9aSpplErpzUXdMWZN8zNQEv3MbGe1xdSM+lhNdqPob/odszAzjkHin'
    alipay_client_config.alipay_public_key = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAkNdMeXTMfEn5oAXRH7K0Cjwk/Sp6bOgVzbEy+T+oKykKrHokoQBZqKIKQtGZ1tKcYT2ZDiZJIWeb4EnMhtmxo5m4s3u9B/SRxZURg4dt5qeEbqxiTVxJ5RYMfZ/fVGlpnXqcLwyzSXPZQDX7LmZ96oqQsF07nJFtm9h7q+AkGjNk5QHnSnzlYPr7ERyb7dFSqOS4Weow3aVrhtC5oZGu37hgIfuq0xEiftEDhMV6BWPWwLVnavwaXzsp6m09YTmFpqJBistyInYlwx/vsPk8wuhVr7qn92rtAav6V0wN3g0Y4l43qq7cLO4ep0nSB3aiMQu1r/9wvdPcPjlaa9mjeQIDAQAB'

    """
       得到客户端对象。
       注意，一个alipay_client_config对象对应一个DefaultAlipayClient，定义DefaultAlipayClient对象后，alipay_client_config不得修改，如果想使用不同的配置，请定义不同的DefaultAlipayClient。
       logger参数用于打印日志，不传则不打印，建议传递。
       """
    client = DefaultAlipayClient(alipay_client_config=alipay_client_config)

    """
    页面接口示例：alipay.trade.page.pay
    """
    # 对照接口文档，构造请求对象
    model = AlipayTradePagePayModel()
    model.out_trade_no = userorder.order_code
    model.total_amount = float(userorder.money)
    model.subject = "iphone XS MAX"
    model.body = "支付宝测试"
    model.product_code = "FAST_INSTANT_TRADE_PAY"  # 固定值
    Alirequest = AlipayTradePagePayRequest(biz_model=model)
    Alirequest.return_url = 'http://127.0.0.1:8100/user/return_url'
    # Alirequest.return_url = 'http://127.0.0.1:8100/goods'
    # 得到构造的请求，如果http_method是GET，则是一个带完成请求参数的url，如果http_method是POST，则是一段HTML表单片段
    #记住上面的话
    response = client.page_execute(Alirequest, http_method="get")

    print("alipay.trade.page.pay response:" + response)

    return HttpResponse(response)

def return_url(request):
    # 根据订单号 修改用户订单状态
    print(request.POST)

    # danhao= request.session['order_code'] #request.GET.get('out_trade_no')
    danhao=request.GET.get('out_trade_no')
    total_amount=request.GET.get('total_amount')
    timestamp=request.GET.get('timestamp')
    user_order.objects.filter(order_code=danhao).update(pay_status=1,pay_money=total_amount,pay_time=timestamp)
    #
    return HttpResponseRedirect('/goods/index/')