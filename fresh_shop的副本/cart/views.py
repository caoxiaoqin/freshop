from django.http import JsonResponse
from django.shortcuts import render

from cart.models import ShoppingCart
from goods.models import Goods


def add_cart(request):
    if request.method == 'POST':
        # 加入到购物车 需要判断是否登录
        # 如果登录 加入到购物车的数据 其实就是加入到数据库中购物车表（）
        # 如果登录 加入到购物车的数据 存储到session里（设计比较好的）
        # 如果没有登录 加入到购物车的数据就是加入到session里
        # 如果登录 则把session里数据同步到数据库中

        # session里存储的数据 商品的id 商品的数量 商品的选择状态
        # 1 获取商品的id(goods_id )和商品数量(goods_num)
        goods_id = int(request.POST.get('goods_id'))
        goods_num = int(request.POST.get('goods_num'))
        # 组装存到session 里的数据格式
        # 商品的id(goods_id )和商品数量(goods_num) 商品是否被选中（1）
        goods_list = [goods_id, goods_num, 1]
        # {'goods': [12,2,1]}
        if request.session.get('goods'):
            # 说明session里存储了加入得到购物车的商品信息
            # 判断当前加入到购物车中的数据 是否存在session中
            # 存在 则修改session中该商品的数量
            # 如果不存在  则就新增
            flag = 0
            session_goods = request.session['goods']
            for goods in session_goods:
                # 判断 加入购物车的数据 已经存在session里 就修改
                if goods[0] == goods_id:
                    goods[1] = int(goods[1]+int(goods_num))
                    flag = 1
            if not flag:
                #  如果不存在就添加
                session_goods.append(goods_list)
                request.session['goods'] = session_goods
            goods_count = len(session_goods)

        else:
            data = []
            data.append(goods_list)
            request.session['goods'] = data
            goods_count = 1
        return JsonResponse({'code': 200, 'msg': '请求成功', 'goods_count': goods_count})


def cart(request):
    if request.method == 'GET':
        # 没有登录 则从session 中取商品
        # 登录了 还是从session中的数据（保证session和数据的商品一致）
        session_goods = request.session.get('goods')
        if session_goods:
            goods_all = []
            # 获取session里所有商品的id值
            for goods in session_goods:
                # 获取所有商品对象
                # 前台需要返回商品的信息 商品的个数 商品的总价
                cart_goods = Goods.objects.filter(pk=goods[0]).first()
                goods_number = goods[1]
                total_price = goods[1] * cart_goods.shop_price
                # 后台返回结构 [[goods.objects, number, total_price], [goods.objects, number, total_price]]
                goods_all.append([cart_goods, goods_number, total_price])

        else:
            goods_all = ''
        return render(request, 'cart.html', {'goods_all': goods_all})


# 结算
def place_order(request):
    if request.method == 'GET':
        user_id = request.session.get('user_id')
        carts = ShoppingCart.objects.filter(user_id=user_id,
                                            is_select=1).all()
        for cart in carts:
            cart.total_price = int(cart.nums) * int(cart.goods.shop_price)
        return render(request, 'place_order.html', {'carts': carts})
