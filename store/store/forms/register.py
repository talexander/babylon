# -*- coding: utf-8 -*-

from django import forms

class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length = 100, label = u'Имя', widget = forms.TextInput(attrs = { 'class': 'first_name text_input', 'data-required': 1 }))
    last_name = forms.CharField(max_length = 100, label = u'Фамилия', widget = forms.TextInput(attrs = {'class': 'last_name text_input'}))
    email = forms.EmailField(widget = forms.TextInput(attrs = {'class': 'email text_input'}))
    address = forms.CharField(max_length = 255, label = u'Адрес', widget = forms.TextInput(attrs = {'class': 'address text_input'}))
    password = forms.CharField(min_length = 5, max_length = 30, label = u'Пароль', widget = forms.TextInput(attrs = {'class': 'password  text_input'}))
    password_confirm = forms.CharField(min_length = 5, max_length = 30, label = u'Подтверждение пароля', widget = forms.TextInput(attrs = {'class': 'password_confirm text_input'}))
