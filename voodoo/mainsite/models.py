#coding=utf-8

from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.conf import settings
from django.template.loader import render_to_string
from registration.models import RegistrationProfile
from registration.models import RegistrationManager


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
    client_type = models.CharField(max_length=120)
    country = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    phiz_adress = models.CharField(max_length=120)
    phone = models. CharField(max_length=120)
    contacts = models.CharField(max_length=120)
    additional_info = models.CharField(max_length=120)
    carrier_default = models.CharField(max_length=120)
    carrier_select = models.CharField(max_length=120)

    def __unicode__(self):
        return "%s" % self.user

    class Meta:
        verbose_name = "User profile"
        verbose_name_plural = "User profiles"


VALUTA_CHOICES = (
            ('UAH', 'UAH'),
            ('USD', 'USD'),
)

TYPE_OF_PAYMENT_CHOICES = (
            ('Webmoney', 'Webmoney'),
            ('Yandex money', 'yandex money'),
)


class NoticeOfPayment(models.Model):
    user = models.ForeignKey(User, unique=False)
    date = models.DateField(max_length=120, verbose_name='Дата проплаты')
    summa = models.CharField(max_length=50, verbose_name='Сумма')
    valuta = models.CharField(max_length=30, choices=VALUTA_CHOICES, verbose_name='Валюта')
    type_of_payment = models.CharField(max_length=30, choices=TYPE_OF_PAYMENT_CHOICES, verbose_name='Тип платежа')
    additional_info = models.CharField(max_length=500, verbose_name='Информация об оплате')

    def __unicode__(self):
        return "%s" % self.user

    class Meta:
        verbose_name = "NoticeOfPayment"
        verbose_name_plural = "NoticeOfPayment"

