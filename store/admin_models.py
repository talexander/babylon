# --*-- coding: utf-8 --*--

from store import models

from imagekit.admin import AdminThumbnail
from django.contrib.admin import ModelAdmin, TabularInline, StackedInline
from django.core import urlresolvers
from django.contrib.contenttypes.models import ContentType


class AdminGoodProperty(ModelAdmin):
    pass

class AdminGoodPropertyInline(StackedInline):
    model = models.GoodProperty
    extra = 0
    can_delete = True

class AdminProductSKUInline(StackedInline):
    model = models.ProductSKU
    readonly_fields = ('admin_thumb1', 'admin_thumb2', 'admin_thumb3')
    exclude = ('width', 'height')
    extra = 0
    can_delete = True
    admin_thumb1 = AdminThumbnail(image_field='thumb1')
    admin_thumb2 = AdminThumbnail(image_field='thumb2')
    admin_thumb3 = AdminThumbnail(image_field='thumb3')



class AdminGoodImageInline(StackedInline):
    readonly_fields = ('admin_thumb1', 'admin_thumb2', 'admin_thumb3')
    model = models.GoodImage
    exclude = ('width', 'height')
    extra = 0
    can_delete = True
    admin_thumb1 = AdminThumbnail(image_field='thumb1')
    admin_thumb2 = AdminThumbnail(image_field='thumb2')
    admin_thumb3 = AdminThumbnail(image_field='thumb3')

class AdminGood(ModelAdmin):
    inlines = [AdminProductSKUInline, AdminGoodImageInline,  AdminGoodPropertyInline,]
    prepopulated_fields = {"alias": ("name",)}
    list_filter = ('vendor',)
    list_display = ('id', 'name', 'alias', 'vendor')

class AdminVendor(ModelAdmin):
    prepopulated_fields = {"alias": ("name",)}

class AdminGoodConsist(ModelAdmin):
    prepopulated_fields = {"alias": ("name",)}

class AdminGoodConsistUnified(ModelAdmin):
    prepopulated_fields = {"alias": ("name",)}


class AdminColour(ModelAdmin):
    pass

class AdminGoodCategory(ModelAdmin):
    prepopulated_fields = {"alias": ("name",)}
    list_display = ('name', 'alias')

class AdminProperty(ModelAdmin):
    prepopulated_fields = {"alias": ("name",)}
    list_display = ('name', 'alias', 'measure', 'property_group')

class AdminPropertyGroup(ModelAdmin):
    list_display = ('name', 'alias')
    prepopulated_fields = {"alias": ("name",)}

class AdminMeasure(ModelAdmin):
    list_display = ('display_name', 'alias')
    prepopulated_fields = {"alias": ("name",)}

    def display_name(self, obj):
        return "%s (%s)" % (obj.descr, obj.name)
    display_name.short_description = 'Name'

class AdminOrderProductInline(TabularInline):
    model = models.OrderProduct
    list_display = ('id', 'product', 'sku', 'amount', 'price')
    readonly_fields = ('product_admin_url',)

    def product_admin_url(self, obj):
        content_type = ContentType.objects.get_for_model(obj.product.__class__)
        url = urlresolvers.reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(obj.product.id,))
        return u'<a href="%s" target="_blank">[ %s ]</a>' % (url,  obj.product.__unicode__())

    product_admin_url.short_description = u'URL'
    product_admin_url.allow_tags = True


class AdminOrder(ModelAdmin):
    list_display = ('id', 'created', 'email', 'phone', 'status', 'ip', 'total')
    list_editable = ('status',)
    ordering = ('-created',)
    inlines = [AdminOrderProductInline]
    readonly_fields = ('total',)

    def total(self, obj):
        return u'%s руб. ' % obj.getTotalSum()
    total.short_description = u'ИТОГО'




class AdminStore(ModelAdmin):
    pass
