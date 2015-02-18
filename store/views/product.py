# -*- coding: utf-8 -*-

from django.views.generic import TemplateView, DetailView
from django.views.generic.base import ContextMixin
from store.views.base import BaseView
from store import models
import logging
import json
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

logger = logging.getLogger(__name__)

class ProductView(DetailView, BaseView):
    model = models.Good
    # queryset = Book.objects.order_by('-publication_date')
    template_name = "product.tpl"
    # queryset = models.Good.objects.prefetch_related('good_category','vendor','consist','consist_unified')
    context_object_name = 'item'
    slug_field = 'alias'
    api_call = False

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ProductView, self).get_context_data(**kwargs)

        context.update(self.common_vars())
        return context

    def render_to_response(self, context, **response_kwargs):
        if not self.api_call and not self.kwargs.get('vendor', False):
            url = reverse('product_url_long', kwargs={'category': context['object'].good_category.alias, 'vendor': context['object'].vendor.alias, 'slug': context['object'].alias })
            return redirect(url, permanent=True)

        return super(ProductView, self).render_to_response(context, **response_kwargs)


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

    def title(self):
        return u'%s: «%s, %s».  Интернет—магазин «Улиткина пряжа»' % (self.object.good_category.name, self.object.vendor.name, self.object.name)
