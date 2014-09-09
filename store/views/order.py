from django.views.generic import TemplateView
from django.views.generic.base import ContextMixin
from store.views.base import BaseView
import logging
import json
from urllib import unquote
from store import models

logger = logging.getLogger(__name__)

class OrderView(BaseView, TemplateView):
    template_name = "order.tpl"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(OrderView, self).get_context_data(**kwargs)
        context.update(self.common_vars())
        return context