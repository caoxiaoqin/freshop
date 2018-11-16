from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from user.forms import UserLoginForm


def login(request):
    # get请求返回登录页面
    if request.method == 'GET':
        return render(request, 'login.html')
    # POST
    if request.method == 'POST':
        # 拿到post请求的参数存在data里
        data = request.POST
        # 创建一个类UserLoginForm
        # 将请求参数去给form表单做验证
        form = UserLoginForm(data)
        # 校验结果：返回true表示校验成功 就是有user
        if form.is_valid():
            # 使用随机标识符token
            user = auth.authenticate(username=form.cleaned_data.get('username'),
                                     password=form.cleaned_data.get('password'))
            if not user:
                # 没有user对象 表示验证密码不通过
                return render(request, 'login.html', {'msg': '密码错误'})
            else:
                # 实现登录 request, user等于登录系统用户对象
                auth.login(request, user)
                return HttpResponseRedirect(reverse('user:index'))
        # 校验结果：返回false表示校验失败 就是没有user
        else:
            # 验证失败 返回错误信息给页面
            # return render(request, 'login.html', {'errors': form.errors})
            errors = form.errors
            return render(request, 'login.html', {'errors': errors})


@login_required
def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')
