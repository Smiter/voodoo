# encoding: UTF-8
from django.db import models

# Create your models here.

class Menu(models.Model):
    name = models.CharField(max_length=30)
    title = models.CharField(max_length=30)
    enabled = models.BooleanField()
    
    def getAllElements(self):
        # TODO remove
        print Menu.objects.all()
        return Menu.objects.all()

    def getActiveElements(self):
        # TODO remove
        print Menu.objects.filter(enabled=True)
        return Menu.objects.filter(enabled=True)
    
    def fillTable(self):
        # TODO initial data
        # Menu(name='name', title='title', enabled=True)
        return None
    
    def __unicode__(self):
        return self.name
    