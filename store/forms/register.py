# -*- coding: utf-8 -*-

from django import forms

class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length = 100, min_length = 2, label = u'Имя')
    last_name = forms.CharField(max_length = 100, min_length = 2, label = u'Фамилия')
    email = forms.EmailField()
#    address = forms.CharField(max_length = 255, label = u'Адрес', widget = forms.TextInput(attrs = {'class': 'address text_input'}))
    password = forms.CharField(min_length = 5, max_length = 30, label = u'Пароль')
    password_confirm = forms.CharField(min_length = 5, max_length = 30, label = u'Подтверждение пароля')
