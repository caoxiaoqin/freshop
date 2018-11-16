from django.conf.urls import url

from goods import views


urlpatterns = [
    # 商品分类
    url(r'^goods_category_list/', views.goods_category_list, name='goods_category_list'),
    # 商品分类编辑
    url(r'^goods_category_detail/', views.goods_category_detail, name='goods_category_detail'),
    url(r'^goods_desc/(\d+)', views.goods_desc, name='goods_desc'),
    url(r'^goods_detail/', views.goods_detail, name='goods_detail'),
    url(r'^goods_list/', views.goods_list, name='goods_list'),
    # 删除商品
    url(r'^del_good/', views.del_good, name='del_good'),
    # # 商品信息修改
    url(r'^good_update/', views.good_update, name='good_update'),
    url(r'^goods_edit/', views.goods_edit, name='goods_edit'),
    # url(r'^user_list/', views.user_list, name='user_list'),

]