# encoding: utf-8
"""
@author: 曹晓芹

"""
import re

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from cart.models import ShoppingCart
from user.models import User


class UserAuthMiddlewareMixin(MiddlewareMixin):
    """中间键"""
    def process_request(self, request):
        # 给request.user赋值 赋的值为当前登录系统的用户对象
        user_id = request.session.get('user_id')
        if user_id:
            # 登录了
            user = User.objects.filter(pk=user_id).first()
            request.user = user
            # 可以访问所有的页面
            return None

            # 首页详情 不管登录与否都可以查看
            # 下单结算订单 个人中心登录查看
        # 不需要登录就可以访问的url
        not_need_path = ['/user/login/', '/user/register/',
                         '/goods/index/', '/goods/detail/',
                         '/media/(.*)/', '/static/(.*)',
                         '/cart/cart/', '/cart/add_carts']
        path = request.path
        for not_path in not_need_path:
            # 匹配当前路径是否为不需要登录验证的路径
            if re.match(not_path, path):
                return None
        # 当前的请求URL不在not_need_path中 则表示当前的url是需要登录之后才能访问
        return HttpResponseRedirect(reverse('user:login'))


class SessionUpdate(MiddlewareMixin):

    def process_request(self, request):
        # session中商品的数据和购物车表中的同步操作
        # session中的数据结构[[id, number, is_select], [id1, number1, is_select]]
        session_goods = request.session.get('goods')
        user_id = request.session.get('user_id')
        if user_id:
            # 用户登录 才做同步
            if session_goods:
                # 时刻保持session中数据和数据库中数据同步
                # 如果session中商品已经存在数据库表中 则更新
                # 如果session中商品不存在数据库表中 则添加
                # 如果session中商品少于数据库表中的商品 则更新
                for goods in session_goods:
                    # goods的结构[id , num,is_select ]
                    cart = ShoppingCart.objects.filter(user_id=user_id,
                                                       goods_id=goods[0]).first()
                    if cart:
                        cart.nums = goods[1]
                        cart.is_select = goods[2]
                        cart.save()
                    else:
                        # 数据库中查询不到该商品 则添加、
                        ShoppingCart.objects.create(user_id=user_id,
                                                    goods_id=goods[0],
                                                    nums=goods[1],
                                                    is_select=goods[2])
            # 将数据库数据同步到session
            carts = ShoppingCart.objects.filter(user_id=user_id).all()
            # sesssion中的数据结构[[id, number, is_select]]
            session_new_goods = [[cart.goods_id, cart.nums, cart.is_select] for cart in carts]
            request.session['goods'] = session_new_goods
        return None


