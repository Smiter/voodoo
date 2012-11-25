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

