from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponseRedirect, reverse,render
from django.conf import settings
from xadmin.models import powers
from django.http import HttpResponse
class MyMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # 定义通过名单
        mingdan = [settings.LOGIN_URL]
        uid = request.session.get('uid', 0)
        # 进入前台页面时不用走这个中间件
        import re
        url = request.path
        # print(url)
        pattern = re.compile(r'^/admin/')
        is_exists = re.match(pattern, url)

        print()

        if uid == 0 and is_exists != None and request.path not in mingdan:
            return HttpResponseRedirect('/admin/login/')
        # if uid == 0:
        #     return HttpResponseRedirect(reverse('admin_login'))
    # 中间件  判断该用户是否拥有某权限，有的话才可以访问

    # 设置权限的时候 需要在数据库里面进行手动添加，我的数据库中角色1 没有设置权限
    def process_view(self, request, callback, callback_args, callback_kwargs):
        # 这句话可以找到操作的那个权限的url_name
        url_name = request.resolver_match.url_name
        from .models import powers
        # print(url_name)
        info = powers.objects.filter(url_name=url_name).first()
        # print(info)
        if info != None:
            if info.id not in request.session.get('user_powers'):
                return HttpResponse('对不起，您没有访问该功能的权限')

