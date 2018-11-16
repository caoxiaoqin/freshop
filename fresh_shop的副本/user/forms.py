# encoding: utf-8
"""
@author: 曹晓芹

"""
from django import forms
from user.models import User


class UserLogin(forms.Form):
    username = forms.CharField(max_length=20, required=True,
                               error_messages={
                                   'max_length': '用户名最长不超过20个字符哟~',
                                   'required': '用户是必填的哟'
                               })
    pwd = forms.CharField(max_length=255, required=True,
                          error_messages={
                              'max_length': '密码最长不超过255个字符哟',
                              'required': '密码是必填的哟'
                          })

    def clean(self):
        user = User.objects.filter(username=self.cleaned_data.get('username')).first()
        if not user:
            raise forms.ValidationError({'username': '该账号没有被注册，请去注册额'})
        return self.cleaned_data

