# coding=utf-8
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db import models


class Event(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    client_name = models.CharField(max_length=100)
    client_number = models.CharField(max_length=100)
    car_description = models.CharField(max_length=100)
    work_description = models.CharField(max_length=100)
    worker = models.ForeignKey(User, unique=False)
    price = models.CharField(max_length=100)


class Event2(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    client_name = models.CharField(max_length=100)
    client_number = models.CharField(max_length=100)
    car_description = models.CharField(max_length=100)
    work_description = models.CharField(max_length=100)
    worker = models.ForeignKey(User, unique=False)
    price = models.CharField(max_length=100)
