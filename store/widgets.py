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
        attrs['class'] = 'dependent-field'
        attrs['data-parent-field'] = parent_field
        attrs['data-source'] = datasource
        super(DependentControl, self).__init__(attrs)
    class Media:
        js = ['js/dependent-control.js']
