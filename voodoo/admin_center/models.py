#!/usr/bin/env python
# encoding: UTF-8
from django.db import models
from django.db.models import *
from django.core.validators import MaxLengthValidator
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from voodoo.mainsite.basket.models import Cart
from django.contrib.contenttypes.models import ContentType
from voodoo.mainsite.models import Profile



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


class OrderStatus(models.Model):
    status = CharField(verbose_name='Статус выполнения заказа', max_length=120)
    color = CharField(verbose_name='Цвет', max_length=120)
    
    def __unicode__(self):
        return self.status
    
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
    order_status = models.ForeignKey(OrderStatus, verbose_name='Статус выполнения заказа', blank=True, null=True)
    creation_date = DateTimeField(verbose_name='Дата создания', max_length=120, auto_now_add=True)
#    order_total_price1 = DecimalField(verbose_name='Всего Цена 1', max_length=120, max_digits=20, decimal_places=1, blank=True)
#    order_total_price2 = DecimalField(verbose_name='Всего Цена 2', max_length=120, max_digits=20, decimal_places=1, blank=True)

    def __unicode__(self):
        return str(self.id)

class Supplier(models.Model):
    name = CharField(verbose_name='Название', max_length=120)
    time_out = IntegerField(verbose_name='Часов до просрочки', max_length=20)
    delivery_time = CharField(verbose_name='Срок поставки', max_length=120)
    transporter = CharField(verbose_name='Перевозчик', max_length=120, blank=True, null=True)
    contact_information = CharField(verbose_name='Контактная информация', max_length=500, blank=True, null=True)
    time_closing_order = TimeField(verbose_name='Время закрытия заказа', max_length=20)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Поставщик"
        ordering = ['name']

class Currency(models.Model):
    name = CharField(verbose_name='Название', max_length=120)
    code = CharField(verbose_name='Код', max_length=120)
    ratio = DecimalField(verbose_name='Коэффициент', max_length=120, max_digits=20, decimal_places=1)
    
    def __unicode__(self):
        return self.code
    

class Product(models.Model):
    code = CharField(verbose_name='Номер', max_length=120)
    brand = CharField(verbose_name='Бдэнд', max_length=120)
    description = CharField(verbose_name='Описание', max_length=120, blank=True)
    count = IntegerField(verbose_name='Количество', max_length=120, blank=True)
    price = DecimalField(verbose_name='Цена', max_length=120, max_digits=20, decimal_places=1)
    supplier = models.ForeignKey(Supplier)
    currency = models.ForeignKey(Currency)
    date_of_import = DateTimeField(verbose_name='Дата импорта', max_length=120, auto_now_add=True)

    def get_price_with_currency(self):
        return float(self.price * self.currency.ratio)
    price_with_currency = property(get_price_with_currency)

    def __unicode__(self):
        return self.code


class ItemManager(models.Manager):
    def get(self, *args, **kwargs):
        if 'product' in kwargs:
            kwargs['content_type'] = ContentType.objects.get_for_model(type(kwargs['product']))
            kwargs['object_id'] = kwargs['product'].pk
            del(kwargs['product'])
        return super(ItemManager, self).get(*args, **kwargs)


class ItemStatus(models.Model):
    status = CharField(verbose_name='Статус', max_length=120)
    color = CharField(verbose_name='Цвет', max_length=120)
    
    def __unicode__(self):
        return self.status


class OrderItem(models.Model):
    order = models.ForeignKey(Order, blank=True, null=True)
    user = models.ForeignKey(User, unique=False, blank=True, null=True)
    code = CharField(verbose_name='Номер', max_length=120)
    brand = CharField(verbose_name='Бдэнд', max_length=120)
    comment = CharField(verbose_name='Комментарий', max_length=120, blank=True)
    price_1 = DecimalField(verbose_name='Цена1', max_length=120, max_digits=20, decimal_places=1)
    price_2 = DecimalField(verbose_name='Цена2', max_length=120, max_digits=20, decimal_places=1)
    currency = CharField(verbose_name='Тип валюты', max_length=120)
    count = PositiveIntegerField(verbose_name='Количество', max_length=120)
    supplier = models.ForeignKey(Supplier, verbose_name='Поставщик', blank=True, null=True)
    delivery_time = CharField(verbose_name='Срок поставки', max_length=120)
    status = models.ForeignKey(ItemStatus)
    cart = models.ForeignKey(Cart, verbose_name='Корзина', blank=True, null=True)
    # quantity = models.PositiveIntegerField(verbose_name=_('quantity'))
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    objects = ItemManager()
    creation_date = DateTimeField(verbose_name='Дата создания', max_length=120, auto_now_add=True)
    status_expired_date = DateTimeField(verbose_name='Дата просрочки заказа', max_length=120, blank=True, null=True)
    
    def __unicode__(self):
        return self.code

    def get_price_with_discount(self):
        discount = self.get_profile_discount()
        if not discount:
            discount = 0
        return float(self.product.price_with_currency - (float(self.product.price_with_currency) / float(100)) * float(discount))

    def total_price(self):
        return self.count * self.get_price_with_discount()
    total_price = property(total_price)

    def get_profile_discount(self):
        if self.user:
            return Profile.objects.get(user=self.user).discount_group.discount
        return None

    # product
    def get_product(self):
        return self.content_type.get_object_for_this_type(id=self.object_id)

    def set_product(self, product):
        self.content_type = ContentType.objects.get_for_model(type(product))
        self.object_id = product.pk

    product = property(get_product, set_product)


class DiscountGroup(models.Model):
    name = CharField(verbose_name='Название', max_length=120)
    discount = DecimalField(verbose_name='Наценка в %', max_length=15, max_digits=4, decimal_places=1)
    
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Группа скидок"


class ShipmentType(models.Model):
    code = CharField(verbose_name='Код отправки', max_length=120, blank=True, null=True)
    name = CharField(verbose_name='Тип отправки', max_length=120, blank=True, null=True)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = "Тип отправки"

class Shipment(models.Model):
    type = models.ForeignKey(ShipmentType, blank=True, null=True)
    declaration_number = CharField(verbose_name='Номер декларации', max_length=120, blank=True, null=True, default='')
    creation_date = DateTimeField(verbose_name='Дата создания', max_length=120, auto_now_add=True)
    comment = CharField(verbose_name='Комментарий', max_length=120, blank=True, null=True, default='')
    price = CharField(verbose_name='Сумма', max_length=120, blank=True, null=True)
    supplier = CharField(verbose_name='Поставщик', max_length=120, blank=True, null=True)
    arrival_date = DateTimeField(verbose_name='Дата прибытия', max_length=120, blank=True, null=True)
    recived = BooleanField(verbose_name='Товар получен')
    city = CharField(verbose_name='Город', max_length=120, blank=True, null=True)

    
    user_login = CharField(verbose_name='Логин Клиента', max_length=120, blank=True, null=True)
    user_fio = CharField(verbose_name='Получатель', max_length=120, blank=True, null=True)
    user_notified = BooleanField(verbose_name='Клиент уведомлен')
    
    transporter_name = CharField(verbose_name='Перевозчик', max_length=120, blank=True, null=True)
    transporter_department_number = CharField(verbose_name='Отделение', max_length=120, blank=True, null=True)
    transporter_count_of_places = CharField(verbose_name='Количество мест', max_length=120, blank=True, null=True, default='')

