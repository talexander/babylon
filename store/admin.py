# --*-- coding: utf-8 --*--


from django.contrib import admin
from store import models
from store import admin_models


admin.site.register(models.Measure, admin_models.AdminMeasure)
admin.site.register(models.Store, admin_models.AdminStore)
admin.site.register(models.PropertyGroup, admin_models.AdminPropertyGroup)
admin.site.register(models.Property, admin_models.AdminProperty)
admin.site.register(models.GoodCategory, admin_models.AdminGoodCategory)
admin.site.register(models.Good, admin_models.AdminGood)
admin.site.register(models.GoodProperty, admin_models.AdminGoodProperty)
admin.site.register(models.Vendor, admin_models.AdminVendor)
admin.site.register(models.GoodConsist, admin_models.AdminGoodConsist)
admin.site.register(models.GoodConsistUnified, admin_models.AdminGoodConsistUnified)
admin.site.register(models.Colour, admin_models.AdminColour)
admin.site.register(models.Order, admin_models.AdminOrder)


