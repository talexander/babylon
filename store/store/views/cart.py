from django.views.generic import TemplateView
from django.views.generic.base import ContextMixin
from store.views.base import BaseView
import logging
import json
from urllib import unquote
from store import models

logger = logging.getLogger(__name__)

class CartView(BaseView, TemplateView):
    template_name = "cart.tpl"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CartView, self).get_context_data(**kwargs)
        context.update(self.common_vars())
        context['items'] = 111
        str = unquote(self.request.COOKIES.get('cart.items', ''))
        if(len(str) > 0 ):
            data = str.split(';')
            logger.debug('data: %s' % json.dumps(data))
            ids = items = []
            for pair in data:
                try:
                    r = {}
                    v = pair.split(':')
                    r['id'] = v[0]
                    r['count'] = v[-1]
                    v2 = r['id'].split('_')
                    if len(v2) > 1:
                        logger.debug('here')
                        r['id'] = v2[0]
                        r['sku'] = v2[-1]
                    r['product'] = models.Good.objects.get(pk=r['id'])
                    if r.get('sku', False):
                        r['sku'] = r['product'].sku(r.get('sku'))
                    logger.debug(r['product'].price)
                    items.append(r)
                except Exception,e:
                    logger.error(e)
                    continue
            context['cart'] = items

        return context