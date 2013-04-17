# --*-- coding: utf-8 --*--

from django import forms
from django.contrib.auth  import authenticate, login

class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField()

    def get_success_url(self):
        return '/'


