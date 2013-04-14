#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.forms import *
import re
from captcha.fields import CaptchaField
from models import *
from bootstrap_toolkit.widgets import BootstrapDateInput
from voodoo.admin_center.models import Order, Shipment


def check_pass_on_numbers(text):
    return re.match('^(?=.*[a-zA-Z])[a-zA-Z0-9]+$', text)


class UserRegistrationForm(forms.Form):
    username = CharField(label='Логин')
    password1 = CharField(label="Пароль", widget=PasswordInput())
    password2 = CharField(label="Пароль(ещё раз)", widget=PasswordInput())
    required_css_class = 'required'
    fio = CharField(label="Ф.И.О")
    client_type = ChoiceField(
        label="Тип клиента",
        widget=Select(),
        choices=([
            ('выберите из списка', 'выберите из списка'),
            ('Автосервис/СТО', 'Автосервис/СТО'),
            ('Автопарк', 'Автопарк'),
            ('Автомагазин', 'Автомагазин'),
            ('Автосалон', 'Автосалон'),
            ('Автоэксперт страховщик', 'Автоэксперт страховщик'),
            ('Частный клиент', 'Частный клиент')
        ]),
        initial='выберите из списка'
       )
    email = EmailField(label="E-mail")
    country = CharField(label="Страна", initial='Украина')
    city = CharField(label="Город")
    phiz_adress = CharField(label="Физический адресс", required=False)
    phone = CharField(label="Контактные телефоны")
    contacts = CharField(label="Контактные лица", required=False)
    additional_info = CharField(
        max_length=200,
        label="Дополнительная информация",
        widget=Textarea(
            attrs={'style': 'max-height:60px;min-height:60px;'
                  + 'max-width:300px;min-width:300px'}
        ),
        required=False)
    carrier_default = ChoiceField(
        label="Перевозчик по умолчанию",
        widget=Select(),
        choices=CARRIER_CHOICES,
        required=False)
    carrier_select = CharField(label="Ваш перевозчик", required=False)
    captcha = CaptchaField()

    def clean(self):
        password1 = self.cleaned_data.get('password1', None)
        password2 = self.cleaned_data.get('password2', None)
        name = self.cleaned_data.get('username', None)
        if password1 and name and (password1 == name):
            raise forms.ValidationError('Пароль должен отличатся от имени.')
        if password1 and password2 and (password1 != password2):
            raise forms.ValidationError('Пароли не совпадают.')

        return self.cleaned_data

    def clean_username(self):
        name = self.cleaned_data['username']
        if len(name) < 4:
            raise forms.ValidationError('Должно быть минимум 4 символа.')

        if not check_pass_on_numbers(name):
            raise forms.ValidationError('Имя не должно содержать только цифры.')
        return name

    def clean_password1(self):
        password = self.cleaned_data['password1']

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
        if phiz_adress != "":
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
        if contacts != "":
            if not re.match(u'^[a-zA-Zа-яА-Я ]+$', contacts):
                raise forms.ValidationError('Поле должно содержать латиницу или кирилицу без цифр')
        return contacts

    def clean_carrier_select(self):
        carrier = self.cleaned_data.get('carrier_default', None)
        your_carrier = self.cleaned_data['carrier_select']
        if carrier == u'Ваш перевозчик':
            if your_carrier == "":
                raise forms.ValidationError('Укажите вашего перевозчика')
        return your_carrier


class PrepaysForm(ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Prepays
        fields = ('date', 'summa', 'valuta', 'type_of_payment', 'additional_info')
        widgets = {
            'date': BootstrapDateInput,
            'additional_info': Textarea(
            attrs={'style': 'max-height:60px;min-height:60px;'
                  + 'max-width:300px;min-width:300px'}
        ),
        }


class OrderDispatchForm(ModelForm):
    required_css_class = 'required'
    carrier = ChoiceField(
        label="Перевозчик",
        widget=Select(),
        choices=CARRIER_CHOICES)
    your_carrier = CharField(label="Ваш перевозчик", required=False)

    class Meta:
        model = Shipment
        fields = ('carrier', 'your_carrier', 'transporter_department_number', 'city', 'user_fio', 'comment')
        widgets = {
            'comment': Textarea(
            attrs={'style': 'max-height:60px;min-height:60px;'
                  + 'max-width:300px;min-width:300px'}
        )
        }

    def clean_your_carrier(self):
        carrier = self.cleaned_data.get('carrier', None)
        your_carrier = self.cleaned_data['your_carrier']
        if carrier == u'Ваш перевозчик':
            if your_carrier == "":
                raise forms.ValidationError('Укажите вашего перевозчика')
        return your_carrier

    def __init__(self, *args, **kwargs):
        super(OrderDispatchForm, self).__init__(*args, **kwargs)
        self.fields['transporter_department_number'].required = True
        self.fields['city'].required = True
        self.fields['user_fio'].required = True



import datetime
from datetime import date, timedelta


class SendingsForm(forms.Form):
    min_date = DateField(label="Создана/редактирована между ", initial=date.today() - timedelta(days=3), widget=BootstrapDateInput(attrs={'style': 'width:80px'}))
    max_date = DateField(label=" и", initial=datetime.datetime.now(), widget=BootstrapDateInput(attrs={'style': 'width:80px'}))


ORDER_CHOICES = (
            (u'Все', u'Все'),
            (u'Принят', u'Принят'),
            (u'Заказан', u'Заказан'),
            (u'Доставлен', u'Доставлен'),
            (u'Отказ', u'Отказ'),
)


class OrdersForm(forms.Form):
    status = ChoiceField(
        label="Статус",
        widget=Select(attrs={'style': 'width:100px'}),
        choices=ORDER_CHOICES,
        initial='1')
    min_date = DateField(label="Дата от ", initial=date.today() - timedelta(days=3), widget=BootstrapDateInput(attrs={'style': 'width:80px'}))
    max_date = DateField(label=" по", initial=datetime.datetime.now(), widget=BootstrapDateInput(attrs={'style': 'width:80px'}))

CAR_ADDITIONS = (
            ('ABS', 'ABS'),
            (u'Гидроусилитель', u'Гидроусилитель'),
            (u'Кондиционер', u'Кондиционер'),
)


def getVinRequestForm(exclude_list, *args, **kwargs):
    class VinRequestForm(ModelForm):
        required_css_class = 'required'
        car_additional_information = MultipleChoiceField(label="Дополнительно",
        widget=CheckboxSelectMultiple, choices=CAR_ADDITIONS, required=False)

        class Meta:
            model = Order
            exclude = exclude_list + ('user', 'client_code', 'client_additional_information', 'delivery_adress', 'order_status', 'creation_date', 'order_info')

        def __init__(self):
            super(VinRequestForm, self).__init__(*args, **kwargs)
            self.fields['car_brand'].required = True
            self.fields['car_vin'].required = True
            self.fields['car_model'].required = True
            self.fields['car_year'].required = True

    return VinRequestForm()
