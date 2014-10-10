from django.forms.widgets import Select, HiddenInput
from django.contrib.admin.templatetags.admin_static import static
from django.utils.safestring import mark_safe
from django.utils import html
import logging

logger = logging.getLogger(__name__)

class DependentControl(HiddenInput):
    def __init__(self, attrs=None, parent_field=None, datasource=None, *args, **kwargs):
        if attrs is None:
            attrs = {}
        attrs['class'] = 'dependent-control'
        attrs['data-parent-field'] = parent_field
        attrs['data-source'] = datasource
        super(DependentControl, self).__init__(attrs)
    class Media:
        js = ['js/dependent-control.js']


class ChainedSelect(Select):
    """
    A ChoiceField widget where the options for the select are dependant on the value of the parent select field.
    When the parent field is changed an ajax call is made to determine the options.

    Form must inherit from ChainedChoicesForm which loads the options when there is already an instance.

    class StandardModelForm(ChainedChoicesForm):
        field_one = forms.ChoiceField(choices=(('', '------------'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), ))
        field_two = ChainedChoiceField(parent_field='field_one', ajax_url='/chainedselectchoices')
        field_three = ChainedChoiceField(parent_field='field_two', ajax_url='/chainedselectchoices')

    """
    def __init__(self, parent_field=None, ajax_url=None, *args, **kwargs):
        self.parent_field = parent_field
        self.ajax_url = ajax_url
        super(ChainedSelect, self).__init__(*args, **kwargs)

    class Media:
        js = ['admin/js/jquery.min.js', 'admin/js/jquery.init.js', 'js/chained-select.js']

    def render(self, name, value, attrs={}, choices=()):
        attrs['ajax_url'] = self.ajax_url

        if(not attrs.get('class')):
            attrs['class'] = ''
        attrs['class'] = '%s %s' % (attrs['class'], 'chained-parent-field')
        output = super(ChainedSelect, self).render(name, value, attrs=attrs, choices=choices)
        logger.debug(html.escape(mark_safe(output)))

        return mark_safe(output)
