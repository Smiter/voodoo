#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.template.loader import render_to_string
from registration.models import RegistrationProfile
from registration.models import RegistrationManager
from voodoo.admin_center.models import DiscountGroup, Order


CLIENT_TYPE = (
            (u'Автосервис/СТО', u'Автосервис/СТО'),
            (u'Автопарк', u'Автопарк'),
            (u'Автомагазин', u'Автомагазин'),
            (u'Автосалон', u'Автосалон'),
            (u'Автоэксперт страховщик', u'Автоэксперт страховщик'),
            (u'Частный клиент', u'Частный клиент')
)

CARRIER_CHOICES = (
            (u'Ваш перевозчик', u'Ваш перевозчик'),
            (u'Гюнсел', u'Гюнсел'),
            (u'САТ', u'САТ'),
            (u'Новая почта', u'Новая почта'),
)

VALUTA_CHOICES = (
            ('UAH', 'UAH'),
            ('USD', 'USD'),
)

TYPE_OF_PAYMENT_CHOICES = (
            (u'ПриватБанк', u'ПриватБанк'),
            (u'Правэкс', u'Правэкс'),
            (u'Другое', u'Другое')
)

ORDER_CHOICES = (
            (u'Сообщен', u'Сообщен'),
            (u'Оформлен', u'Оформлен'),
            (u'Заказан', u'Заказан'),
            (u'Доставлен', u'Доставлен'),
            (u'Отказ', u'Отказ'),
)


class MyRegistrationProfile(RegistrationProfile):

    objects = RegistrationManager()

    def send_activation_email(self, site):
        profile = Profile.objects.get(user=self.user)
        ctx_dict = {
            'activation_key': self.activation_key,
            'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
            'site': site,
            'username': self.user.username,
            'password': self.user.password,
            'contacts': profile.contacts,
            'client_type': profile.client_type
            }
        subject = render_to_string('registration/activation_email_subject.txt',
                                   ctx_dict)
        subject = ''.join(subject.splitlines())

        message = render_to_string('registration/activation_email.txt',
                                   ctx_dict)

        self.user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)


class Profile(models.Model):
    user = models.ForeignKey(User, unique=True)
    fio = models.CharField(max_length=120)
    client_type = models.CharField(verbose_name='Тип клиента', choices=CLIENT_TYPE, max_length=120)
    country = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    phiz_adress = models.CharField(max_length=120, blank=True, null=True)
    phone = models. CharField(max_length=120)
    contacts = models.CharField(max_length=120, blank=True, null=True)
    additional_info = models.CharField(max_length=120, blank=True, null=True)
    carrier_default = models.CharField(verbose_name='Перевозчик по умолчанию', choices=CARRIER_CHOICES, max_length=120, blank=True, null=True)
    carrier_select = models.CharField(max_length=120, blank=True, null=True)
    font_color = models.CharField(max_length=120, blank=True, null=True)
    discount_group = models.ForeignKey(DiscountGroup, blank=True, null=True)

    def __unicode__(self):
        return "%s" % self.user

    class Meta:
        verbose_name = "User profile"
        verbose_name_plural = "User profiles"


class Prepays(models.Model):
    user = models.ForeignKey(User, unique=False)
    date = models.DateField(max_length=120, verbose_name='Дата проплаты')
    summa = models.CharField(max_length=50, verbose_name='Сумма')
    valuta = models.CharField(max_length=30, choices=VALUTA_CHOICES, verbose_name='Валюта')
    type_of_payment = models.CharField(max_length=30, choices=TYPE_OF_PAYMENT_CHOICES, verbose_name='Тип платежа')
    additional_info = models.CharField(max_length=500, verbose_name='Информация об оплате')
    confirmed = models.BooleanField(max_length=1, default=0)

    def __unicode__(self):
        return "%s" % self.user

    class Meta:
        verbose_name = "Prepays"
        verbose_name_plural = "Prepays"


class OrderDispatch(models.Model):
    user = models.ForeignKey(User, unique=False)
    carrier = models.CharField(max_length=30, choices=CARRIER_CHOICES, verbose_name='Перевозчик')
    department = models.CharField(max_length=150, verbose_name='Отделение транспортной компании', blank=True, null=True)
    city_recipient = models.CharField(max_length=100, verbose_name='Город получателя')
    name_recipient = models.CharField(max_length=150, verbose_name='Имя получателя')
    comment = models.CharField(max_length=500, verbose_name='Комментарии', blank=True, null=True)

    def __unicode__(self):
        return "%s" % self.user

    class Meta:
        verbose_name = "OrderDispatch"
        verbose_name_plural = "OrderDispatch"


class Sendings(models.Model):
    user = models.ForeignKey(User, unique=False)
    date = models.DateField(max_length=120, verbose_name='Время отправки')
    time_of_view = models.DateTimeField(max_length=120, verbose_name='Время просмотра пользователем', blank=True, null=True)
    receiver = models.CharField(max_length=50, verbose_name='Получатель')
    city = models.CharField(max_length=30, verbose_name='Город')
    warehouse = models.CharField(max_length=30, verbose_name='Склад')
    declaration_number = models.CharField(max_length=500, verbose_name='Номер декларации')

    def __unicode__(self):
        return "%s" % self.user

    class Meta:
        verbose_name = "Sendings"
        verbose_name_plural = "Sendings"


class VinRequest(models.Model):
    order = models.ForeignKey(Order)