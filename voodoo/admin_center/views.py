# encoding: UTF-8

from django.views.generic.simple import direct_to_template
from voodoo.admin_center.models import Menu, Order
from django.contrib.auth.decorators import login_required
from voodoo.admin_center.forms import OrderForm, OrdersManagementForm

#from django.db import models

@login_required(login_url='/admin_center/login/')
def admin_center(request):
    #TODO add checking for super user
    return direct_to_template(request, 'admin_center.html', {'menu_elements': getMenuElements()})

@login_required(login_url='/admin_center/login/')
def order_create(request):
    form = OrderForm(request.POST or None)
    
    if form.is_valid():
        # TODO validating
        # TODO working with data
        order = Order()
        order.save()
        # TODO add message about saving
        
        return direct_to_template(request, 'admin_center.html', {'menu_elements': getMenuElements(), 'form': form})
    else:
        form = OrderForm()
        
    return direct_to_template(request, 'order_create.html', {'menu_elements': getMenuElements(), 'form': form})

@login_required(login_url='/admin_center/login/')
def orders_management(request):
    #TODO
    form = OrdersManagementForm(request.POST or None)
    if form.is_valid():
        # TODO validating
        # TODO filtering from DB
        # TODO rendering filtered data
        # message 'Найдены следующие заказы(для полного просмотра выберите нужный в списке)
        # using results
        print None
    else:
        form = OrdersManagementForm()
        
    return direct_to_template(request, 'orders_management.html', {'menu_elements': getMenuElements(), 'form': form})

@login_required(login_url='/admin_center/login/')
def orders_import(request):
    # TODO
    # remove copy/paste
    form = OrdersManagementForm(request.POST or None)
    if form.is_valid():
    # using results
    # TODO filtering from DB
    # TODO rendering filtered data
        print None
    else:
        # remove copy/paste
        form = OrdersManagementForm()
        
    return direct_to_template(request, 'orders_import.html', {'menu_elements': getMenuElements(), 'form': form})

def getMenuElements():
    menu_elements = Menu.getActiveElements(Menu())
    for element in menu_elements:
        # Was decided to use element.name instead of external configuration file or hard-code link inside DB
        element.link = element.name
        
    return menu_elements