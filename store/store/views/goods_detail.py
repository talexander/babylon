# --*-- coding: utf-8 --*--

from django.views.generic import DetailView
from store.models import Good

class GoodsDetailView(DetailView):
    model = Good
    context_object_name = 'goods'
    template_name = 'goods_detail.tpl'
