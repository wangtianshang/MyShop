from django.conf.urls import url
from . import views
urlpatterns = [
 url(r'^login/$',views.login,name='admin_login'),
 url(r'^index/$',views.index,name='admin_index'),
 url(r'^addtype/$',views.addtype,name='addtype'),
 url(r'^doaddtype/$',views.doaddtype,name='doaddtype'),
 url(r'^addtype_list/$',views.addtype_list,name='admin_addtype_list'),
 url(r'^type_edit/$', views.edittype, name='admin_edittype'),
 url(r'^dotype_edit/$', views.doedittype, name='admin_doedittype'),
 url(r'^goodsadd/$',views.goodsadd,name='admin_goodsadd'),
 url(r'^dogoodsadd/$',views.dogoodsadd,name='admin_dogoodsadd'),
 url(r'^goodslist/$',views.goodslist,name='admin_goodslist'),
 url(r'^goodsdel/$',views.goodsdel,name='admin_goodsdel'),
 url(r'^goodsedit/$',views.goodsedit,name='admin_goodsedit'),
 url(r'^goodsimgdel/$', views.goodsImgDel, name='admin_goodsimgdel'),
 url(r'^dogoodsedit/$', views.doGoodsEdit, name='admin_dogoodsedit'),


 url(r'^addpower/$',views.addpower,name='admin_addpower'),
 url(r'^doaddpower/$',views.doaddpower,name='admin_doaddpower'),
 url(r'^addrole/$',views.addrole,name='admin_addrole'),
 url(r'^doaddrole/$',views.doaddrole,name='admin_doaddrole'),

 url(r'^addfloor/$',views.addfloor,name='admin_addfloor'),
 url(r'^doaddfloor/$',views.doaddfloor,name='admin_doaddfloor'),
 url(r'^addfloorgoods/$',views.addfloorgoods,name='admin_addfloorgoods'),
 url(r'^doaddfloorgoods/$',views.doaddfloorgoods,name='admin_doaddfloorgoods'),

]
