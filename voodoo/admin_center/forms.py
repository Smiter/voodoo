# encoding: UTF-8

from django import forms
from django.forms import *

class OrderForm(forms.Form):
    # Создание заказа
    
    # Информация о заказчике
    client_name = CharField(label='Ф.И.О. или название клиента', max_length=50)
    client_phone = CharField(label='Контактные телефоны', max_length=50)
    client_code = CharField(label='Код клиента в ATSP', max_length=50, required=False)
    client_additional_information = CharField(
                                              label='Дополнительная информация',
                                              widget=Textarea(
                                                              attrs={'style': 'max-height:60px;min-height:60px;'
                                                                     + 'max-width:400px;min-width:400px'}
                                                              ),
                                              required=False
                                              )
    required_css_class = 'required'
    # Информация о авто
    car_brand = CharField(label='Марка автомобиля', max_length=50, required=False)
    car_vin = CharField(label='VIN', min_length=17, max_length=17, required=False)
    car_model = CharField(label='Модель/Серия', max_length=50, required=False)
    car_engine = CharField(label='Двигатель', max_length=50, required=False)
    car_year = CharField(label='Год выпуска', max_length=50, required=False)
    car_engine_size = CharField(label='Объем двигателя', max_length=50, required=False)
    car_body = ChoiceField(
                                      label="Кузов",
                                      widget=Select(),
                                      choices=([
                                                ('Седан', 'Седан'),
                                                ('Хетчбек', 'Хетчбек'),
                                                ('Универсал', 'Универсал'),
                                                ('Джип', 'Джип'),
                                                ('Минивен', 'Минивен'),
                                                ('Купе', 'Купе'),
                                                ('Автобус', 'Автобус'),
                                                ('Грузовик', 'Грузовик'),
                                                ]),
                                      initial='Седан',
                                      required=False)
    car_gearbox = ChoiceField(
                                      label="КПП",
                                      widget=Select(),
                                      choices=([
                                                ('Ручная', 'Ручная'),
                                                ('Автомат', 'Автомат'),
                                                ('Вариатор', 'Вариатор'),
                                                ('Робот', 'Робот'),
                                                ]),
                                      initial='Ручная',
                                      required=False)
    car_additional_information = CharField(
                                              label='Дополнительная информация',
                                              widget=Textarea(
                                                              attrs={'style': 'max-height:60px;min-height:60px;'
                                                                     + 'max-width:400px;min-width:400px'}
                                                              ),
                                              required=False
                                              )
    # Информация о заказе и запчастям
    order_info = CharField(
                           label='Полная формулировка заказа',
                           widget=Textarea(
                                           attrs={'style': 'max-height:60px;min-height:60px;'
                                                  + 'max-width:400px;min-width:400px'}
                                           )
                           )
    
    # Список запчастей заказа (таблица на темплейте)
    
class OrdersManagementForm(forms.Form):
    # Фильтр
    order_filter_number = CharField(label='Номер заказа', required=False)
    order_filter_status = ChoiceField(
                                      label="Статус заказа",
                                      widget=Select(),
                                      choices=([
                                                ('Принят', 'Принят'),
                                                ('Обработан', 'Обработан'),
                                                ('Закрыт', 'Закрыт')
                                                ]),
                                      initial='Принят',
                                      required=False)                        
    
    order_filter_creation_date_1 = DateField(label='Создан между')
    order_filter_creation_date_2 = CharField(label='и')
    order_filter_text = CharField(label='Искать текст')
    order_filter_order_part = CharField(label='в инфе о')
