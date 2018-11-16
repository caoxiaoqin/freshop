from django.shortcuts import render

from goods.models import GoodsCategory, Goods
from utils.function import login_token


@login_token
def index(request):
    if request.method == 'GET':
        # {key1:[value1,value2],key1:[value3,value4]}
        categorys = GoodsCategory.CATEGORY_TYPE
        goods = Goods.objects.all()
        goods_dict = {}

        for category in categorys:
            goods_list = []
            count = 0
            for good in goods:
                # 判断商品分类和商品对象
                if count < 4:
                    if category[0] == good.category_id:
                        goods_list.append(good)
                        count += 1
            # {新鲜水果：[], 海鲜水产：[]...}
            goods_dict[category[1]] = goods_list
        return render(request, 'index.html', {'goods_dict': goods_dict})


def detail(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        goods = Goods.objects.filter(pk=id).first()
        return render(request, 'detail.html', {'goods': goods})
