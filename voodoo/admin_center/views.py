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
from decimal import Decimal, InvalidOperation
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.core.serializers import serialize
from django.utils.simplejson import dumps, loads, JSONEncoder
from django.http import Http404
from django.forms.models import modelform_factory
from django.db.models.loading import get_model
from django.db.models import Q
import time
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
                search_where = request.POST["order_filter_order_part"]
            
            results = Order.objects.all()
            
            if order_id is not None :
                results = results.filter(id=order_id)
            if order_status is not None:
                results = results.filter(order_status_id=order_status)
            if creation_date_after is not None:
                results = results.filter(creation_date__gte=creation_date_after)
            if creation_date_before is not None:
                results = results.filter(creation_date__lte=creation_date_before)
            if search_text is not None:
                if search_where == u'Запчасти':
                    results = results.filter(orderitem__in=OrderItem.objects.filter(code=search_text))
                elif search_where == u'Клиенте':
                    results = results.filter(Q(client_name__icontains=search_text) | 
                                             Q(client_phone__icontains=search_text) | 
                                             Q(client_additional_information__icontains=search_text
                                            ))
                elif search_where == u'Авто':
                    results = results.filter(Q(car_brand__icontains=search_text) | 
                                             Q(car_vin__icontains=search_text) |
                                             Q(car_model__icontains=search_text) | 
                                             Q(car_engine__icontains=search_text) | 
                                             Q(car_year__icontains=search_text) | 
                                             Q(car_engine_size__icontains=search_text) | 
                                             Q(car_body__icontains=search_text) | 
                                             Q(car_gearbox__icontains=search_text) | 
                                             Q(car_additional_information__icontains=search_text
                                            ))
                elif search_where == u'Заказе':
                    #инфа о заказе. поле полная формулировка заказа
                    results = results.filter(Q(order_info__icontains=search_text) | 
                                             Q(order_additional_information__icontains=search_text))
    else:
        message = ''
        # default results
        order_creation_date_1_initial = datetime.datetime.combine(datetime.datetime.now().date() - datetime.timedelta(days=7), datetime.time.min)
        order_creation_date_2_initial = datetime.datetime.combine(datetime.datetime.now().date(), datetime.time.max)
        
        form = OrdersManagementForm(initial={'order_filter_creation_date_1': order_creation_date_1_initial, 'order_filter_creation_date_2': order_creation_date_2_initial })
        order_status_initial = form['order_filter_status'].field.initial
        
        results = Order.objects.filter(Q(order_status_id=order_status_initial) & 
                                       Q(creation_date__gte=order_creation_date_1_initial) & 
                                       Q(creation_date__lte=order_creation_date_2_initial))
    # message
    if results:
        message = 'Найдены следующие заказы(для полного просмотра выберите нужный в списке)'
    else:
        message = 'Ничего не найдено.'
        
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
        user_fio = u"Не зарегестрирован"
        user_phone = u""
        if user:
            try:
                profile = Profile.objects.get(user=user)
                user_fio = profile.fio
                user_phone = profile.phone
            except Profile.DoesNotExist:
                print u"User not found."
                
        order = Order(user=user, client_name=user_fio, client_phone=user_phone, order_status=OrderStatus.objects.get(status='Обработан'))
        order.order_info = "\n".join([item.product.brand + " " + str(item.count) for item in list_of_items])
        order.save()
        for item in list_of_items:
            item.order = order
            item.status = ItemStatus.objects.get(status=u'Оформлен')
            item.save()
    return HttpResponse('')


def readBrandFromRow(column_brand, row):
    result = row[column_brand]
    if type(result) is str:
        result.strip()
    return result

def readDescriptionFromRow(column_description, row):
    result = ''
    if column_description != None:
        result = row[column_description]
        if type(result) is str:
            result.strip()
    return result

def readCountFromRow(column_count, row):
    result = 1
    parsed_value = row[column_count]
    
    if type(parsed_value) is float:
        result = parsed_value
    else:
        if type(parsed_value) is str:
            try:
                count_string = row[column_count].strip().replace('<','').replace('>','')
                result = int(count_string)
            except ValueError:
                print "Can't cast" + row[column_count] + "to integer. Default value will be used."
    return result

def readPriceFromRow(column_price, row):
    result = 0
    
    try:
        result = Decimal(row[column_price])
    except InvalidOperation:
        print "Can't cast" + row[column_price] + "to Decimal. Default value will be used."
    return result

def readCodeFromRow(column_number, row):
    result = row[column_number]
    if type(result) is str:
        result.replace(' ','').replace('-','')
    return result

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
            column_description = None;
            if request.POST['column_description'] != '':
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
                    product.brand = readBrandFromRow(column_brand, row)
                    product.description = readDescriptionFromRow(column_description, row)
                    product.count = readCountFromRow(column_count, row)
                    product.price = readPriceFromRow(column_price, row)
                    
                    rows_updated += 1
                else:
                    parsed_code = readCodeFromRow(column_number, row)
                    if parsed_code != '':
                        # creating Model
                        product = Product(code=parsed_code, brand=readBrandFromRow(column_brand, row),
                                          description=readDescriptionFromRow(column_description, row), count=readCountFromRow(column_count, row),
                                          price=readPriceFromRow(column_price, row))           
                        
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
    if request.method == 'POST':
        form = ItemsManagementForm(request.POST or None)
        if form.is_valid():
            order_id = None
            item_status = None
            added_after = None
            added_before = None
            supplier = None
            code = None
            expired_items = False
            expired_date = None
            
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
            
            expired_items = form.cleaned_data['expired_items']
            expired_date = form.cleaned_data['expired_date']
                    
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
            if expired_items:
                expired_selected_date = datetime.datetime.combine(expired_date, datetime.datetime.now().time())
                results = OrderItem.objects.filter(Q(status_expired_date__lte=expired_selected_date) & Q(status=3))
            # message
            if results:
                message = 'Найдены следующие запчасти...'
            else:
                message = 'Ничего не найдено.'
    else:
        message = ''
        form = ItemsManagementForm()
        
        item_status_initial = form['item_status'].field.initial
        item_creation_date_1_initial = form['added_after'].field.initial
        item_creation_date_2_initial = form['added_before'].field.initial
        
        # default results
        results = OrderItem.objects.filter(Q(status_id=item_status_initial) & 
                                       Q(creation_date__gte=item_creation_date_1_initial) & 
                                       Q(creation_date__lte=item_creation_date_2_initial))
        
        # message
        if results:
            message = 'Найдены следующие заказы(для полного просмотра выберите нужный в списке)'
        else:
            message = 'Ничего не найдено.'
        
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
def autocomplete_client_name(request):
    if request.method == 'GET':
        GET = request.GET
        if GET.has_key('term'):
            q = request.GET.get( 'term' )
            orders = Order.objects.filter(client_name__istartswith = q).values('client_name').distinct()
            results = []
            for order in orders:
                results.append(order['client_name'])
            return HttpResponse(json.dumps(results), mimetype="text/plain")

@login_required(login_url='/admin_center/login/')
@permission_required('admin_center.view_admin_center', login_url='/admin_center/login/')
def autocomplete_client_login(request):
    if request.method == 'GET':
        GET = request.GET
        if GET.has_key('term'):
            q = request.GET.get( 'term' )
            
            users = User.objects.filter(username__istartswith = q).values('username')
            results = []
            for user in users:
                results.append(user['username'])
                
            return HttpResponse(json.dumps(results), mimetype="text/plain")

@login_required(login_url='/admin_center/login/')
@permission_required('admin_center.view_admin_center', login_url='/admin_center/login/')
def autocomplete_client_phone(request, client):
    if request.method == 'GET':
        GET = request.GET
        if GET.has_key('term'):
            q = request.GET.get( 'term' )
            orders = Order.objects.filter(client_name = client, client_phone__istartswith = q).values('client_phone').distinct()
            results = []
            for order in orders:
                results.append(order['client_phone'])
            return HttpResponse(json.dumps(results), mimetype="text/plain")

@login_required(login_url='/admin_center/login/')
@permission_required('admin_center.view_admin_center', login_url='/admin_center/login/')
def autocomplete_client_latest_phone(request):
    if request.method == 'GET':
        GET = request.GET
        if GET.has_key('client'):
            response = ""
            client = request.GET.get( 'client' )
            results = Order.objects.filter(client_name = client).order_by('creation_date')
            if results:
                response = results[len(results) - 1].client_phone
            return HttpResponse(response, mimetype="text/plain")
            

@login_required(login_url='/admin_center/login/')
@permission_required('admin_center.view_admin_center', login_url='/admin_center/login/')
def autocomplete_code(request):
    if request.method == 'GET':
        GET = request.GET
        if GET.has_key('term'):
            q = request.GET.get( 'term' )
            products = Product.objects.filter(code__icontains = q)[:10]
            results = []
            for product in products:
                results.append(product.code)
            return HttpResponse(json.dumps(results), mimetype="text/plain")

@login_required(login_url='/admin_center/login/')
@permission_required('admin_center.view_admin_center', login_url='/admin_center/login/')
def autocomplete_brand(request):
    if request.method == 'GET':
        GET = request.GET
        if GET.has_key('term'):
            q = request.GET.get( 'term' )
            products = Product.objects.filter(brand__icontains = q).values('brand').distinct()[:10]
            results = []
            for product in products:
                results.append(product['brand'])
            return HttpResponse(json.dumps(results), mimetype="text/plain")

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
        try:
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
                supplier = None
                status_expired_date = None
                if supplier_id:
                    supplier = Supplier.objects.get(id=supplier_id)
                    
                    if status.status == u'Заказан':
                        status_expired_date = datetime.datetime.now() + datetime.timedelta(hours=float(supplier.time_out))
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
                    
                    item_edited = item.status != status
                    if (item_edited ):
                        new_status_is_ordered = status.status == u'Заказан'
                        if new_status_is_ordered:
                            item.status_expired_date = status_expired_date
                        else:
                            item.status_expired_date = None
                    item.status = status
                        
                    item.save()
                else:
                    #creating new item
                    item = OrderItem(order=order, code=code, brand=brand, comment=comment, price_1=price_1, price_2=price_2, 
                        currency=currency, count=count, supplier=supplier, delivery_time=delivery_time, status=status, product=None, status_expired_date=status_expired_date)
                    item.save()
        except:
            print u'Order Item with id:%s skipped' % i


@login_required(login_url='/admin_center/login/')
@permission_required('admin_center.view_admin_center', login_url='/admin_center/login/')
def suppliers_list(request):
    results = Supplier.objects.all()
    return direct_to_template(request, 'suppliers_list.html', {'results': results})


@login_required(login_url='/admin_center/login/')
@permission_required('admin_center.view_admin_center', login_url='/admin_center/login/')
def delete_model(request, modelname, id):
    if request.method == 'POST':
        Model = get_model('admin_center', modelname)
        if not Model:
            Model = get_model('mainsite', modelname)
        if not Model:
            raise Http404
        model = Model.objects.get(id=id)
        model.delete()
    return HttpResponse('')


@login_required(login_url='/admin_center/login/')
@permission_required('admin_center.view_admin_center', login_url='/admin_center/login/')
def edit_model(request, modelname, id):
    Model = get_model('admin_center', modelname)
    if not Model:
        Model = get_model('mainsite', modelname)
        if not Model:
            raise Http404
    if id == "add":
        model = Model()
        title = 'Добавить: ' + model._meta.verbose_name
    else:
        try:
            model = Model.objects.get(id=id)
        except Model.DoesNotExist:
            raise Http404
        title = 'Редактировать: ' + model._meta.verbose_name
    Form = modelform_factory(Model)
    if request.method == 'POST':
        form = Form(request.POST, instance=model)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.session['return_url'])
    else:
        request.session['return_url'] = request.GET['return_url']
        form = Form(instance=model)

    form.required_css_class = 'required'
    return direct_to_template(request, 'edit_model.html', {'form': form, 'id': id, 'title': title, 'modelname': modelname})

@login_required(login_url='/admin_center/login/')
@permission_required('admin_center.view_admin_center', login_url='/admin_center/login/')
def order_print(request, id):
    message =''
    order = Order.objects.get(id=id)
    order_items = OrderItem.objects.filter(order_id=order.id)
        
    return direct_to_template(request, 'order_print.html', {'message': message, 'order': order, 'order_items': order_items})

@login_required(login_url='/admin_center/login/')
@permission_required('admin_center.view_admin_center', login_url='/admin_center/login/')
def shipment_create(request):
    message = ''
    form = ShipmentForm()
    
    if request.method == 'POST':
        form = ShipmentForm(request.POST or None)
        
        if form.is_valid():
            shipment = form.save(commit=False)
            
            if 'for_client' in request.POST:
                shipment.type = ShipmentType.objects.get(code = 'for_client')
            if 'from_client' in request.POST:
                shipment.type = ShipmentType.objects.get(code = 'from_client')
            if 'from_supplier' in request.POST:
                shipment.type = ShipmentType.objects.get(code = 'from_supplier')
            if 'returning' in request.POST:
                shipment.type = ShipmentType.objects.get(code = 'returning')
            
            shipment.save()
            print shipment
            message = u'Отправка создана. ID: %s' % shipment.id
            
    return direct_to_template(request, 'shipment_create.html', {'form': form, 'message': message})