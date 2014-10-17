# -*- coding: utf-8 -*-

from django.views.generic import TemplateView, ListView
from django.views.generic.base import ContextMixin
from store.views.base import BaseView
from store import models

class IndexView(ListView, BaseView):
    model = models.Good
    # queryset = Book.objects.order_by('-publication_date')
    template_name = "index.tpl"

    context_object_name = 'goods_list'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(IndexView, self).get_context_data(**kwargs)

        context.update(self.common_vars())
        context['filter_data'] = self.filter_data()
        return context

    def filter_data(self):
        filter = {
            'color': models.Colour.objects.all().order_by('name'),
            'vendor': models.Vendor.objects.all().order_by('name'),
            'consist': models.GoodConsistUnified.objects.all().order_by('name'),
        }
        return filter


    # def get_queryset(self):
    #     self.publisher = get_object_or_404(Publisher, name=self.args[0])
    #     return Book.objects.filter(publisher=self.publisher)
