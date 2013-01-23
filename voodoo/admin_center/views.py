# encoding: UTF-8
from datetime import datetime
import time
from django.contrib.auth.decorators import login_required, user_passes_test,\
    permission_required
from django.views.generic.simple import direct_to_template
from voodoo.admin_center.models import Menu, Order, Product, Supplier, OrderItem
from voodoo.admin_center.forms import *
import xlrd
from django.contrib.auth.models import User
from voodoo.mainsite.models import Profile
from decimal import Decimal
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.core.serializers import serialize
from django.utils.simplejson import dumps, loads, JSONEncoder
#from django.db import models

@login_required(login_url='/admin_center/login/')
@permission_required('admin_center.view_admin_center', login_url='/admin_center/login/')
def admin_center(request):
    #TODO add checking for super user
    return direct_to_template(request, 'admin_center.html', {})


@login_required(login_url='/admin_center/login/')
@permission_required('admin_center.view_admin_center', login_url='/admin_center/login/')
def order_create(request):
    message = u''
    if request.method == 'POST':
        form = OrderForm(request.POST or None)

        if form.is_valid():
            # order_total_price1 = request.POST['total_sum_1']
            # order_total_price2 = request.POST['total_sum_2']
            
            # creating new Order
            order = form.save()
            
            saveItemsForOrder(request, order)
            
            # TODO if status is 'Отказ' отправляем письмо на указаный в профиле e-mail(номер заявки, номер запчасти и комментарий)
            # message about saving
            message = u'Заказ создан. ID: %s' % order.id
            
            # TODO forward with message if it possible
            return HttpResponseRedirect("order_edit/%s/" % order.id)
    else:
        form = OrderForm()
    return direct_to_template(request, 'order_create.html', {'form': form, 'message': message})

@login_required(login_url='/admin_center/login/')
@permission_required('admin_center.view_admin_center', login_url='/admin_center/login/')
def order_edit(request, id):
    message =''
    if request.method == 'POST':
        form = OrderForm(request.POST or None)
        
        if form.is_valid():
            # editing existing Order
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
            order.order_status = OrderStatus.objects.get(id=int(request.POST['order_status']))
            
            order.save()
            
            saveItemsForOrder(request, order)

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
@permission_required('admin_center.view_admin_center', login_url='/admin_center/login/')
def order_delete(request, id):
    if request.method == 'POST':
        order = Order.objects.get(id=id)
        order.delete()
        
    return HttpResponse('')

@login_required(login_url='/admin_center/login/')
@permission_required('admin_center.view_admin_center', login_url='/admin_center/login/')
def orders_management(request):
    #TODO
    message = ''
    # default results
    results = Order.objects.filter(order_status_id=1)
    if request.method == 'POST':
        form = OrdersManagementForm(request.POST or None)
        if form.is_valid():
            order_id = None
            order_status = None
            creation_date_after = None
            creation_date_before = None
            search_text = None
            search_where = None
            # TODO validating
            if request.POST["order_filter_number"] != '' :
                order_id = int(request.POST["order_filter_number"])
            
            if request.POST["order_filter_status"] != '' :
                order_status = int(request.POST["order_filter_status"])
                
            if request.POST["order_filter_creation_date_1"] != '' :
                creation_date_after = datetime.datetime.strptime(request.POST["order_filter_creation_date_1"] + " 00:00:00", '%d.%m.%Y %H:%M:%S')
                
            if request.POST["order_filter_creation_date_2"] != '' :
                creation_date_before = datetime.datetime.strptime(request.POST["order_filter_creation_date_2"] + " 23:59:59", '%d.%m.%Y %H:%M:%S')
                
            if request.POST["order_filter_text"] != '' :
                search_text = request.POST["order_filter_text"]
            
            results = Order.objects.all()
            
            if order_id is not None :
                results = results.filter(id=order_id)
            if order_status is not None:
                results = results.filter(order_status_id=order_status)
            if creation_date_after is not None:
                results = results.filter(creation_date__gte=creation_date_after)
            if creation_date_before is not None:
                results = results.filter(creation_date__lte=creation_date_before)
            #TODO Search text
                
            # message
            if results:
                message = 'Найдены следующие заказы(для полного просмотра выберите нужный в списке)'
            else:
                message = 'Ничего не найдено.'
    else:
        form = OrdersManagementForm()
    return direct_to_template(request, 'orders_management.html', {'form': form, 'results': results, 'message': message})

@login_required(login_url='/admin_center/login/')
@permission_required('admin_center.view_admin_center', login_url='/admin_center/login/')
def orders_import(request):
    results = OrderItem.objects.filter(order=None, cart__checked_out=True)
    return direct_to_template(request, 'orders_import.html', {'results': results})


@login_required(login_url='/admin_center/login/')
@permission_required('admin_center.view_admin_center', login_url='/admin_center/login/')
def orders_import_submit(request):
    detail_checkboxes = request.POST.getlist("detail_checkboxes[]")
    results = OrderItem.objects.filter(order=None, cart__checked_out=True)
    groups_by_client = {}
    for i in range(len(results)):
        if detail_checkboxes[i] == 'true':
            if results[i].user not in groups_by_client:
                groups_by_client[results[i].user] = [results[i]]
            else:
                groups_by_client[results[i].user].append(results[i])
    for user, list_of_items in groups_by_client.items():
        order = Order(user=user, order_status=OrderStatus.objects.get(status='Обработан'))
        order.order_info = "\n".join([item.product.brand + " " + str(item.count) for item in list_of_items])
        order.save()
        for item in list_of_items:
            item.order = order
            item.status = ItemStatus.objects.get(status=u'Оформлен')
            item.save()
    return HttpResponse('')


@login_required(login_url='/admin_center/login/')
@permission_required('admin_center.view_admin_center', login_url='/admin_center/login/')
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
@permission_required('admin_center.view_admin_center', login_url='/admin_center/login/')
def user_management(request):
    message = ''
    
    if request.method == 'POST':
        form = OrderForm(request.POST or None)
        
        # find filtered results 
    else:
        form = UserManagementForm()
        results = Profile.objects.all()
    
    return direct_to_template(request, 'user_management.html', {'form': form, 'message': message, 'results': results})

@login_required(login_url='/admin_center/login/')
@permission_required('admin_center.view_admin_center', login_url='/admin_center/login/')
def items_management(request):
    #TODO
    #filter
    message = ''
    results = None
    if request.method == 'POST':
        form = ItemsManagementForm(request.POST or None)
        if form.is_valid():
            order_id = None
            item_status = None
            added_after = None
            added_before = None
            supplier = None
            code = None
            
            # TODO validating to properly values
            if request.POST["order_id"] != '' :
                order_id = int(request.POST["order_id"])
                
            if request.POST["item_status"] != '' :
                item_status = request.POST["item_status"]
            
            if request.POST["added_after"] != '' :
                added_after = datetime.datetime.strptime(request.POST["added_after"] + " 00:00:00", '%d.%m.%Y %H:%M:%S')
                
            if request.POST["added_before"] != '' :
                added_before = datetime.datetime.strptime(request.POST["added_before"] + " 23:59:59", '%d.%m.%Y %H:%M:%S')
            
            if request.POST["supplier"] != '' :
                supplier = request.POST["supplier"]
                
            if request.POST["item_code"] != '' :
                code = request.POST["item_code"]
                    
            # Fetching results
            results = OrderItem.objects.all()
            if order_id is not None :
                results = results.filter(order_id=order_id)
            if item_status is not None:
                results = results.filter(status_id=item_status)
            if added_after is not None:
                results = results.filter(creation_date__gte=added_after)
            if added_before is not None:
                results = results.filter(creation_date__lte=added_before)
            if supplier is not None:
                results = results.filter(supplier_id=supplier)
            if code is not None:
                results = results.filter(code=code)
            # message
            if results:
                message = 'Найдены следующие запчасти...'
            else:
                message = 'Ничего не найдено.'
    else:
        form = ItemsManagementForm()
    return direct_to_template(request, 'items_management.html', {'form': form, 'results': results, 'message': message})

@login_required(login_url='/admin_center/login/')
@permission_required('admin_center.view_admin_center', login_url='/admin_center/login/')
def getMenuElements():
    menu_elements = Menu.getActiveElements(Menu())
    for element in menu_elements:
        # Was decided to use element.name instead of external configuration file or hard-code link inside DB
        element.link = element.name
    return menu_elements

def beforeImport(supplier):
    products = Product.objects.filter(supplier_id=supplier.id)
    
    for product in products:
        product.count = 0;
        product.save()

@login_required(login_url='/admin_center/login/')
@permission_required('admin_center.view_admin_center', login_url='/admin_center/login/')
def autocomplete_client_phone(request):
    if request.method == 'GET':
        GET = request.GET
        if GET.has_key('q'):
            q = request.GET.get( 'q' )
            results = Profile.objects.filter(phone__istartswith = q)
            matches = ""
            for result in results:
                matches = matches + "%s\n" % (result.phone)
            return HttpResponse(matches, mimetype="text/plain")

@login_required(login_url='/admin_center/login/')
@permission_required('admin_center.view_admin_center', login_url='/admin_center/login/')
def autocomplete_code(request):
    if request.method == 'GET':
        GET = request.GET
        if GET.has_key('q'):
            q = request.GET.get( 'q' )
            results = Product.objects.filter(code__icontains = q)
            matches = ""
            for result in results:
                matches = matches + "%s\n" % (result.code)
            return HttpResponse(matches, mimetype="text/plain")

@login_required(login_url='/admin_center/login/')
@permission_required('admin_center.view_admin_center', login_url='/admin_center/login/')
def autocomplete_brand(request):
    if request.method == 'GET':
        GET = request.GET
        if GET.has_key('q'):
            q = request.GET.get( 'q' )
            results = Product.objects.filter(brand__icontains = q)
            matches = ""
            for result in results:
                matches = matches + "%s\n" % (result.brand)
            return HttpResponse(matches, mimetype="text/plain")

@login_required(login_url='/admin_center/login/')
@permission_required('admin_center.view_admin_center', login_url='/admin_center/login/')
def item_edit(request):
    if request.method == 'POST':
        post_id = request.POST['id']
        post_value = request.POST['value']
        
        id = post_id.split('_')[2]
        field = post_id.split('_')[3]
        
        item = OrderItem.objects.get(id = id)
        
        if (field == 'code'):
            item.code = post_value
        if (field == 'brand'):
            item.brand = post_value
        if (field == 'comment'):
            item.comment = post_value
        if (field == 'price_1'):
            item.price_1 = post_value
        if (field == 'price_2'):
            item.price_2 = post_value
        if (field == 'currency'):
            item.currency = post_value
        if (field == 'count'):
            item.count = post_value
        if (field == 'delivery_time'):
            item.delivery_time = post_value
        if (field == 'status'):
            item.status = post_value
        
        item.save()
    return HttpResponse({post_value})

@login_required(login_url='/admin_center/login/')
@permission_required('admin_center.view_admin_center', login_url='/admin_center/login/')
def item_ajax_edit(request, id):
    if request.method == 'POST':
        item = OrderItem.objects.get(id = id)
        
        #TODO validation on server side
        
        item.code = request.POST['code']
        item.brand = request.POST['brand']
        item.comment = request.POST['comment']
        item.price_1 = make_decimal_from_string(request.POST['price_1'])
        item.price_2 = make_decimal_from_string(request.POST['price_2'])
        item.currency = request.POST['currency']
        item.count = request.POST['count']
        item.delivery_time = request.POST['delivery_time']
        item.status = ItemStatus.objects.get(status=request.POST['status'])
        
        item.save()
    
    return HttpResponse()

@login_required(login_url='/admin_center/login/')
@permission_required('admin_center.view_admin_center', login_url='/admin_center/login/')
def item_delete(request, id):
    if request.method == 'POST':
        item = OrderItem.objects.get(id=id)
        item.delete()
        
    return HttpResponse('')

@login_required(login_url='/admin_center/login/')
@permission_required('admin_center.view_admin_center', login_url='/admin_center/login/')
def feeds_currency(request):
    response_data = dict()
    currencyList = Currency.objects.all()
    if currencyList :
        for curr in currencyList :
            response_data[curr.code] = curr.code
        
    return HttpResponse(json.dumps(response_data), mimetype="application/json")

@login_required(login_url='/admin_center/login/')
@permission_required('admin_center.view_admin_center', login_url='/admin_center/login/')
def feeds_status(request):
    response_data = dict()
    statusList = ItemStatus.objects.all()
    if statusList :
        for status in statusList :
            response_data[status.status] = status.status
        
    return HttpResponse(json.dumps(response_data), mimetype="application/json")

def make_decimal_from_string(string):
    string = string.replace(",", ".")
    result = None
    try:
        result = Decimal(string)
    except:
        print "Can not cast string '%s' to Decimal" % string
    return result

def saveItemsForOrder(request, order):
    rowCount = int(request.POST['row_count'])
    for i in range(1, rowCount + 1):
        item = None
        id = request.POST['row%s_id' % i]
        code = request.POST['row%s_code' % i]
        brand = request.POST['row%s_brand' % i]
        comment = request.POST['row%s_comment' % i]
        price_1 = make_decimal_from_string(request.POST['row%s_price_1' % i])
        price_2 = make_decimal_from_string(request.POST['row%s_price_2' % i])
        currency = request.POST['row%s_currency' % i]
        count = request.POST['row%s_count' % i]
        supplier_id = request.POST['row%s_supplier' % i]
        delivery_time = request.POST['row%s_delivery_time' % i]
        status = ItemStatus.objects.get(status=request.POST['row%s_status' % i])
        # working only with rows where 'code' is not empty
        if (code):
            if id != '':
                try:
                    item = OrderItem.objects.get(id=id)
                except OrderItem.DoesNotExist:
                    print u"OrderItem с кодом '" + code + u"' не существует"
            if supplier_id:
                supplier = Supplier.objects.get(id=supplier_id)
            else:
                supplier = None
            if item is not None:
                # updating current item
                item.code = code
                item.brand = brand
                item.comment = comment
                item.price_1 = price_1
                item.price_2 = price_2
                item.currency = currency
                item.count = count
                item.supplier = supplier
                item.delivery_time = delivery_time
                item.status = status
                item.save()
            else:
                #creating new item
                item = OrderItem(order=order, code=code, brand=brand, comment=comment, price_1=price_1, price_2=price_2, 
                    currency=currency, count=count, supplier=supplier, delivery_time=delivery_time, status=status, product=None)
                item.save()
