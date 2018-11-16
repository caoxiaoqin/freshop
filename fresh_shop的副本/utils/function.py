# encoding: utf-8
"""
@author: 曹晓芹

"""
from django.http import HttpResponseRedirect
from django.urls import reverse


def login_token(func):
    def check_login(request):
        try:
            request.session.get('user.id')
        except Exception as e:
            return HttpResponseRedirect(reverse('user:login'))

        return func(request)
    return check_login
