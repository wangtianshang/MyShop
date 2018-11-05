from xadmin.models import types
from user.models import shop_cart
def getMenu(request):
    types_list = types.objects.filter(parent_id=0).order_by('id')[:10]
    # [ [ { []}]]
    all_data = []
    for one_list in types_list:
        # 找到第二级的数据
        two_list = types.objects.filter(parent_id=one_list.id)
        two_data = []
        for two_type in two_list:
            lis = {}
            lis['name'] = two_type.name
            lis['id'] = two_type.id
            three_list = types.objects.filter(parent_id=two_type.id)
            lis['list'] = three_list
            two_data.append(lis)
        all_data.append(two_data)
    cou = shop_cart.objects.all()
    num = 0
    for i in cou:
        num += 1
    return {'type_lis': types_list, 'all_data': all_data,'num':num}

def count(request):
    cou = shop_cart.objects.all()
    num=0
    for i in cou:
        num+=1
    print(1)
    return {'num':num}