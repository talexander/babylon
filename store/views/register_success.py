# --*-- coding: utf-8 --*--

from django.views.generic import TemplateView

class RegisterSuccessView(TemplateView):
    template_name = 'register_success.tpl'
