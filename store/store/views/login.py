# -*- coding: utf-8 -*-

from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from store.forms.login import LoginForm

class LoginView(FormView):
    template_name = "login.tpl"
    form_class = LoginForm


    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
#        user = authenticate()

        return super(LoginForm, self).form_valid(form)
