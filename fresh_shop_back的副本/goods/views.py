from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from fresh_shop_back.settings import PAGE_NUMBER
from goods.models import GoodsCategory, Goods
from goods.form import GoodsForm

#
# @login_required
# def goods_desc(request):
#     if request.method == 'GET':
#         return render(request, 'goods_desc.html')


@login_required
def goods_detail(request):
    if request.method == 'GET':
        return render(request, 'goods_detail.html')
    if request.method == 'POST':
        data = request.POST
        form = GoodsForm(data)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            goods_sn = form.cleaned_data.get('goods_sn')
            goods_nums = form.cleaned_data.get('goods_nums')
            market_price = form.cleaned_data.get('market_price')
            shop_price = form.cleaned_data.get('shop_price')
            goods_brief = form.cleaned_data.get('goods_brief')
            category = request.POST.get('category')
            goods_front_image = request.FILES.get('goods_front_image')
            Goods.objects.create(name=name,
                                 goods_sn=goods_sn,
                                 goods_nums=goods_nums,
                                 market_price=market_price,
                                 shop_price=shop_price,
                                 goods_brief=goods_brief,
                                 category_id=category,
                                 goods_front_image=goods_front_image)
            return HttpResponseRedirect(reverse('goods:goods_list'))
        else:
            return render(request, 'goods_detail.html', {'errors': form.errors})


@login_required
def good_update(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        good = Goods.objects.filter(pk=id).first()
        return render(request, 'good_update.html', {'good':good})
    if request.method == 'POST':
        id = request.GET.get('id')
        data = request.POST
        form = GoodsForm(data)
        if form.is_valid():
            category = request.POST.get('category')
            goods_front_image = request.FILES.get('goods_front_image')
            good = Goods.objects.filter(id=id).first()
            good.category_id = category
            good.goods_front_image = goods_front_image
            good.save()
            Goods.objects.filter(pk=id).update(**form.cleaned_data)
            return HttpResponseRedirect(reverse('goods:goods_list'))
        else:
            return render(request, 'goods_detail.html', {'errors':form.errors})


@login_required
def goods_list(request):
    if request.method == 'GET':
        goods = Goods.objects.all()
        categorys = GoodsCategory.CATEGORY_TYPE
        try:
            page = int(request.GET.get('page', 1))
        except Exception as e:
            page = 1
        paginator = Paginator(goods, PAGE_NUMBER)
        good_now = paginator.page(page)
        return render(request, 'goods_list.html', {'goods': good_now, 'categorys': categorys, 'page': page})


@login_required
def goods_category_list(request):
    if request.method == 'GET':
        categorys = GoodsCategory.objects.all()
        types = GoodsCategory.CATEGORY_TYPE
        return render(request, 'goods_category_list.html', {'categorys':categorys, 'types':types})


@login_required
def goods_category_detail(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        category = GoodsCategory.objects.filter(pk=id).first()
        types = GoodsCategory.CATEGORY_TYPE
        return render(request, 'goods_category_detail.html', {'category':category, 'types':types})

    if request.method == 'POST':
        img = request.FILES.get('category_front_image')
        id = request.GET.get('id')
        if img:
            category = GoodsCategory.objects.filter(pk=id).first()
            category.category_front_image = img
            category.save()
            return HttpResponseRedirect(reverse('goods:goods_category_list'))
        else:
            error = '图片必填'
            return render(request, 'goods_category_detail.html', {'error': error})


@login_required
def del_good(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        Goods.objects.filter(id=id).first().delete()
        return HttpResponse('删除对应商品成功！')


# @login_required
# def order_list(request):
#     if request.method == 'GET':
#         return render(request, 'order_list.html')

#
# @login_required
# def user_list(request):
#     if request.method == 'GET':
#         return render(request, 'user_list.html')


def goods_edit(request, id):
    if request.method == 'GET':
        goods = GoodsCategory.objects.filter(pk=id).first()
        types = GoodsCategory.CATEGORY_TYPE
        return render(request, 'goods_detail.html', {'goods': goods, 'types': types})
    if request.method == 'POST':
        form = GoodsForm(request.POST, request.FILES)
        if form.is_valid():
            # 验证成功
            data = form.cleaned_data
            # 把图片从data中删除
            # img表示商品时 选择了图片 则img为图片的内容
            # 如果在更新商品的时候 没有选择图片 则img为None
            img = data.pop('goods_front_image')
            data = form.cleaned_data
            # 更新除了图片的其他的字段信息
            Goods.objects.filter(pk=id).updata(**data)
            if img:
                # 更新图片的信息
                goods = Goods.objects.filter(pk=id).first()
                goods.goods_front_image = img
                goods.save()
            return HttpResponseRedirect(reverse('goods:goods_list'))
        else:
            # 修改失败
            goods = GoodsCategory.objects.filter(pk=id).first()
            types = GoodsCategory.CATEGORY_TYPE
            return render(request, 'goods_datail.html', {'errors': form.errors, 'goods': goods, 'types': types})


def goods_desc(request, id):
    if request.method == 'GET':
        return render(request, 'goods_desc.htlm')
    if request.method == 'POST':

        # 获取编辑器的内容
        content = request.POST.get('content')

        # 获取修改商品对象
        goods = Goods.objects.filter(pk=id).first()
        goods.goods_desc = content
        goods.save()
        return HttpResponseRedirect(reverse('goods: goods_list'))
