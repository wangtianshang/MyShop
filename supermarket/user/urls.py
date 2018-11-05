from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^login/$',views.login,name='login'),
    url(r'^dologin/$',views.dologin,name='dologin'),
    url(r'^sign/$',views.sign,name='sign'),
    url(r'^checkuser/$',views.checkuser,name='checkuser'),
    url(r'^verify_code/$',views.verify_code,name='verify_code'),
    url(r'^check_code/$',views.check_code,name='check_code'),
    url(r'^subpassword/$',views.subpassword,name='subpassword'),
    url(r'^reg/$',views.reg,name='reg'),
    url(r'^exit/$',views.exit,name='exit'),

    url(r'^showcarlist/$',views.showlist,name='showcarlist'),
    url(r'^compute/$',views.compute,name='compute'),
    url(r'^dingdan',views.dingdan,name='dingdan'),
    url(r'^pay',views.pay,name='pay'),
    url(r'^return_url/',views.return_url) # 支付宝回调链接

]
