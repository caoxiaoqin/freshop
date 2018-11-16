# encoding: utf-8
"""
@author: 曹晓芹

"""
from django import forms
from django.contrib.auth.models import User


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=15, min_length=2, required=True,
                               error_messages={
                                   'required': '必填',
                                   'max_length': '最长15',
                                   'min_length': '最短2'
                               })
    password = forms.CharField(required=True,
                               error_messages={
                                   'required': '必填',
                               })

    def clean(self):
        # 使用django自带的User模块进行验证
        user = User.objects.filter(username=self.cleaned_data.get('username')).first()
        if not user:
            raise forms.ValidationError({'username': '该账号没有注册'})
        return self.cleaned_data
