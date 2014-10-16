# -*- coding: utf-8 -*-

from django.views.generic import TemplateView,FormView
from django.views.generic.base import ContextMixin
from store.views.base import BaseView
import logging
import json
from urllib import unquote
from store import models
from store.forms.base import OrderForm
from django.http import HttpResponseRedirect
from store import utils
from django.db import transaction
from django.core import mail
from django.template.loader import render_to_string
from store import settings

logger = logging.getLogger(__name__)

class OrderView(BaseView, FormView):
    template_name = "order.tpl"
    form_class = OrderForm
    success_url = '/order/success'
    success = None

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        context.update(self.common_vars())
        str = unquote(self.request.COOKIES.get('cart.items', ''))
        items = utils.get_cart_items(str)
        if len(items):
            context['cart'] = items
            context['total'] = reduce(lambda res, item: res + item['summ'], items, 0)

        context['order_form'] = OrderForm()

        return context

    def form_valid(self, form):
        str = unquote(self.request.COOKIES.get('cart.items', ''))
        items = utils.get_cart_items(str)
        if len(items) == 0:
            return HttpResponseRedirect('/order/new')

        with transaction.atomic():
            order = models.Order.objects.create(
                fname = form.cleaned_data.get('fname'),
                phone = form.cleaned_data.get('phone'),
                email = form.cleaned_data.get('email'),
                delivery = utils.intval(form.cleaned_data.get('delivery')),
                payment = utils.intval(form.cleaned_data.get('payment')),
                comment = form.cleaned_data.get('comment'),
                ip = utils.get_client_ip(self.request),
            )
            for x in items:
                order_product = models.OrderProduct.objects.create(
                    order = order,
                    product = x.get('product'),
                    sku = x.get('sku', None),
                    amount = utils.intval(x.get('count')),
                    price = x.get('product').price,
                )

        if order.id:
            html_content = render_to_string('mail/order.tpl', {
                'STATIC_URL': 'http://nitki-ulitki.ru/',
                'order': order,
            })
            from_email = 'order@nitki-ulitki.ru'
            to = order.email
            msg = mail.EmailMessage(u'Подтверждение оформления заказа', html_content, from_email, [to])
            msg.content_subtype = "html"
            msg.send()

            html_content = render_to_string('mail/order.tpl', {
                'STATIC_URL': 'http://nitki-ulitki.ru/',
                'order': order,
                'admin': True,
            })
            msg = mail.EmailMessage(u'Новый заказ №%d' % order.id, html_content, from_email, [from_email])
            msg.content_subtype = "html"
            msg.send()


        return super(OrderView, self).form_valid(form)

    def render_to_response(self, context, **response_kwargs):
        response = super(OrderView, self).render_to_response(context, **response_kwargs)
        if self.success:
            response.set_cookie("cart.items", '')
        return response