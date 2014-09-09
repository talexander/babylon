# -*- coding: utf-8 -*-

from django.views.generic.edit import FormView
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User

from store.forms.login import LoginForm

class LoginView(FormView):
    template_name = "login.tpl"
    form_class = LoginForm
    success_url = '/'
    error = ''


    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(email = email, password = password)
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return super(LoginView, self).form_valid(form)
            else:
                self.error = u'Пользователь заблокирован.'
        else:
            self.error = u'Пользователь с таким email не найден.'

        return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['login_error'] = self.error
        return context

