# -*- coding: utf-8 -*-

from django.views.generic import TemplateView
import random

class RegisterView(TemplateView):
    template_name = "register.tpl"
    def get_context_data(self, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)
        context['rand'] = random.randint(0, 10000)
        return context


