# encoding: utf-8
"""
@author: 曹晓芹

"""

from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import static

from order import views

urlpatterns = [
    # url(r'^place_order/', views.place_order, name='place_order')
    url(r'^order/', views.order, name='order'),
]