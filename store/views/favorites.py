# -*- coding: utf-8 -*-

from django.views.generic import TemplateView, ListView
from django.views.generic.base import ContextMixin
from store.views.base import BaseView
from store import models
import store.utils as sUtils
import logging
import json
from urllib import unquote
from django.utils.safestring import mark_safe, SafeData

# Get an instance of a logger
logger = logging.getLogger(__name__)

class FavoritesView(ListView, BaseView):
    model = models.Good
    # queryset = Book.objects.order_by('-publication_date')
    template_name = "favorites.tpl"

    context_object_name = 'goods_list'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        logger.debug('favorites: %s' % json.dumps(self.request.COOKIES))
        context = super(FavoritesView, self).get_context_data(**kwargs)
        context.update(self.common_vars())
        return context

    def get_queryset(self):
        q = models.Good.objects.filter()
        ids  = sUtils.parseFavourites(unquote(self.request.COOKIES.get('favoriteGoods', '')))
        logger.info('ids: %s' % json.dumps(ids))
        q = q.filter(pk__in = ids)


        q = q.order_by('-left_amount')
        return q

