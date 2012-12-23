#!/usr/bin/env python
# encoding: UTF-8

from django.db import models
from django.db.models import *
from django.core.validators import MaxLengthValidator
from django.core.validators import MinLengthValidator

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
    client_name = CharField(verbose_name='Ф.И.О. или название клиента', max_length=120)
    client_phone = CharField(verbose_name='Контактные телефоны', max_length=120)
    client_code = CharField(verbose_name='Код клиента в ATSP', max_length=120, blank=True)
    client_additional_information = CharField(verbose_name='Дополнительная информация', max_length=500, blank=True)
    # Информация о авто
    car_brand = CharField(verbose_name='Марка автомобиля', max_length=120, blank=True)
    car_vin = CharField(verbose_name='VIN',validators=[MinLengthValidator(17), MaxLengthValidator(17)], max_length=17, blank=True)
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
    order_total_price1 = DecimalField(verbose_name='Всего Цена 1', max_length=120, max_digits=20, decimal_places=1)
    order_total_price2 = DecimalField(verbose_name='Всего Цена 2', max_length=120, max_digits=20, decimal_places=1)

    def __unicode__(self):
        return self.client_name
   
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
    price = CharField(verbose_name='Цена', max_length=120)
    supplier = ManyToManyField(Supplier)
    date_of_import = DateTimeField(verbose_name='Дата импорта', max_length=120, auto_now_add=True)
    
    def __unicode__(self):
        return self.code
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order)
    code = CharField(verbose_name='Номер', max_length=120)
    brand = CharField(verbose_name='Бдэнд', max_length=120)
    comment = CharField(verbose_name='Комментарий', max_length=120, blank=True)
    price_1 = DecimalField(verbose_name='Цена1', max_length=120, max_digits=20, decimal_places=1)
    price_2 = DecimalField(verbose_name='Цена2', max_length=120, max_digits=20, decimal_places=1)
    currency = CharField(verbose_name='Тип валюты', max_length=120)
    count = CharField(verbose_name='Количество', max_length=120)
    supplier = CharField(verbose_name='Поставщик', max_length=120)
    delivery_time = CharField(verbose_name='Срок поставки', max_length=120)
    status = CharField(verbose_name='Статус', max_length=120)
 
class OrderStatus(models.Model):
    status = CharField(verbose_name='Статус выполнения заказа', max_length=120)
    color = CharField(verbose_name='Цвет', max_length=120)

class ItemStatus(models.Model):
    status = CharField(verbose_name='Статус', max_length=120)
    color = CharField(verbose_name='Цвет', max_length=120)
    
class Currency(models.Model):
    name = CharField(verbose_name='Название', max_length=120)
    code = CharField(verbose_name='Код', max_length=120)
    ratio = DecimalField(verbose_name='Коэффициент', max_length=120, max_digits=20, decimal_places=1)