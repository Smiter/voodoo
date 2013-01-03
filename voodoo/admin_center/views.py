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
from django.http import HttpResponse
#from django.db import models


@login_required(login_url='/admin_center/login/')
def admin_center(request):
    #TODO add checking for super user
    return direct_to_template(request, 'admin_center.html', {})


@login_required(login_url='/admin_center/login/')
def order_create(request):
    message = u''
    if request.method == 'POST':
        form = OrderForm(request.POST or None)
        # rowCount = int(request.POST['row_count'])
        # TODO use OrderStatus, ItemStatus, Currency models

        if form.is_valid():
            # order_total_price1 = request.POST['total_sum_1']
            # order_total_price2 = request.POST['total_sum_2']
            
            #TODO if code/brand empty - skipp item
            order = form.save()
            # message about saving
            message = u'Заказ создан. ID: %s' % order.id
            
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
            message = u'Заказ сохранен. ID: %s' % order
    else:
        form = OrdersManagementForm()
    return direct_to_template(request, 'orders_management.html', {'form': form, 'results': results, 'message': message})


@login_required(login_url='/admin_center/login/')
def order_edit(request, id):
    message =''
    if request.method == 'POST':
        form = OrderForm(request.POST or None)
        
        if form.is_valid():
            order = Order.objects.get(id=id)
            
            order.client_name = request.POST['client_name']
            order.client_phone = request.POST['client_phone']
            order.client_code = request.POST['client_code']
            order.client_additional_information = request.POST['client_additional_information']
            order.car_brand = request.POST['car_brand']
            order.car_vin = request.POST['car_vin']
            order.car_model = request.POST['car_model']
            order.car_engine = request.POST['car_engine']
            order.car_year = request.POST['car_year']
            order.car_engine_size = request.POST['car_engine_size']
            order.car_body = request.POST['car_body']
            order.car_gearbox = request.POST['car_gearbox']
            order.car_additional_information = request.POST['car_additional_information']
            order.order_info = request.POST['order_info']
            order.order_additional_information = request.POST['order_additional_information']
            order.order_status = request.POST['order_status']
            
            order.save()
            
            rowCount = int(request.POST['row_count'])
            for i in range(1, rowCount + 1):
                # working only with rows where 'code' is not empty
                code = request.POST['row%s_code' % i]
                item = None
                if (code):
                    try:
                        item = OrderItem.objects.get(order_id=order.id, code=code)
                    except OrderItem.DoesNotExist:
                        message = u"OrderItem с кодом '" + code + u"' не существует";
                        
                    if item is not None:
                        # updating current item
                        item.code = request.POST['row%s_code' % i]
                        item.brand = request.POST['row%s_brand' % i]
                        item.comment = request.POST['row%s_comment' % i]
                        item.price_1 = request.POST['row%s_price_1' % i]
                        item.price_2 = request.POST['row%s_price_2' % i]
                        item.currency = request.POST['row%s_currency' % i]
                        item.count = request.POST['row%s_count' % i]
                        item.supplier = request.POST['row%s_supplier' % i]
                        item.delivery_time = request.POST['row%s_delivery_time' % i]
                        item.status = request.POST['row%s_status' % i]
                        
                        item.save()
                    else:
                        #creating new item
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
            # message about saving
            message = u'Заказ ID: %s обновлен.' % order.id
            order_items = OrderItem.objects.filter(order_id=order.id)
    else:
        order = Order.objects.get(id=id)
        order_items = OrderItem.objects.filter(order_id=order.id)
        form = OrderForm(instance=order)
        
    return direct_to_template(request, 'order_edit.html', {'form': form, 'message': message, 'order': order, 'order_items': order_items})


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
            supplier = Supplier.objects.get(id=int(request.POST['supplier']))
            
            # setting all products count for current supplier to 0
            beforeImport(supplier)
            
            rows_added = 0
            rows_updated = 0
            # adapting column numbers to xlrd: -1
            column_number = int(request.POST['column_number']) - 1
            column_brand = int(request.POST['column_brand']) - 1
            column_count = int(request.POST['column_count']) - 1
            column_price = int(request.POST['column_price']) - 1
            start_row = int(request.POST['start_row']) - 1
            # column_description optional
            if request.POST['column_description'] is not None:
                column_description = int(request.POST['column_description']) - 1
            
            currency = Currency.objects.get(id=int(request.POST['currency']))
            # opening file
            file_name = request.FILES['file']
            rb = xlrd.open_workbook(file_contents=file_name.read())
            sheet = rb.sheet_by_index(0)
            # going through rows in range
            for rownum in range(start_row, sheet.nrows):
                row = sheet.row_values(rownum)
                
                products = Product.objects.filter(code=row[column_number], supplier_id=supplier.id)
                
                if len(products) > 0:
                    product = products[0]
                    # updating model
                    product.brand = brand=row[column_brand]
                    product.description = row[column_description]
                    product.count = int(row[column_count])
                    product.price = Decimal(row[column_price])
                    
                    rows_updated += 1
                else:
                    # creating Model
                    product = Product(code=row[column_number], brand=row[column_brand],
                                      description=row[column_description], count=int(row[column_count]),
                                      price=Decimal(row[column_price]))           
                    
                    product.supplier = supplier
                    product.currency = currency
                    product.save()
                    
                    rows_added += 1
            # message
            message = u"Файл %s успешно импортирован. %s записей добавлено. %s записей обновлено." % (file_name, rows_added, rows_updated)
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

def beforeImport(supplier):
    products = Product.objects.filter(supplier_id=supplier.id)
    
    print products
    
    for product in products:
        product.count = 0;
        product.save()

def autocomplete_client_phone(request):
    if request.method == 'GET':
        GET = request.GET
        if GET.has_key('q'):
            q = request.GET.get( 'q' )
            results = Profile.objects.filter(phone__contains = q)
            matches = ""
            for result in results:
                matches = matches + "%s\n" % (result.phone)
            return HttpResponse(matches, mimetype="text/plain")

def autocomplete_code(request):
    if request.method == 'GET':
        GET = request.GET
        if GET.has_key('q'):
            q = request.GET.get( 'q' )
            results = Product.objects.filter(code__contains = q)
            matches = ""
            for result in results:
                matches = matches + "%s\n" % (result.code)
            return HttpResponse(matches, mimetype="text/plain")

def autocomplete_brand(request):
    if request.method == 'GET':
        GET = request.GET
        if GET.has_key('q'):
            q = request.GET.get( 'q' )
            results = Product.objects.filter(brand__contains = q)
            matches = ""
            for result in results:
                matches = matches + "%s\n" % (result.brand)
            return HttpResponse(matches, mimetype="text/plain")