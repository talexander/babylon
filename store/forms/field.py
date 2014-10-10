from store.widgets import ChainedSelect, DependentControl
from django.forms import Field
from django.forms import widgets

class DependentField(Field):
    def __init__(self, parent_field, datasource, *args, **kwargs):
        self.parent_field = parent_field
        self.data_source = datasource
        defaults = {
            'widget': DependentControl(parent_field = parent_field, datasource= datasource),
        }
        defaults.update(kwargs)

        super(DependentField, self).__init__(*args, **defaults)