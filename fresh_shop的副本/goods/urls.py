# encoding: utf-8
"""
@author: 曹晓芹

"""
from django.conf.urls import url

from goods import views

urlpatterns = [
    url(r'^index/', views.index, name='index'),
    # 商品详情
    url(r'^detail/', views.detail, name='detail'),


]
