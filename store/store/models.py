# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.admin import ModelAdmin
from django import forms

class BitMaskField(models.Field):
    def __init__(self, masks, *args, **kwargs):
        defaults = {'choices': masks}
        defaults.update(kwargs)
        self.masks = masks
        super(BitMaskField, self).__init__(*args, **defaults)

    def formfield(self, **kwargs):
        defaults = {'widget': forms.CheckboxSelectMultiple}
        defaults.update(kwargs)
        return super(BitMaskField, self).formfield(**defaults)


class Store(models.Model):
    name = models.CharField(max_length = 255)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        db_table = 'store'

class AdminStore(ModelAdmin):
    pass

class Measure(models.Model):
    alias = models.CharField(max_length = 40)
    descr = models.CharField(max_length = 100)
    name = models.CharField(max_length = 100)

    def __unicode__(self):
        return u'%s (%s)' % (self.descr, self.name)

    class Meta:
        db_table = 'measure'

class AdminMeasure(ModelAdmin):
    list_display = ('display_name', 'alias')

    def display_name(self, obj):
        return "%s (%s)" % (obj.descr, obj.name)
    display_name.short_description = 'Name'



class PropertyGroup(models.Model):
    FLAGS = [(u'0', u'--'), (u'1', u'Bit 1'), (u'2', u'Bit 2')]
    alias = models.CharField(max_length = 40)
    name = models.CharField(max_length = 255)
    flags = BitMaskField(masks = FLAGS)
    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        db_table = 'property_group'

class AdminPropertyGroup(ModelAdmin):
    list_display = ('name', 'alias')


class Property(models.Model):
    alias = models.CharField(max_length = 40)
    name = models.CharField(max_length = 255)
    measure = models.ForeignKey('Measure', db_column= 'measure', blank = True, null = True)
    property_group = models.ForeignKey('PropertyGroup', db_column = 'property_group')
    flags = models.BigIntegerField(default = 0)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        db_table = 'property'

class AdminProperty(ModelAdmin):
    list_display = ('name', 'alias', 'measure', 'property_group')

class GoodCategory(models.Model):
    name = models.CharField(max_length = 255)
    flags = models.BigIntegerField(default = 0)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        db_table = 'good_category'

class AdminGoodCategory(ModelAdmin):
    pass

class Good(models.Model):
    alias = models.CharField(max_length = 40)
    name = models.CharField(max_length = 255)
    good_category = models.ForeignKey('GoodCategory', db_column = 'good_category')
    descr = models.TextField()
    flags = models.BigIntegerField(default = 0)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        db_table = 'good'

class AdminGood(ModelAdmin):
    pass

