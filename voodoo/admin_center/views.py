# Create your views here.
from django.views.generic.simple import direct_to_template
from voodoo.admin_center.models import Menu
from django.contrib.auth.decorators import login_required

#from django.db import models

@login_required(login_url='/admin_center/login/')
def admin_center(request):
    #TODO add checking for super user
    return direct_to_template(request, 'admin_center.html', {'menu_elements': getMenuElements()})

@login_required(login_url='/admin_center/login/')
def order_create(request):
    #TODO
    return direct_to_template(request, 'order_create.html', {'menu_elements': getMenuElements()})

@login_required(login_url='/admin_center/login/')
def order_details(request):
    #TODO
    return direct_to_template(request, 'order_details.html', {'menu_elements': getMenuElements()})

@login_required(login_url='/admin_center/login/')
def orders_management(request):
    #TODO
    return direct_to_template(request, 'orders_management.html', {'menu_elements': getMenuElements()})

@login_required(login_url='/admin_center/login/')
def orders_import(request):
    #TODO
    return direct_to_template(request, 'orders_import.html', {'menu_elements': getMenuElements()})

@login_required(login_url='/admin_center/login/')
def test(request):
    return direct_to_template(request, 'admin_base.html', {'menu_elements': getMenuElements()})

def getMenuElements():
    menu_elements = Menu.getActiveElements(Menu())
    for element in menu_elements:
        # Was decided to use element.name instead of external configuration file or hard-code link inside DB
        element.link = element.name
        
    return menu_elements