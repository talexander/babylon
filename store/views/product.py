# -*- coding: utf-8 -*-

from django.views.generic import TemplateView, DetailView
from django.views.generic.base import ContextMixin
from store.views.base import BaseView
from store import models
import logging
logger = logging.getLogger(__name__)

class ProductView(DetailView, BaseView):
    model = models.Good
    # queryset = Book.objects.order_by('-publication_date')
    template_name = "product.tpl"
    # queryset = models.Good.objects.prefetch_related('good_category','vendor','consist','consist_unified')
    context_object_name = 'item'
    slug_field = 'alias'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ProductView, self).get_context_data(**kwargs)

        context.update(self.common_vars())
        return context

    def seo(self):
        s = super(ProductView, self).seo()

        upd = {
            'keywords': self.object.property(models.Property.PROP_ALIAS_SEO_KEYWORDS),
            'description': self.object.property(models.Property.PROP_ALIAS_SEO_DESCR),
        }

        for k in upd:
            v = upd[k]
            if not v:
                upd[k] = s.get(k, '')

        return upd
