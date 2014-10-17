# -*- coding: utf-8 -*-

from django.db import models
from django.core import exceptions
from django.utils.translation import ugettext_lazy as _
from imagekit.models import ImageSpecField
from pilkit.processors import  ResizeToFill, Adjust, SmartResize, ResizeToCover, ResizeToFit, ResizeCanvas
from store.bitmask import BitMaskField


from django.contrib.auth.models import User
from django.contrib.sessions.models import Session

from django.utils.encoding import smart_str, force_str

import logging
logger = logging.getLogger(__name__)

class Store(models.Model):
    name = models.CharField(_(u'Наименование'), max_length = 255)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        db_table = 'store'
        verbose_name = _(u'Магазин')
        verbose_name_plural = _(u'Магазины')

class Measure(models.Model):
    name = models.CharField(_(u'Наименование'), max_length = 100)
    alias = models.SlugField(_(u'Алиас'), max_length = 40)
    descr = models.CharField(_(u'Описание'), max_length = 100)

    def __unicode__(self):
        return u'%s (%s)' % (self.descr, self.name)

    class Meta:
        db_table = 'measure'
        verbose_name = _(u'Единица измерения')
        verbose_name_plural = _(u'Единицы измерения')


class PropertyGroup(models.Model):
    FLAGS = [(0x0001, u'For admin only'), (0x002, u'Disabled')]
    name = models.CharField(_(u'Наименование'), max_length = 255)
    alias = models.SlugField(_(u'Алиас'), max_length = 40)
    flags = BitMaskField(_(u'Флаги'), masks = FLAGS, blank = True, default = 0)
    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        db_table = 'property_group'
        verbose_name = _(u'Группа характеристик')
        verbose_name_plural = _(u'Группы характеристик')

class Property(models.Model):
    PROP_ALIAS_LENGTH = 'length_m'
    FLAGS = [(0x0001, u'For admin only'), (0x002, u'Disabled')]
    name = models.CharField(_(u'Наименование'), max_length = 255)
    alias = models.SlugField(_(u'Алиас'), max_length = 40)
    measure = models.ForeignKey('Measure', db_column= 'measure', blank = True, null = True, verbose_name = _(u'Единица измерения'))
    property_group = models.ForeignKey('PropertyGroup', db_column = 'property_group', verbose_name = _(u'Группа характеристик'))
    flags = BitMaskField(_(u'Флаги'), masks = FLAGS, blank = True, default = 0)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        db_table = 'property'
        verbose_name = _(u'Характеристика')
        verbose_name_plural = _(u'Характеристики')


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

class Colour(models.Model):
    name = models.CharField(_(u'Наименование'), max_length = 255)
    code = models.CharField(_(u'Код'), max_length = 20, unique = True)
    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        db_table = 'colour'
        verbose_name = _(u'Цвет товара')
        verbose_name_plural = _(u'Цвета товаров')



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
        verbose_name = _(u'Артикул')
        verbose_name_plural = _(u'Артикулы')

    def __unicode__(self):
        return u'ID: %d, артикул: %s' % (self.id, self.vendor_colour)


class Good(models.Model):
    FLAG_IN_STOCK = 0x004
    FLAGS = [(0x0001, u'For admin only'), (0x002, u'Disabled'), (FLAG_IN_STOCK, u'In stock'),]
    #  (0x008, u'Под заказ'), (0x010, u'New'), (0x020, u'Акция')
    name = models.CharField(_(u'Наименование'), max_length = 255)
    alias = models.SlugField(_(u'Алиас'), max_length = 40)
    good_category = models.ForeignKey('GoodCategory', db_column = 'good_category', verbose_name = _(u'Категория'))
    vendor = models.ForeignKey('Vendor', db_column = 'vendor', verbose_name = _(u'Производитель'), blank = True, default = 0, null=True)
    consist = models.ForeignKey('GoodConsist', db_column = 'consist', verbose_name = _(u'Состав (произв.)'), blank = True, default=0, null=True)
    consist_unified = models.ForeignKey('GoodConsistUnified', db_column = 'consist_unified', verbose_name = _(u'Состав (униф.)'), blank = True, default=0, null=True)
    left_amount = models.PositiveIntegerField(_(u'Остаток'), blank=True, default=0, null=True)
    price = models.DecimalField(_(u'Цена'), max_digits = 15, decimal_places = 2)
    descr = models.TextField(_(u'Описание'), default='', null=True, blank=True)
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

    def thumbnail(self, type):
        try:
            item = self.get_sku().filter(img__isnull = False).order_by('id')[0]
        except IndexError, e:
            try:
                item = GoodImage.objects.get(good = self.id, kind = GoodImage.KIND_DEFAULT)
            except exceptions.ObjectDoesNotExist, e:
                item = self.img()
                if (not item):
                    logger.debug('item: %d, images not found' % self.id)
                    return False


        r = getattr(item, type)
        return r

    def thumb(self):
        return self.thumbnail('thumb1')

    def thumb2(self):
        return self.thumbnail('thumb2')

    def thumb3(self):
        return self.thumbnail('thumb3')

    def in_stock(self):
        return (self.flags & Good.FLAG_IN_STOCK > 0)

    def get_sku(self):
        return ProductSKU.objects.filter(good = self.id).exclude(vendor_colour__isnull=True).exclude(vendor_colour__exact='')

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



class Vendor(models.Model):
    FLAGS = [(0x0001, u'For admin only'), (0x002, u'Disabled')]
    name = models.CharField(_(u'Наименование'), max_length = 100)
    alias = models.SlugField(_(u'Алиас'), max_length = 50)
    flags = BitMaskField(_(u'Флаги'), masks = FLAGS, blank = True, default = 0)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        db_table = 'vendor'
        verbose_name = _(u'Производитель')
        verbose_name_plural = _(u'Производители')


class GoodConsist(models.Model):
    name = models.CharField(_(u'Наименование'), max_length = 100)
    alias = models.SlugField(_(u'Алиас'), max_length = 50)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        db_table = 'good_consist'
        verbose_name = _(u'Состав товара')
        verbose_name_plural = _(u'Состав товара')

class GoodConsistUnified(models.Model):
    name = models.CharField(_(u'Наименование'), max_length = 100)
    alias = models.SlugField(_(u'Алиас'), max_length = 50)
    good_category = models.ForeignKey('GoodCategory', db_column = 'good_category', verbose_name = _(u'Категория'))

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        db_table = 'good_consist_unified'
        verbose_name = _(u'Состав товара (унифицированный)')
        verbose_name_plural = _(u'Состав товара (унифицированный)')



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


class StandardModel(models.Model):
    field_one = models.CharField(max_length=255)
    field_two = models.CharField(max_length=255)
    field_three = models.CharField(max_length=255)

    class Meta:
        db_table = 'smodel1'


class Order(models.Model):
    DELIVERY_CHOICES = (
        (0, u'Выберите значение'),
        (1, u'Почта России'),
        (2, u'Транспортная компания'),
        (3, u'Самовывоз'),
        (4, u'По договоренности'),
    )
    PAYMENT_CHOICES = (
        (0, u'Выберите значение'),
        (1, u'Наличными при получении'),
        (2, u'Банковский перевод'),
    )

    STATUS_NEW = 1
    STATUS_ACCEPTED = 2
    STATUS_PAID = 3
    STATUS_SEND = 4
    STATUS_CANCELED = 5

    STATUS_CHOICES = (
        (STATUS_NEW, u'Новый'),
        (STATUS_ACCEPTED, u'Принят'),
        (STATUS_PAID, u'Оплачен'),
        (STATUS_SEND, u'Отправлен'),
        (STATUS_CANCELED, u'Отменен'),
    )

    created = models.DateTimeField(_(u'Дата создания'), auto_now = True)
    status = models.PositiveSmallIntegerField(_(u'Статус'), choices=STATUS_CHOICES, default=STATUS_NEW, blank=True)
    fname = models.CharField(_(u'Имя'), max_length=100)
    phone = models.CharField(_(u'Телефон'), max_length=15)
    email = models.EmailField(_(u'E-mail'), max_length=100)
    delivery = models.PositiveSmallIntegerField(_(u'Вариант доставки'), choices = DELIVERY_CHOICES)
    payment = models.PositiveSmallIntegerField(_(u'Оплата'), choices = PAYMENT_CHOICES)
    comment = models.TextField(_(u'Комментарий'), blank = True, default = '')
    ip = models.GenericIPAddressField(_(u'IP'))


    def code(self):
        return '%s%s%s%s%s' % ( self.created.strftime("%a")[0], self.created.strftime("%m"), self.created.strftime("%d"), self.created.strftime("%b")[0], self.id)

    def deliveryMethod(self):
        for i, s in Order.DELIVERY_CHOICES:
            if i == self.delivery:
                return s

        return '--'

    def paymentMethod(self):
        for i, s in Order.PAYMENT_CHOICES:
            if i == self.payment:
                return s
        return '--'

    def products(self):
        return OrderProduct.objects.filter(order = self).prefetch_related('sku', 'product')

    def getTotalSum(self):
        return OrderProduct.objects.filter(order = self).aggregate(total = models.Sum('amount', field = 'price*amount'))['total']

    def __unicode__(self):
        return u'Заказ #%d от %s [%s]' % (self.id, self.created, self.statusVerbose())

    class Meta:
        db_table = 'order'
        verbose_name = _(u'Заказ')
        verbose_name_plural = _(u'Заказы')

    def statusVerbose(self):
        for (s, name) in self.STATUS_CHOICES:
            if s == self.status:
                return name
        return 'undeclarated "%s"' % self.status


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, db_column='order')
    product = models.ForeignKey(Good, db_column='product')
    sku = models.ForeignKey(ProductSKU, blank=True, null=True, db_column='sku')
    amount = models.PositiveIntegerField(_(u'Кол-во'))
    price = models.DecimalField(_(u'Цена'), max_digits = 15, decimal_places = 2)

    def __unicode__(self):
        return u'Позиция заказа #%d, Товар: %s #%d, sku: %s' % (self.order.id, self.product.name, self.product.id, self.sku)

    class Meta:
        db_table = 'order_product'
        verbose_name = _(u'Позиции заказа')
        verbose_name_plural = _(u'Позиции заказа')

    def summ(self):
        return self.amount*self.price

