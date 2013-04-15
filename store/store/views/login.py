# -*- coding: utf-8 -*-

from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from store.forms.login import LoginForm

class LoginView(FormView):
    template_name = "login.tpl"
    form_class = LoginForm
