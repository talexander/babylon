# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.admin import ModelAdmin, TabularInline, StackedInline
from django import forms
from itertools import chain
from django.utils.html import format_html
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.utils.text import capfirst
from django.core import validators, exceptions
from django.utils.translation import ugettext_lazy as _
from imagekit.models import ImageSpecField
from pilkit.processors import  ResizeToFill, Adjust, SmartResize, ResizeToCover, ResizeToFit, ResizeCanvas
from imagekit.admin import AdminThumbnail
from bitfield import BitField
from bitfield.forms import BitFieldCheckboxSelectMultiple

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session

from django.utils.encoding import smart_str, force_str

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

class BitMaskField(models.Field):
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

class Store(models.Model):
    name = models.CharField(_(u'Наименование'), max_length = 255)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        db_table = 'store'
        verbose_name = _(u'Магазин')
        verbose_name_plural = _(u'Магазины')

class AdminStore(ModelAdmin):
    pass

class Measure(models.Model):
    alias = models.SlugField(_(u'Алиас'), max_length = 40)
    descr = models.CharField(_(u'Описание'), max_length = 100)
    name = models.CharField(_(u'Наименование'), max_length = 100)

    def __unicode__(self):
        return u'%s (%s)' % (self.descr, self.name)

    class Meta:
        db_table = 'measure'
        verbose_name = _(u'Единица измерения')
        verbose_name_plural = _(u'Единицы измерения')

class AdminMeasure(ModelAdmin):
    list_display = ('display_name', 'alias')
    prepopulated_fields = {"alias": ("name",)}

    def display_name(self, obj):
        return "%s (%s)" % (obj.descr, obj.name)
    display_name.short_description = 'Name'



class PropertyGroup(models.Model):
    FLAGS = [(0x0001, u'For admin only'), (0x002, u'Disabled')]
    alias = models.SlugField(_(u'Алиас'), max_length = 40)
    name = models.CharField(_(u'Наименование'), max_length = 255)
    flags = BitMaskField(_(u'Флаги'), masks = FLAGS, blank = True, default = 0)
    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        db_table = 'property_group'
        verbose_name = _(u'Группа характеристик')
        verbose_name_plural = _(u'Группы характеристик')

class AdminPropertyGroup(ModelAdmin):
    list_display = ('name', 'alias')
    prepopulated_fields = {"alias": ("name",)}

class Property(models.Model):
    PROP_ALIAS_LENGTH = 'length_m'
    FLAGS = [(0x0001, u'For admin only'), (0x002, u'Disabled')]
    alias = models.SlugField(_(u'Алиас'), max_length = 40)
    name = models.CharField(_(u'Наименование'), max_length = 255)
    measure = models.ForeignKey('Measure', db_column= 'measure', blank = True, null = True, verbose_name = _(u'Единица измерения'))
    property_group = models.ForeignKey('PropertyGroup', db_column = 'property_group', verbose_name = _(u'Группа характеристик'))
    flags = BitMaskField(_(u'Флаги'), masks = FLAGS, blank = True, default = 0)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        db_table = 'property'
        verbose_name = _(u'Характеристика')
        verbose_name_plural = _(u'Характеристики')

class AdminProperty(ModelAdmin):
    prepopulated_fields = {"alias": ("name",)}
    list_display = ('name', 'alias', 'measure', 'property_group')

class GoodCategory(models.Model):
    FLAGS = [(0x0001, u'For admin only'), (0x002, u'Disabled')]
    name = models.CharField(_(u'Наименование'), max_length = 255)
    alias = models.SlugField(_(u'Алиас'), max_length = 40)
    flags = BitMaskField(_(u'Флаги'), masks = FLAGS, blank = True, default = 0)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        db_table = 'good_category'
        verbose_name = _(u'Категория товара')
        verbose_name_plural = _(u'Категории товаров')

class AdminGoodCategory(ModelAdmin):
    prepopulated_fields = {"alias": ("name",)}
    list_display = ('name', 'alias')

class Colour(models.Model):
    name = models.CharField(_(u'Наименование'), max_length = 255)
    code = models.CharField(_(u'Код'), max_length = 20, unique = True)
    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        db_table = 'colour'
        verbose_name = _(u'Цвет товара')
        verbose_name_plural = _(u'Цвета товаров')

class AdminColour(ModelAdmin):
    pass


class ProductSKU(models.Model):
    good = models.ForeignKey('Good', db_column = 'good', verbose_name = _(u'Товар'))
    unified_colour = models.ForeignKey('Colour', db_column = 'unified_colour', verbose_name = _(u'Унифицированный цвет'))
    vendor_colour = models.CharField(_(u'Цвет производителя'), max_length = 150)
    img = models.ImageField(_(u'Картинка'), upload_to ='goods/', max_length = 255, width_field = 'width', height_field = 'height')
    thumb1 = ImageSpecField([ResizeToFit(190, 275), ], source='img',  options={'quality': 90})
    thumb2 = ImageSpecField([ResizeToFit(600, 600), ], source='img', options={'quality': 90})
    thumb3 = ImageSpecField([ResizeToFit(80, 160), ], source='img', options={'quality': 90})
    width = models.CharField(max_length=7, blank = True, null = True)
    height = models.CharField(max_length=7, blank = True, null = True)
    left_amount = models.PositiveIntegerField(_(u'Остаток'), blank=False, default=0)


    class Meta:
        db_table = 'product_sku'
        verbose_name = _(u'Цвет товара')
        verbose_name_plural = _(u'Цвета товаров')


class Good(models.Model):
    FLAG_IN_STOCK = 0x004
    FLAGS = [(0x0001, u'For admin only'), (0x002, u'Disabled'), (FLAG_IN_STOCK, u'In stock'),]
    #  (0x008, u'Под заказ'), (0x010, u'New'), (0x020, u'Акция')
    alias = models.SlugField(_(u'Алиас'), max_length = 40)
    name = models.CharField(_(u'Наименование'), max_length = 255)
    good_category = models.ForeignKey('GoodCategory', db_column = 'good_category', verbose_name = _(u'Категория'))
    vendor = models.ForeignKey('Vendor', db_column = 'vendor', verbose_name = _(u'Производитель'), blank = True, default = 0)
    consist = models.ForeignKey('GoodConsist', db_column = 'consist', verbose_name = _(u'Состав'), blank = True, default = 0)
    price = models.DecimalField(_(u'Цена'), max_digits = 15, decimal_places = 2)
    descr = models.TextField(_(u'Описание'))
    flags = BitMaskField(_(u'Флаги'), masks = FLAGS, blank = True, default = 0)


    def __unicode__(self):
        return u'%s' % self.name

    def property(self, p_alias):
        try:
            p = Property.objects.get(alias = p_alias)
            pp = GoodProperty.objects.get(good = self.id, prop = p.id)
        except Exception, e:
            return None

        return pp.val

    def xstr(s):
        if s is None:
            return ''
        return str(s)

    def length2weight(self):
        l = self.property('length_m')
        w = self.property('weight_gr')
        r = ''
        if l is None:
            l = '--'
        if w is None:
            w = '--'
        return u'%s м. / %s гр.' % (l, w)

    def img(self):
        img_item = GoodImage.objects.filter(good = self.id).order_by(id).first()
        return img_item

    def thumb(self):
        try:
            item = ProductSKU.objects.get(good = self.id, img__isnull = False).order_by('id')
        except Exception, e:
            try:
                item = GoodImage.objects.get(good = self.id, kind = GoodImage.KIND_DEFAULT)
            except Exception, e:
                item = self.img()
        return item.thumb1

    def thumb2(self):
        try:
            item = GoodImage.objects.get(good = self.id, kind = GoodImage.KIND_DEFAULT)
        except Exception, e:
            item = self.img()
        return item.thumb2

    def thumb3(self):
        try:
            item = GoodImage.objects.get(good = self.id, kind = GoodImage.KIND_DEFAULT)
        except Exception, e:
            item = self.img()
        return item.thumb3

    def in_stock(self):
        return (self.flags & Good.FLAG_IN_STOCK > 0)

    def get_colours(self):
        return ProductSKU.objects.filter(good = self.id)

    def sku(self, id):
        try:
            return ProductSKU.objects.get(pk = id)
        except Exception, e:
            raise e
            return False

    class Meta:
        db_table = 'good'
        verbose_name = _(u'Товар')
        verbose_name_plural = _(u'Товары')

class GoodProperty(models.Model):
    FLAGS = [(0x0001, u'For admin only'), (0x002, u'Disabled')]
    good = models.ForeignKey('Good', db_column = 'good', verbose_name = _(u'Товар'))
    prop = models.ForeignKey('Property', db_column = 'property', verbose_name = _(u'Характеристика'))
    val = models.CharField(_(u'Значение'), max_length = 255, db_column = 'val')
    flags = BitMaskField(_(u'Флаги'), masks = FLAGS, blank = True, default = 0)

    def __unicode__(self):
        return u'%s=%s' % (self.prop.name, self.val)

    class Meta:
        db_table = 'good_property'
        verbose_name = _(u'Характеристика товара')
        verbose_name_plural = _(u'Характеристики товаров')

class GoodImage(models.Model):
    KIND_DEFAULT = 1
    KINDS = ((KIND_DEFAULT, u'Default'),)
    FLAGS = [(0x0001, u'For admin only'), (0x002, u'Disabled')]
    good = models.ForeignKey('Good', db_column = 'good')
    img = models.ImageField(_(u'Картинка'), upload_to ='goods/', max_length = 255, width_field = 'width', height_field = 'height')
    width = models.CharField(max_length=7, blank = True, null = True)
    height = models.CharField(max_length=7, blank = True, null = True)
    thumb1 = ImageSpecField([ResizeToFit(190, 275), ], source='img',  options={'quality': 90})
    thumb2 = ImageSpecField([ResizeToFit(600, 600), ], source='img', options={'quality': 90})
    thumb3 = ImageSpecField([ResizeToFit(80, 160), ], source='img', options={'quality': 90})
    kind = models.IntegerField(_(u'Тип'), blank = True, default = 0, null = False, choices = KINDS)
    flags = BitMaskField(_(u'Флаги'), masks = FLAGS, blank = True, default = 1)

    class Meta:
        db_table = 'good_image'
        verbose_name = _(u'Картинка товара')
        verbose_name_plural = _(u'Картинки товаров')

class AdminGoodProperty(ModelAdmin):
    pass

class AdminGoodPropertyInline(StackedInline):
    model = GoodProperty
    extra = 0
    can_delete = True

class AdminProductSKUInline(StackedInline):
    model = ProductSKU
    readonly_fields = ('admin_thumb1', 'admin_thumb2', 'admin_thumb3')
    exclude = ('width', 'height')
    extra = 0
    can_delete = True
    admin_thumb1 = AdminThumbnail(image_field='thumb1')
    admin_thumb2 = AdminThumbnail(image_field='thumb2')
    admin_thumb3 = AdminThumbnail(image_field='thumb3')



class AdminGoodImageInline(StackedInline):
    readonly_fields = ('admin_thumb1', 'admin_thumb2', 'admin_thumb3')
    model = GoodImage
    exclude = ('width', 'height')
    extra = 0 
    can_delete = True
    admin_thumb1 = AdminThumbnail(image_field='thumb1')
    admin_thumb2 = AdminThumbnail(image_field='thumb2')
    admin_thumb3 = AdminThumbnail(image_field='thumb3')

class AdminGood(ModelAdmin):
    inlines = [AdminGoodImageInline, AdminProductSKUInline, AdminGoodPropertyInline,]
    prepopulated_fields = {"alias": ("name",)}


class Vendor(models.Model):
    FLAGS = [(0x0001, u'For admin only'), (0x002, u'Disabled')]
    alias = models.SlugField(_(u'Алиас'), max_length = 50)
    name = models.CharField(_(u'Наименование'), max_length = 100)
    flags = BitMaskField(_(u'Флаги'), masks = FLAGS, blank = True, default = 0)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        db_table = 'vendor'
        verbose_name = _(u'Производитель')
        verbose_name_plural = _(u'Производители')

class AdminVendor(ModelAdmin):
    prepopulated_fields = {"alias": ("name",)}

class GoodConsist(models.Model):
    alias = models.SlugField(_(u'Алиас'), max_length = 50)
    name = models.CharField(_(u'Наименование'), max_length = 100)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        db_table = 'good_consist'
        verbose_name = _(u'Состав товара')
        verbose_name_plural = _(u'Состав товара')

class AdminGoodConsist(ModelAdmin):
    prepopulated_fields = {"alias": ("name",)}


# class Cart(models.Model):
#     created = models.DateTimeField(_(u'Добавлено'), auto_now_add=True,)
#     user = models.ForeignKey(User, 'user', null=True, blank=True)
#     session = models.ForeignKey(Session, 'session', null=True, blank=True)
#     product = models.ForeignKey(Good, 'product')
#     product_code = models.CharField(_(u'Код товара'), max_length = 150, blank = True, null = False, default='')
#     amount = models.IntegerField(_(u'Количество'), blank = False, null = False)
#
#     def __unicode__(self):
#         return u'cart item: %s' % self.id