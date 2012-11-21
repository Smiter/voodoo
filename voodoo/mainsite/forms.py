# -*- coding:utf-8 -*-

from django import forms
from django.forms import *
from django.core import validators
import logging
import re
# from captcha.fields import CaptchaField
from registration.forms import RegistrationForm


def check_pass_on_numbers(text):
    return re.match('^(?=.*[a-zA-Z])[a-zA-Z0-9]+$', text)


class UserRegistrationForm(RegistrationForm):
    required_css_class = 'required'
    fio = CharField(label="Ф.И.О")
    client_type = ChoiceField(label="Тип клиента", widget=Select(),
                              choices=([
                                       ('выберите из списка', 'выберите из списка'),
                             ('Автосервис/СТО', 'Автосервис/СТО'),
                                  ('Автопарк', 'Автопарк'),
                                  ('Автомагазин', 'Автомагазин'),
                                  ('Автосалон', 'Автосалон'),
                                  ('Автоэксперт страховщик', 'Автоэксперт страховщик'),
                                  ('Частный клиент', 'Частный клиент'), ]),
                              initial='выберите из списка',
                              required = False)
    country = CharField(label="Страна", initial='Украина')
    city = CharField(label="Город")
    phiz_adress = CharField(label="Физический адресс")
    phone = CharField(label="Контактные телефоны")
    contacts = CharField(label="Контактные лица")
    additional_info =  CharField(max_length = 200,label="Дополнительная информация", widget=Textarea(attrs = {'style':'max-height:60px;min-height:60px;max-width:400px;min-width:400px'}),required = False)
    carrier_default = ChoiceField(label="Перевозчик по умолчанию", widget=Select(),
                                  choices=([
                                           ('выберите из списка', 'выберите из списка'),
                                 ('Новая почта', 'Новая почта'),
                                      ('Гюнсел', 'Гюнсел'),
                                      ('САТ', 'САТ')
                                  ]),
                                  initial='1', required = False)
    carrier_select = CharField(label="Ваш перевозчик", required=False)
    # captcha = CaptchaField()

    def clean_username(self):
        name = self.cleaned_data['username']
        if len(name) < 4:
            raise forms.ValidationError('Должно быть минимум 4 символа.')

        if not check_pass_on_numbers(name):
            raise forms.ValidationError('Имя не должно содержать только цифры.')
        return name

    def clean_password1(self):
        password = self.cleaned_data['password1']
        name = self.cleaned_data['username']

        if password == name:
            raise forms.ValidationError('Пароль должен отличатся от имени.')

        if len(password) < 6:
            raise forms.ValidationError('Должно быть минимум 6 символа.')

        if not check_pass_on_numbers(password):
            raise forms.ValidationError('Пароль не должен содержать только цифры.')
        return password

    def clean_fio(self):
        fio = self.cleaned_data['fio']
        if not re.match(u'^[a-zA-Zа-яА-Я ]+$', fio):
            raise forms.ValidationError('Поле должно содержать латиницу или кирилицу без цифр')
        return fio

    def clean_client_type(self):
        client_type = self.cleaned_data['client_type']
        if client_type == u'выберите из списка':
            raise forms.ValidationError('Необходимо указать тип клиента')
        return client_type

    def clean_country(self):
        country = self.cleaned_data['country']
        if not re.match(u'^[a-zA-Zа-яА-Я ]+$', country):
            raise forms.ValidationError('Поле должно содержать латиницу или кирилицу без цифр')
        return country

    def clean_city(self):
        city = self.cleaned_data['city']
        if not re.match(u'^[a-zA-Zа-яА-Я ]+$', city):
            raise forms.ValidationError('Поле должно содержать латиницу или кирилицу без цифр')
        return city

    def clean_phiz_adress(self):
        phiz_adress = self.cleaned_data['phiz_adress']
        if not re.match(u'^[a-zA-Zа-яА-Я ]+$', phiz_adress):
            raise forms.ValidationError('Поле должно содержать латиницу или кирилицу без цифр')
        return phiz_adress

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not re.match(u'^[0-9 -]+$', phone):
            raise forms.ValidationError('Номер телефона указан не верно.')
        return phone

    def clean_contacts(self):
        contacts = self.cleaned_data['contacts']
        if not re.match(u'^[a-zA-Zа-яА-Я ]+$', contacts):
            raise forms.ValidationError('Поле должно содержать латиницу или кирилицу без цифр')
        return contacts


class SignupForm(forms.Form):
    required_css_class = 'required'
    login = CharField(label="Логин")
    password = CharField(label="Пароль", widget=PasswordInput())
    r_password = CharField(label="Пароль(ещё раз)", widget=PasswordInput())
    fio = CharField(label="Ф.И.О")
    client_type = ChoiceField(label="Тип клиента", widget=Select(),
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
    country = CharField(label="Страна", initial='Украина')
    city = CharField(label="Город")
    Phiz_adress = CharField(label="Физический адресс")
    phone = CharField(label="Контактные телефоны")
    contacts = CharField(label="Контактные лица")
    additional_info = CharField(label="Дополнительная информация")
    carrier_default = ChoiceField(label="Перевозчик по умолчанию", widget=Select(),
                                  choices=([
                                           ('1', 'выберите из списка'),
                                 ('2', 'Новая почта'),
                                      ('3', 'Гюнсел'),
                                      ('4', 'САТ')
                                  ]),
                                  initial='1', required = False)
    carrier_select = CharField(label="Ваш перевозчик", required=False)
