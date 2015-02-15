# -*- coding: utf-8 -*-

from django.views.generic import TemplateView, ListView
from django.views.generic.base import ContextMixin
from store.views.base import BaseView
from store import models
import store.utils as sUtils
import logging
import json
from django.utils.safestring import mark_safe, SafeData

# Get an instance of a logger
logger = logging.getLogger(__name__)

class GoodsFilterView(ListView, BaseView):
    model = models.Good
    # queryset = Book.objects.order_by('-publication_date')
    template_name = "index.tpl"

    context_object_name = 'goods_list'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(GoodsFilterView, self).get_context_data(**kwargs)

        context.update(self.common_vars())
        show_filter = True
        context['not_filled_yet'] = False
        if (self.kwargs.get('category', '')):
            show_filter = False
            cat = str(self.kwargs.get('category', ''))
            cat_list = cat.split('+')
            if cat_list and models.GoodCategory.ALIAS_YARN in cat_list:
                show_filter = True
            else:
                context['not_filled_yet'] = True
        if show_filter:
            context['filter_data'] = self.filter_data()
            context['gf'] = {
                'price_from': self.request.GET.get('gf_price_from', ''),
                'price_to': self.request.GET.get('gf_price_to', ''),
                'length_from': self.request.GET.get('gf_length_from', ''),
                'length_to': self.request.GET.get('gf_length_to', ''),
                'vendors':  [sUtils.intval(x) for x in self.request.GET.getlist('gf_vendor', [])],
                'colours': [sUtils.intval(x) for x in self.request.GET.getlist('gf_colour', [])],
                'consists': [sUtils.intval(x) for x in self.request.GET.getlist('gf_consist', [])],
                'q': self.request.GET.get('q', ''),
            }


        return context

    def filter_data(self):
        filter = {
            'color': models.Colour.objects.all().order_by('name'),
            'vendor': models.Vendor.objects.all().order_by('name'),
            'consist': models.GoodConsistUnified.objects.all().order_by('name'),
        }
        return filter


    def get_queryset(self):
        q = models.Good.active()
        if (self.request.GET.get('q', '')):
            qq = models.Good.search.query(self.request.GET.get('q', '')).order_by('@weight')
            ids = [sUtils.intval(x.id) for x in qq[0:100]]
            q = q.filter(pk__in = ids)

        logger.debug('args: %s, kwargs: %s' % (json.dumps(self.args), json.dumps(self.kwargs)))
        if (self.kwargs.get('category', '')):
            cat = str(self.kwargs.get('category', ''))
            cat_list = cat.split('+')
            logger.debug('cat list: %s' % json.dumps(cat_list))

            product_category = models.GoodCategory.objects.filter(alias__in=cat_list)
            q = q.filter(good_category__in = product_category)
            # logger.debug('categories: %s' % json.dumps(product_category.values_list(id, flat=True)))


        price_from = sUtils.intval(self.request.GET.get('gf_price_from', 0))
        price_to = sUtils.intval(self.request.GET.get('gf_price_to', 0))
        logger.debug('price_from %d, price_to: %d' % (price_from, price_to))

        length_from = sUtils.intval(self.request.GET.get('gf_length_from', 0))
        length_to = sUtils.intval(self.request.GET.get('gf_length_to', 0))
        logger.debug('length_from %d, length_to: %d' % (length_from, length_to))

        vendor_ids = self.request.GET.getlist('gf_vendor', [])
        logger.debug('vendors: %s' % json.dumps(vendor_ids))

        colour_ids = [sUtils.intval(x) for x in self.request.GET.getlist('gf_colour', [])]
        logger.debug('colours: %s' % json.dumps(colour_ids))
        logger.debug('session, keys: %s, items: %s' % (json.dumps(self.request.session.keys()), json.dumps(self.request.session.keys()),))
        logger.debug('session, key: %s' % self.request.session.session_key)

        consists_ids = [sUtils.intval(x) for x in self.request.GET.getlist('gf_consist', [])]
        logger.debug('consists: %s' % json.dumps(consists_ids))

        if (len(consists_ids) > 0):
            q = q.filter(consist_unified__in = consists_ids)


        if (len(colour_ids) > 0):
            g_ids = models.ProductSKU.objects.filter(unified_colour__in = colour_ids).values_list('good', flat=True)
            q = q.filter(pk__in = g_ids)

        if (len(vendor_ids) > 0):
            q = q.filter(vendor__in = vendor_ids)

        if(price_from > 0):
            q = q.filter(price__gte = price_from)
        if(price_to > 0 and price_to >= price_from):
            q = q.filter(price__lte = price_to)

        if(length_from > 0 or length_from > 0):
            props = models.Property.objects.filter(alias = models.Property.PROP_ALIAS_LENGTH)
            goods_props = models.GoodProperty.objects.filter(prop = props)
            if(length_from > 0):
                goods_props = goods_props.filter(val__gte = length_from)

            if(length_to > 0 and length_to >= length_from):
                goods_props = goods_props.filter(val__lte = length_to)

            goods_ids = goods_props.values_list('good_id', flat=True)
            q = q.filter(id__in = goods_ids)

        q = q.order_by('-left_amount')
        return q

