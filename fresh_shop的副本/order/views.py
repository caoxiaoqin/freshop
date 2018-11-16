from django.http import JsonResponse
from django.shortcuts import render

from cart.models import ShoppingCart
from order.models import OrderGoods, OrderInfo


def order(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        carts = ShoppingCart.objects.filter(user_id=user_id,
                                            is_select=1).all()
        # 计算总金额
        order_mount = 0
        for cart in carts:
            order_mount += int(cart.nums) * int(cart.goods.shop_price)
        # 创建订单
        order = OrderInfo.objects.create(user_id=user_id,
                                         order_sn='',
                                         order_mount='order_mount')

        # 创建订单详情信息
        for cart in carts:
            OrderGoods.objects.create(order=order,
                                      goods=cart.goods,
                                      goods_nums=cart.nums)
        # 删除购物车里已经下单的商品信息
        carts.delete()
        return JsonResponse({'code': 200, 'msg': '请求成功'})
