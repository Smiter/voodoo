# encoding: UTF-8
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template
from voodoo.admin_center.models import Menu, Order, Product, Supplier, OrderItem
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
    #TODO get rid of this hard-code
    currencyList = [u"UAH", u"USD", u"EUR"]
    #TODO Сообщен (черный цвет), Оформлен (оранжевый), Заказан (зеленый), Доставлен (синий), Отказ (красный)
    # also need to add ORDER and COLOR
    statusList = [u"Сообщен", u"Оформлен", u"Заказан", u"Доставлен", u"Отказ"]
    suppliersList = Supplier.objects.all()
    message = ''
    if request.method == 'POST':
        form = OrderForm(request.POST or None)
        # TODO validating
        # JS validation
        # rowCount = int(request.POST['row_count'])
        # TODO use OrderStatus, ItemStatus, Currency models

        if form.is_valid():
            client_name = form.cleaned_data['client_name']
            client_phone = form.cleaned_data['client_phone']
            client_code = form.cleaned_data['client_code']
            client_additional_information = form.cleaned_data['client_additional_information']
            car_brand = form.cleaned_data['car_brand']
            car_vin = form.cleaned_data['car_vin']
            car_model = form.cleaned_data['car_model']
            car_engine = form.cleaned_data['car_engine']
            car_year = form.cleaned_data['car_year']
            car_engine_size = form.cleaned_data['car_engine_size']
            car_body = form.cleaned_data['car_body']
            car_gearbox = form.cleaned_data['car_gearbox']
            car_additional_information = form.cleaned_data['car_additional_information']
            order_info = form.cleaned_data['order_info']
            order_additional_information = form.cleaned_data['order_additional_information']
            order_status = form.cleaned_data['order_status']
            # TODO is it necessary ?
            # if yes - use form.cleaned_data
            # order_total_price1 = request.POST['total_sum_1']
            # order_total_price2 = request.POST['total_sum_2']
            order = Order(client_name=client_name, client_phone=client_phone, client_code=client_code, client_additional_information=client_additional_information,
                          car_brand=car_brand, car_vin=car_vin, car_model=car_model, car_engine=car_engine, car_year=car_year, car_engine_size=car_engine_size,
                          car_body=car_body, car_gearbox=car_gearbox, car_additional_information=car_additional_information,
                          order_info=order_info, order_additional_information=order_additional_information, order_status=order_status)
            order.save()
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
                item = OrderItem(order=order, code=code, brand=brand, comment=comment, price_1=price_1, price_2=price_2,
                                 currency=currency, count=count, supplier=supplier, delivery_time=delivery_time, status=status)
                item.save()
            # message about saving
            message = 'Заказ создан. ID: %s' % order.id
            # TODO if status is 'Отказ' отправляем письмо на указаный в профиле e-mail(номер заявки, номер запчасти и комментарий)
            form = OrderForm()
    else:
        form = OrderForm()
    return direct_to_template(request, 'order_create.html', {'menu_elements': getMenuElements(),
                                                             'form': form, 'currencyList': currencyList,
                                                             'suppliersList': suppliersList, 'statusList': statusList, 'message': message})


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
    return direct_to_template(request, 'orders_management.html', {'menu_elements': getMenuElements(), 'form': form, 'results': results, 'message': message})


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
    return direct_to_template(request, 'order_edit.html', {'menu_elements': getMenuElements(), 'form': form})


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
                                  price=[column_price])
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
    form = TestForm(request.POST)
    print 'initial enter'
    if form.is_valid():
        print 'form is valid'
    return direct_to_template(request, 'test.html', {'menu_elements': getMenuElements(), 'form': form})
