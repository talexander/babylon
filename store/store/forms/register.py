# -*- coding: utf-8 -*-

from django import forms

class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length = 100)
    last_name = forms.CharField(max_length = 100)
    email = forms.EmailField()
    address = forms.CharField(max_length = 255)
