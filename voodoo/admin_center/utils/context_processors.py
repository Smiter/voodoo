# -*- coding: utf-8 -*-
from voodoo.admin_center.models import *

def global_vars(request):
    return {
        'menu_elements': getMenuElements(),
        'suppliersList': Supplier.objects.all(),
        'currencyList': Currency.objects.all(),
        'statusList': ItemStatus.objects.all(),
    }
    
def getMenuElements():
    menu_elements = Menu.getActiveElements(Menu())
    for element in menu_elements:
        # Was decided to use element.name instead of external configuration file or hard-code link inside DB
        element.link = element.name
    return menu_elements