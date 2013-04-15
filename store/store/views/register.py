# -*- coding: utf-8 -*-

from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from store.forms.register import RegisterForm
from django.contrib.auth.models import User
from django.shortcuts import redirect

import random

class RegisterView(FormView):
    template_name = "register.tpl"

    form_class = RegisterForm
    success_url = '/register/success/'

    def form_valid(self, form):
        user = User.objects.create_user(form.data['first_name'], form.data['email'], form.data['password'], first_name = form.data['first_name'], last_name=form.data['last_name']);
        return super(RegisterView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)
        context['rand'] = random.randint(0, 10000)
        return context


    def post(self, request, *args, **kwargs):
        return super(RegisterView, self).post(request, *args, **kwargs)


    def dispatch(self, request, *args, **kwargs):
        # если на руках авторизованный пользователь, то уводим пользователя отсюда
        if request.user.is_authenticated():
            redirect('/')
        return super(RegisterView, self).dispatch(request, *args, **kwargs)


