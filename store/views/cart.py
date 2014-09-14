from django.views.generic import TemplateView
from django.views.generic.base import ContextMixin
from store.views.base import BaseView
import logging
import json
from urllib import unquote
from store import models
from store.utils import get_cart_items

logger = logging.getLogger(__name__)

class CartView(BaseView, TemplateView):
    template_name = "cart.tpl"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CartView, self).get_context_data(**kwargs)
        context.update(self.common_vars())
        str = unquote(self.request.COOKIES.get('cart.items', ''))
        items = get_cart_items(str)
        if len(items):
            context['cart'] = items
        return context