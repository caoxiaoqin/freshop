from django import forms


class GoodsForm(forms.Form):
    name = forms.CharField(max_length=10, required=True, error_messages={
        'max_length': '商品名最长不超过10字符',
        'required': '商品名必填'
    })
    goods_sn = forms.CharField(max_length=10, required=True, error_messages={
        'max_length': '货号最长不超过10字符',
        'required': '商品货号必填'
    })
    goods_nums = forms.CharField(max_length=10, required=True, error_messages={
        'max_length': '最长不超过10字符',
        'required': '库存必填'
    })
    market_price = forms.CharField(max_length=10, required=True, error_messages={
        'max_length': '价格栏最长不超过10字符',
        'required': '市场价格必填'
    })
    shop_price = forms.CharField(max_length=10, required=True, error_messages={
        'max_length': '价格栏最长不超过10字符',
        'required': '本店价格必填'
    })
    goods_brief = forms.CharField(max_length=100, required=True, error_messages={
        'max_length': '描述最长不超过100字符',
        'required': '描述必填'
    })

    def clean(self):
        return self.cleaned_data
