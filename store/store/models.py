# -*- coding: latin-1 -*-

from django.db import models
from django.contrib.admin import ModelAdmin

# Create your models here.

class Store(models.Model):
    name = models.CharField(max_length = 255)

    class Meta:
        db_table = 'store'

class AdminStore(ModelAdmin):
    pass

class Measure(models.Model):
    alias = models.CharField(max_length = 40)
    descr = models.CharField(max_length = 100)
    name = models.CharField(max_length = 100)

    class Meta:
        db_table = 'measure'

class AdminMeasure(ModelAdmin):
    list_display = ('display_name', 'alias')
    def display_name(self, obj):
        return "%s (%s)" % (obj.descr, obj.name)
    display_name.short_description = 'Name'



class PropertyGroup(models.Model):
    alias = models.CharField(max_length = 40)
    name = models.CharField(max_length = 255)
    flags = models.BigIntegerField(default = 0)

    class Meta:
        db_table = 'property_group'

class AdminPropertyGroup(ModelAdmin):
    pass


class Property(models.Model):
    alias = models.CharField(max_length = 40)
    name = models.CharField(max_length = 255)
    measure = models.ForeignKey('Measure', db_column= 'measure') # @TODO: прописать название поля в БД
    propery_group = models.ForeignKey('PropertyGroup', db_column = 'property_group') # @TODO: прописать название поля в БД
    flags = models.BigIntegerField(default = 0)

    class Meta:
        db_table = 'property'

class AdminProperty(ModelAdmin):
    pass

class GoodCategory(models.Model):
    name = models.CharField(max_length = 255)
    flags = models.BigIntegerField(default = 0)

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

    class Meta:
        db_table = 'good'

class AdminGood(ModelAdmin):
    pass

