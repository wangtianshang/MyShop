from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^base/',views.base),
    url(r'^index/$',views.index,name='goods_index'),
    url(r'^list/',views.goods_list,name='goods_list'),
    url(r'^showdetails/',views.showdetails,name='goods_showdetails'),
    url(r'^addcar/',views.addshoppingcart,name='goods_addcar'),
    url(r'^carlist/',views.carlist,name='goods_carlist'),
]
