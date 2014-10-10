# --*-- coding: utf-8 --*--

from django.db import models as djModels
from django.utils.text import capfirst
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text
from django.utils.html import format_html
from itertools import chain
from django import forms
from django.core import validators, exceptions
from django.contrib import admin

def to_long(val):
    try:
        return long(float(val))
    except Exception, e:
        return 0

def list2long(l):
    if type(l) != list:
        raise ValueError('Value is not list')
    result = 0
    for v in l:
        result |= to_long(v)
    return result

class BitMaskMultiCheckbox(forms.SelectMultiple):
    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        output = ['<ul>']
        long_val = to_long(value)

        for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):
            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if to_long(option_value) == 0:
                continue
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
                label_for = format_html(' for="{0}"', final_attrs['id'])
            else:
                label_for = ''

            cb = forms.CheckboxInput(final_attrs, check_test=lambda value: bool(to_long(value) & long_val))
            option_value = force_text(option_value)
            rendered_cb = cb.render(name, option_value)
            option_label = force_text(option_label)
            output.append(format_html('<li><label{0}>{1} {2}</label></li>',
                                      label_for, rendered_cb, option_label))
        output.append('</ul>')
        return mark_safe('\n'.join(output))

    def _has_changed(self, initial, data):
        if data is None:
            data_value = ''
        else:
            data_value = data
        if initial is None:
            initial_value = ''
        else:
            initial_value = initial
        if force_text(initial_value)  != force_text(data_value):
            return True
        return False


class CustomTypedMultipleChoiceField(forms.TypedMultipleChoiceField):
    def clean(self, value):
        value = self.to_python(value)
        self.validate(value)
        self.run_validators(value)
        return list2long(value)

class BitMaskField(djModels.Field):
    def __init__(self, verbose_name=None, masks= [], *args, **kwargs):
        defaults = {'choices': masks }
        defaults.update(kwargs)
        self.masks = masks
        super(BitMaskField, self).__init__(verbose_name, *args, **defaults)

    def formfield(self, form_class=forms.CharField, **kwargs):
        """
        Returns a django.forms.Field instance for this database Field.
        """
        def co(val):
            return to_long(val)

        defaults = {'required': not self.blank,
                    'label': capfirst(self.verbose_name),
                    'help_text': self.help_text,
                    'widget': BitMaskMultiCheckbox,
                    'coerce': co
                    }
        if self.has_default():
            if callable(self.default):
                defaults['initial'] = self.default
                defaults['show_hidden_initial'] = True
            else:
                defaults['initial'] = self.get_default()
        if self.choices:
            # Fields with choices get special treatment.
            include_blank = (self.blank or
                             not (self.has_default() or 'initial' in kwargs))
            defaults['choices'] = self.get_choices(include_blank=include_blank)
            if self.null:
                defaults['empty_value'] = None
            form_class = CustomTypedMultipleChoiceField
            for k in list(kwargs):
                if k not in ('empty_value', 'choices', 'required',
                             'label', 'initial', 'help_text',
                             'error_messages', 'show_hidden_initial', 'verbose_name'):
                    del kwargs[k]
        defaults.update(kwargs)
        return form_class(**defaults)

    def validate(self, value, model_instance):
        if not self.editable:
            # Skip validation for non-editable fields.
            return
        if value is None and not self.null:
            raise exceptions.ValidationError(self.error_messages['null']);
        if not self.blank and value  in validators.EMPTY_VALUES:
            raise exceptions.ValidationError(self.error_messages['blank'])
