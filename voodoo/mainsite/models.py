#coding=utf-8

from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
# Create your models here.


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


try:
    admin.site.register(Profile)
except:
    pass
