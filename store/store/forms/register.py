# -*- coding: utf-8 -*-

from django import forms

class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length = 100, label = u'Имя')
    last_name = forms.CharField(max_length = 100, label = u'Фамилия')
    email = forms.EmailField()
    address = forms.CharField(max_length = 255, label = u'Адрес')
