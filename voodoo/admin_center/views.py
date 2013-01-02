# encoding: UTF-8
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template
from voodoo.admin_center.models import Menu, Order, Product, Supplier, OrderItem
from voodoo.admin_center.forms import *
import xlrd
from django.contrib.auth.models import User
from voodoo.mainsite.models import Profile
from decimal import Decimal
#from django.db import models


@login_required(login_url='/admin_center/login/')
def admin_center(request):
    #TODO add checking for super user
    return direct_to_template(request, 'admin_center.html', {})


@login_required(login_url='/admin_center/login/')
def order_create(request):
    message = ''
    if request.method == 'POST':
        form = OrderForm(request.POST or None)
        # TODO validating
        # JS validation
        # rowCount = int(request.POST['row_count'])
        # TODO use OrderStatus, ItemStatus, Currency models

        if form.is_valid():
            # order_total_price1 = request.POST['total_sum_1']
            # order_total_price2 = request.POST['total_sum_2']
            
            #TODO if code/brand empty - skipp item
            order = form.save()
            # message about saving
            message = 'Заказ создан. ID: %s' % order.id
            
            rowCount = int(request.POST['row_count'])
            for i in range(1, rowCount + 1):
                code = request.POST['row%s_code' % i]
                brand = request.POST['row%s_brand' % i]
                comment = request.POST['row%s_comment' % i]
                price_1 = request.POST['row%s_price_1' % i]
                price_2 = request.POST['row%s_price_2' % i]
                currency = request.POST['row%s_currency' % i]
                count = request.POST['row%s_count' % i]
                supplier = request.POST['row%s_supplier' % i]
                delivery_time = request.POST['row%s_delivery_time' % i]
                status = request.POST['row%s_status' % i]
                # working only with rows where 'code' is not empty
                if (code):
                    try:
                        product = Product.objects.get(code=code)
                        
                        item = OrderItem(order=order, code=code, brand=brand, comment=comment, price_1=price_1, price_2=price_2,
                                         currency=currency, count=count, supplier=supplier, delivery_time=delivery_time, status=status, product=product)
                        item.save()
                        
                    except Product.DoesNotExist:
                        # raise Product.DoesNotExist(u"Продукт с id = " + code + u" не существует")
                        # should return validation error
                        message = u"Продукт с id '" + code + u"' не существует";
            # TODO if status is 'Отказ' отправляем письмо на указаный в профиле e-mail(номер заявки, номер запчасти и комментарий)
            form = OrderForm()
    else:
        form = OrderForm()
    return direct_to_template(request, 'order_create.html', {'form': form, 'message': message})


@login_required(login_url='/admin_center/login/')
def orders_management(request):
    #TODO
    message = ''
    results = None
    if request.method == 'POST':
        form = OrdersManagementForm(request.POST or None)
        if form.is_valid():
            # TODO validating
            results = Order.objects.all()
            # TODO rendering order
            # message
            order = 'id will be here'
            message = 'Заказ сохранен. ID: %s' % order
    else:
        form = OrdersManagementForm()
    return direct_to_template(request, 'orders_management.html', {'form': form, 'results': results, 'message': message})


@login_required(login_url='/admin_center/login/')
def order_edit(request):
    if request.method == 'POST':
        #TODO
        # edit order
        form = OrderForm(request.POST or None)
        if form.is_valid():
            # TODO validating
            # editing order
            print None
    else:
        #TODO
        # drawing order
        form = OrderForm()
    return direct_to_template(request, 'order_edit.html', {'form': form})


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
    return direct_to_template(request, 'orders_import.html', {'form': form})


@login_required(login_url='/admin_center/login/')
def xls_import(request):
    message = ''
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
            supplier = Supplier.objects.get(id=int(request.POST['supplier']))
            currency = Currency.objects.get(id=int(request.POST['currency']))
            # opening file
            file_name = request.FILES['file']
            rb = xlrd.open_workbook(file_contents=file_name.read())
            sheet = rb.sheet_by_index(0)
            # going through rows in range
            for rownum in range(start_row, sheet.nrows):
                row = sheet.row_values(rownum)
                # creating Model
                product = Product(code=row[column_number], brand=row[column_brand],
                                  description=row[column_description], count=row[column_count],
                                  price=Decimal([column_price]))
                product.save()
                product.supplier.add(supplier)
                product.supplier.add(currency)
                rows_added += 1
            # message
            message = "Файл %s успешно импортирован. %s записей добавлено." % (file_name, rows_added)
            # cleaning form
            form = XlsImportForm()
    else:
        form = XlsImportForm()
    return direct_to_template(request, 'xls_import.html', {'form': form, 'message': message})

# TODO use permission system
#@permission_required('polls.can_vote', login_url='/admin_center/login/')
@login_required(login_url='/admin_center/login/')
def user_management(request):
    message = ''
    
    if request.method == 'POST':
        form = OrderForm(request.POST or None)
        
        # find filtered results 
    else:
        form = UserManagementForm()
        results = Profile.objects.all()
    
    return direct_to_template(request, 'user_management.html', {'form': form, 'message': message, 'results': results})

def getMenuElements():
    menu_elements = Menu.getActiveElements(Menu())
    for element in menu_elements:
        # Was decided to use element.name instead of external configuration file or hard-code link inside DB
        element.link = element.name
    return menu_elements
