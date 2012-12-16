# encoding: UTF-8
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template
from voodoo.admin_center.models import Menu, Order, Product, Supplier
from voodoo.admin_center.forms import OrderForm, OrdersManagementForm,\
    XlsImportForm, TestForm
import xlrd

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

@login_required(login_url='/admin_center/login/')
def xls_import(request):
    message = '';
    
    if request.method == 'POST':
        form = XlsImportForm(request.POST, request.FILES or None)
        
        if form.is_valid():
            rows_added = 0
            # adapting column numbers to xlrd: -1
            column_number = int(request.POST['column_number']) - 1
            column_brand = int(request.POST['column_brand']) - 1
            column_count = int(request.POST['column_count']) - 1
            column_price = int(request.POST['column_price']) - 1
            start_row = int(request.POST['start_row']) - 1
            
            # column_description optional 
            if request.POST['column_description'] is not None:
                column_description = int(request.POST['column_description']) - 1
            
            supplier = Supplier.objects.get(id = int(request.POST['supplier']))
            
            # opening file
            file_name = request.FILES['file']
            rb = xlrd.open_workbook(file_contents=file_name.read())
            sheet = rb.sheet_by_index(0)
            
            # going through rows in range
            for rownum in range(start_row, sheet.nrows):
                row = sheet.row_values(rownum)
                
                # creating Model
                product = Product(code = row[column_number], brand = row[column_brand], 
                                  description = row[column_description], count = row[column_count], 
                                  price = [column_price])
                product.save()
                product.supplier.add(supplier)
                
                rows_added += 1
                
            # message
            message = "Файл %s успешно импортирован. %s записей добавлено." % (file_name, rows_added)
            
            # cleaning form
            form = XlsImportForm()
    else:
        form = XlsImportForm()
            
    return direct_to_template(request, 'xls_import.html', {'menu_elements': getMenuElements(), 'form': form, 'message': message})

def getMenuElements():
    menu_elements = Menu.getActiveElements(Menu())
    for element in menu_elements:
        # Was decided to use element.name instead of external configuration file or hard-code link inside DB
        element.link = element.name
        
    return menu_elements

def test_view(request):
    form = TestForm(request.POST);
    
    print 'initial enter'
    
    if form.is_valid():
        print 'form is valid'
    
    return direct_to_template(request, 'test.html', {'menu_elements': getMenuElements(), 'form': form})