# --*-- coding: utf-8 --*--

from django import forms
from django.contrib.auth  import authenticate, login

class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField()

    def get_success_url(self):
        return '/'

class CheckBoxForm(forms.Form):
    CHOICES = ((0, 'qwe'), (1, 'rty'), (2, 'asd'))
    checkbox = forms.TypedChoiceField(choices = CHOICES, widget = forms.CheckboxSelectMultiple)
