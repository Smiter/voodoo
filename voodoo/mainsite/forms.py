# -*- coding:utf-8 -*-

from django import forms
from django.forms import *


from registration.forms import RegistrationForm

class UserRegistrationForm(RegistrationForm):
    required_css_class = 'required'
    fio = CharField(label="Ф.И.О")
    client_type = ChoiceField(label="Тип клиента",widget=Select(),
                              choices=([
                                       ('1', 'выберите из списка'),
                             ('Автосервис/СТО', 'Автосервис/СТО'),
                                  ('Автопарк', 'Автопарк'),
                                  ('4', 'Автомагазин'),
                                  ('5', 'Автосалон'),
                                  ('6', 'Автоэксперт страховщик'),
                                  ('7', 'Частный клиент'), ]),
                              initial='1',
                              required = False)
    country = CharField(label="Страна",initial='Украина')
    city = CharField(label="Город")
    phiz_adress = CharField(label="Физический адресс")
    phone = CharField(label="Контактные телефоны")
    contacts = CharField(label="Контактные лица")
    additional_info = CharField(label="Дополнительная информация")
    carrier_default = ChoiceField(label="Перевозчик по умолчанию",widget=Select(),
                              choices=([
                                       ('1', 'выберите из списка'),
                             ('2', 'Новая почта'),
                                  ('3', 'Гюнсел'),
                                  ('4', 'САТ')
                               ]),
                              initial='1',required = False)
    carrier_select = CharField(label="Ваш перевозчик",required = False)



class SignupForm(forms.Form):
    required_css_class = 'required'
    login = CharField(label="Логин")
    password = CharField(label="Пароль",widget=PasswordInput())
    r_password = CharField(label="Пароль(ещё раз)",widget=PasswordInput())
    fio = CharField(label="Ф.И.О")
    client_type = ChoiceField(label="Тип клиента",widget=Select(),
                              choices=([
                                       ('1', 'выберите из списка'),
                             ('2', 'Автосервис/СТО'),
                                  ('3', 'Автопарк'),
                                  ('4', 'Автомагазин'),
                                  ('5', 'Автосалон'),
                                  ('6', 'Автоэксперт страховщик'),
                                  ('7', 'Частный клиент'), ]),
                              initial='1',
                              required = False)
    email = EmailField(label="E-mail")
    country = CharField(label="Страна",initial='Украина')
    city = CharField(label="Город")
    Phiz_adress = CharField(label="Физический адресс")
    phone = CharField(label="Контактные телефоны")
    contacts = CharField(label="Контактные лица")
    additional_info = CharField(label="Дополнительная информация")
    carrier_default = ChoiceField(label="Перевозчик по умолчанию",widget=Select(),
                              choices=([
                                       ('1', 'выберите из списка'),
                             ('2', 'Новая почта'),
                                  ('3', 'Гюнсел'),
                                  ('4', 'САТ')
                               ]),
                              initial='1',required = False)
    carrier_select = CharField(label="Ваш перевозчик",required = False)



