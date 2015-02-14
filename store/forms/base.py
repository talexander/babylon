# --*-- coding: utf-8 --*--

from store.forms.field import DependentField
from django import forms
from django.forms import widgets
from store import models

class OrderForm(forms.Form):

    fname = forms.CharField(label = u'Имя', min_length=3, widget=widgets.TextInput(attrs={'class':'fname form-control'}))
    phone = forms.CharField(label = u'Телефон', min_length=6, widget=widgets.TextInput(attrs={'class':'phone form-control'}))
    email = forms.EmailField(label = u'E-mail', widget=widgets.EmailInput(attrs={'class':'delivery form-control'}))
    delivery = forms.ChoiceField(label = u'Вариант доставки', choices = models.Order.DELIVERY_CHOICES, initial=0, widget=widgets.Select(attrs={'class':'delivery form-control'}))
    payment = forms.ChoiceField(label = u'Оплата', choices = models.Order.PAYMENT_CHOICES, initial=0, widget=widgets.Select(attrs={'class':'pay_info form-control'}))
    comment = forms.CharField(label= u'Комментарий', widget=widgets.Textarea(attrs={'class':'comment form-control', 'rows': 5}), required = False)

    def as_dtdd(self):
        "Returns this form rendered as HTML <li>s -- excluding the <ul></ul>."
        return self._html_output(
            normal_row = '<dt%(html_class_attr)s>%(label)s %(help_text)s</dt><dd>%(field)s %(errors)s</dd>',
            error_row = '<dt>%s</dt><dd></dd>',
            row_ender = '</dd>',
            help_text_html = ' <span class="helptext">%s</span>',
            errors_on_separate_row = False)



