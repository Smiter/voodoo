#!/usr/bin/env python
# encoding: UTF-8

from django.db import models
from django.db.models import *
from django.core.validators import MaxLengthValidator
from django.core.validators import MinLengthValidator

# Create your models here.

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
            ('Седан', 'Седан'),
            ('Хетчбек', 'Хетчбек'),
            ('Универсал', 'Универсал'),
            ('Джип', 'Джип'),
            ('Минивен', 'Минивен'),
            ('Купе', 'Купе'),
            ('Автобус', 'Автобус'),
            ('Грузовик', 'Грузовик'),
)

CAR_GEARBOXES = (
            ('Ручная', 'Ручная'),
            ('Автомат', 'Автомат'),
            ('Вариатор', 'Вариатор'),
            ('Робот', 'Робот'),
)

class Order(models.Model):
    # Создание заказа
    
    # Информация о заказчике
    client_name = CharField(verbose_name='Ф.И.О. или название клиента', max_length=120)
    client_phone = CharField(verbose_name='Контактные телефоны', max_length=120)
    client_code = CharField(verbose_name='Код клиента в ATSP', max_length=120, blank=True)
    client_additional_information = CharField(verbose_name='Дополнительная информация', max_length=500, blank=True)
    required_css_class = 'required'
    # Информация о авто
    car_brand = CharField(verbose_name='Марка автомобиля', max_length=120, blank=True)
    car_vin = CharField(verbose_name='VIN',validators=[MinLengthValidator(17), MaxLengthValidator(17)], max_length=17, blank=True)
    car_model = CharField(verbose_name='Модель/Серия', max_length=120, blank=True)
    car_engine = CharField(verbose_name='Двигатель', max_length=120, blank=True)
    car_year = CharField(verbose_name='Год выпуска', max_length=120, blank=True)
    car_engine_size = CharField(verbose_name='Объем двигателя', max_length=120, blank=True)
    car_body = CharField(verbose_name='Кузов', choices=CAR_BODIES, max_length=120, blank=True)
    car_gearbox = CharField(verbose_name='КПП', choices=CAR_GEARBOXES, max_length=120, blank=True)
    car_additional_information = CharField(verbose_name='Дополнительная информация', max_length=500, blank=True)
    # Информация о заказе и запчастям
    order_info = CharField(verbose_name='Полная формулировка заказа', max_length=500, blank=True)
    
    # Список запчастей заказа (таблица на темплейте)
    
    def __unicode__(self):
        return self.client_name
   
class Supplier(models.Model):
    name = CharField(verbose_name='Название', max_length=120)
    delivery_time = CharField(verbose_name='Срок поставки', max_length=120)
    
    def __unicode__(self):
        return self.name
    
class Product(models.Model):
    code = CharField(verbose_name='Номер', max_length=120)
    brand = CharField(verbose_name='Бдэнд', max_length=120)
    description = CharField(verbose_name='Описание', max_length=120, blank=True)
    count = CharField(verbose_name='Количество', max_length=120, blank=True)
    price = CharField(verbose_name='Цена', max_length=120)
    supplier = ManyToManyField(Supplier)
    date_of_import = DateField(verbose_name='Дата импорта', max_length=120)
    
    def __unicode__(self):
        return self.code