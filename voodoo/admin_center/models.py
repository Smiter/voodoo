# encoding: UTF-8
from django.db import models

# Create your models here.

class Menu(models.Model):
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    enabled = models.BooleanField()
    
    def getAllElements(self):
        return Menu.objects.all()

    def getActiveElements(self):
        return Menu.objects.filter(enabled=True)
    
    def fillTable(self):
        # TODO initial data
        # Menu(name='name', title='title', enabled=True)
        return None
    
    def __unicode__(self):
        return self.name

class Order(models.Model):
    client_name = models.CharField(max_length=50)
    client_phone = models.CharField(max_length=50)
    client_code = models.CharField(max_length=50)
    client_additional_information = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.client_name