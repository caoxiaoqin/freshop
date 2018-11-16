# encoding: utf-8
"""
@author: 曹晓芹

"""
from django.conf.urls import url

from user import views

urlpatterns = [
    # 登录
    url(r'^login/', views.login, name='login'),
    url(r'^index/', views.index, name='index'),
]
