# *-* coding: utf-8 -*-

from django.views.generic import ListView
from store.models import Good
from django.core.paginator import Paginator

class GoodsListView(ListView):
    model = Good
    template_name = 'goods_list.tpl'
    context_object_name = 'goods_list'
    paginate_by = 10

    def get_query_set(self):
        return  Good.objects.order_by('+id')

    def get_context_data(self, **kwargs):
        context = super(GoodsListView, self).get_context_data(**kwargs)
        return context
