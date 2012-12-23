# coding=utf-8
from django.db import models

# Create your models here.
from django.db import models

LIFT_CHOICES = (
    ('1', u'Подъемник 1'),
    ('2', u'Подъемник 2'),
    )

class Event(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    client_name = models.CharField(max_length=100)
    client_number = models.CharField(max_length=100)
    car_description = models.CharField(max_length=100)
    work_description = models.CharField(max_length=100)
    worker = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    lift = models.CharField(max_length=30, choices=LIFT_CHOICES, verbose_name=u'Выбор подъемника')
