#!/usr/bin/env python
# encoding: UTF-8

from django.db import models
from django.db.models import *
from django.core.validators import MaxLengthValidator
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from voodoo.mainsite.basket.models import Cart
from django.contrib.contenttypes.models import ContentType


class Menu(models.Model):
    name = CharField(max_length=120)
    title = CharField(max_length=120)
    enabled = BooleanField()

    def getAllElements(self):
        return Menu.objects.all()

    def getActiveElements(self):
        return Menu.objects.filter(enabled=True)

    def fillTable(self):
        # TODO initial data
        # Menu(name='name', title='title', enabled=True)
        return None

    def __unicode__(self):
        return self.name
    
# TODO list of permissions
#    class Meta:
#        permissions = (
#            ("view_task", "Can see available tasks"),
#            ("change_task_status", "Can change the status of tasks"),
#            ("close_task", "Can remove a task by setting its status as closed"),
#        )
#user.has_perm('app.view_task')

CAR_BODIES = (
            (u'Седан', u'Седан'),
            (u'Хетчбек', u'Хетчбек'),
            (u'Универсал', u'Универсал'),
            (u'Джип', u'Джип'),
            (u'Минивен', u'Минивен'),
            (u'Купе', u'Купе'),
            (u'Автобус', u'Автобус'),
            (u'Грузовик', u'Грузовик'),
)

CAR_GEARBOXES = (
            (u'Ручная', u'Ручная'),
            (u'Автомат', u'Автомат'),
            (u'Вариатор', u'Вариатор'),
            (u'Робот', u'Робот'),
)

ORDER_STATUS = (
            (u'Принят (черный)', u'Принят (черный)'),
            (u'Обработан (зеленый)', u'Обработан (зеленый)'),
            (u'Закрыт (красный)', u'Закрыт (красный)'),
)


class Order(models.Model):
    # Создание заказа
    required_css_class = 'required'
    # Информация о заказчике
    user = models.ForeignKey(User, unique=False, blank=True, null=True)
    client_name = CharField(verbose_name='Ф.И.О. или название клиента', max_length=120)
    client_phone = CharField(verbose_name='Контактные телефоны', max_length=120)
    client_code = CharField(verbose_name='Код клиента в ATSP', max_length=120, blank=True)
    client_additional_information = CharField(verbose_name='Дополнительная информация', max_length=500, blank=True)
    email = CharField(max_length=50, verbose_name='Email', blank=True, null=True)
    delivery_adress = models.CharField(max_length=50, verbose_name='Адресс доставки', blank=True, null=True)
    # Информация о авто
    car_brand = CharField(verbose_name='Марка автомобиля', max_length=120, blank=True)
    car_vin = CharField(verbose_name='VIN', validators=[MinLengthValidator(17), MaxLengthValidator(17)], max_length=17, blank=True)
    car_model = CharField(verbose_name='Модель/Серия', max_length=120, blank=True)
    car_engine = CharField(verbose_name='Двигатель', max_length=120, blank=True)
    car_year = CharField(verbose_name='Год выпуска', max_length=120, blank=True)
    car_engine_size = CharField(verbose_name='Объем двигателя', max_length=120, blank=True)
    car_body = CharField(verbose_name='Кузов', choices=CAR_BODIES, max_length=120, default=0, blank=True)
    car_gearbox = CharField(verbose_name='КПП', choices=CAR_GEARBOXES, max_length=120, default=0,  blank=True)
    car_additional_information = CharField(verbose_name='Дополнительная информация по авто', max_length=500, blank=True)
    # Информация о заказе и запчастям
    order_info = CharField(verbose_name='Полная формулировка заказа', max_length=500, blank=True)
    order_additional_information = CharField(verbose_name='Дополнительная информация по заказу', max_length=500, blank=True)
    # TODO use OrderStatus and ItemStatus
    order_status = CharField(verbose_name='Статус выполнения заказа', choices=ORDER_STATUS, max_length=120, default=0)
    creation_date = DateTimeField(verbose_name='Дата создания', max_length=120, auto_now_add=True)
#    order_total_price1 = DecimalField(verbose_name='Всего Цена 1', max_length=120, max_digits=20, decimal_places=1, blank=True)
#    order_total_price2 = DecimalField(verbose_name='Всего Цена 2', max_length=120, max_digits=20, decimal_places=1, blank=True)

    def __unicode__(self):
        return str(self.id)


class Supplier(models.Model):
    name = CharField(verbose_name='Название', max_length=120)
    delivery_time = CharField(verbose_name='Срок поставки', max_length=120)

    def getProducts(self):
        print None

    def isProductExists(self):
        print None

    #TODO Extract this methods into ProductManager class?
    def getAllSuppliersByProduct(self):
        print None

    def __unicode__(self):
        return self.name


class Product(models.Model):
    code = CharField(verbose_name='Номер', max_length=120)
    brand = CharField(verbose_name='Бдэнд', max_length=120)
    description = CharField(verbose_name='Описание', max_length=120, blank=True)
    count = CharField(verbose_name='Количество', max_length=120, blank=True)
    price = DecimalField(verbose_name='Цена', max_length=120, max_digits=20, decimal_places=1)
    supplier = models.ForeignKey(Supplier)
    date_of_import = DateTimeField(verbose_name='Дата импорта', max_length=120, auto_now_add=True)

    def __unicode__(self):
        return self.code


class ItemManager(models.Manager):
    def get(self, *args, **kwargs):
        if 'product' in kwargs:
            kwargs['content_type'] = ContentType.objects.get_for_model(type(kwargs['product']))
            kwargs['object_id'] = kwargs['product'].pk
            del(kwargs['product'])
        return super(ItemManager, self).get(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, blank=True, null=True)
    code = CharField(verbose_name='Номер', max_length=120)
    brand = CharField(verbose_name='Бдэнд', max_length=120)
    comment = CharField(verbose_name='Комментарий', max_length=120, blank=True)
    price_1 = DecimalField(verbose_name='Цена1', max_length=120, max_digits=20, decimal_places=1)
    price_2 = DecimalField(verbose_name='Цена2', max_length=120, max_digits=20, decimal_places=1)
    currency = CharField(verbose_name='Тип валюты', max_length=120)
    count = PositiveIntegerField(verbose_name='Количество', max_length=120)
    supplier = CharField(verbose_name='Поставщик', max_length=120)
    delivery_time = CharField(verbose_name='Срок поставки', max_length=120)
    status = CharField(verbose_name='Статус', max_length=120)
    cart = models.ForeignKey(Cart, verbose_name='Корзина', blank=True, null=True)
    # quantity = models.PositiveIntegerField(verbose_name=_('quantity'))
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    objects = ItemManager()

    def __unicode__(self):
        return self.code

    def total_price(self):
        return self.count * self.price_2
    total_price = property(total_price)

    # product
    def get_product(self):
        return self.content_type.get_object_for_this_type(id=self.object_id)

    def set_product(self, product):
        self.content_type = ContentType.objects.get_for_model(type(product))
        self.object_id = product.pk

    product = property(get_product, set_product)


class OrderStatus(models.Model):
    status = CharField(verbose_name='Статус выполнения заказа', max_length=120)
    color = CharField(verbose_name='Цвет', max_length=120)


class ItemStatus(models.Model):
    status = CharField(verbose_name='Статус', max_length=120)
    color = CharField(verbose_name='Цвет', max_length=120)
    
    def __unicode__(self):
        return self.status


class Currency(models.Model):
    name = CharField(verbose_name='Название', max_length=120)
    code = CharField(verbose_name='Код', max_length=120)
    ratio = DecimalField(verbose_name='Коэффициент', max_length=120, max_digits=20, decimal_places=1)
    
    def __unicode__(self):
        return self.code

class DiscountGroup(models.Model):
    name = CharField(verbose_name='Название', max_length=120)
    discount = DecimalField(verbose_name='Скидка в %', max_length=120, max_digits=20, decimal_places=1)
    
    def __unicode__(self):
        return self.name