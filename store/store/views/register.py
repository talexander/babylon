# -*- coding: utf-8 -*-

from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from store.forms.register import RegisterForm

import random

class RegisterView(FormView):
    template_name = "register.tpl"

    form_class = RegisterForm
    success_url = '/register/success/'

    def form_valid(self, form):
        return super(RegisterView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)
        context['rand'] = random.randint(0, 10000)
        return context


