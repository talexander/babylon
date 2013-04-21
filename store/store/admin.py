# --*-- coding: utf-8 --*--


from django.contrib import admin
from store import models

admin.site.register(models.Measure, models.AdminMeasure)
admin.site.register(models.Store, models.AdminStore)
admin.site.register(models.PropertyGroup, models.AdminPropertyGroup)
admin.site.register(models.Property, models.AdminProperty)
admin.site.register(models.GoodCategory, models.AdminGoodCategory)
admin.site.register(models.Good, models.AdminGood)
admin.site.register(models.GoodProperty, models.AdminGoodProperty)
