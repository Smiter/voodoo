#coding=utf-8

from django.http import *
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.views.generic.simple import direct_to_template
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import *
import json
from datetime import datetime
from django.core.serializers import serialize
from django.utils.simplejson import dumps, loads, JSONEncoder
from django.db.models.query import QuerySet
from django.contrib.auth.decorators import login_required
from voodoo.admin_center.models import Product, OrderItem, OrderStatus, ItemStatus


class DjangoJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, QuerySet):
            return loads(serialize('json', obj, use_natural_keys=True))
        return JSONEncoder.default(self, obj)


def index(request):
    return direct_to_template(request, 'index.html')


def login(request):
    response_data = dict()
    response_data['username_error'] = ''
    response_data['password_error'] = ''
    username = request.POST['username']
    password = request.POST['password']
    form = AuthenticationForm(data=request.POST)
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            response_data['user'] = user.username
        else:
            response_data['msg'] = "disabled account"
    else:
        if not form.is_valid():
            response_data['msg'] = "invalid login"
    return HttpResponse(json.dumps(response_data), mimetype="application/json")


@login_required(login_url='/')
def notice_of_payment(request):
    success = False
    if request.method == 'POST':
        form = PrepaysForm(request.POST)
        if form.is_valid():
            success = True
            notice = form.save(commit=False)
            notice.user = request.user
            notice.save()
            return HttpResponseRedirect("/notice_of_payment/")
    else:
        form = PrepaysForm()

    return render_to_response('notice_of_payment.html',
                               {'form': form, 'success': success}, context_instance=RequestContext(request))


@login_required(login_url='/')
def order_dispatch(request):
    success = False
    profile = None
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None
    initial = {"city_recipient": profile.city if profile else "", "name_recipient": request.user.username}
    if request.method == 'POST':
        form = OrderDispatchForm(request.POST)
        if form.is_valid():
            success = True
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            return HttpResponseRedirect("/order_dispatch/")
    else:
        form = OrderDispatchForm(initial=initial)

    return render_to_response('order_dispatch.html',
                               {'form': form, 'success': success}, context_instance=RequestContext(request))


@login_required(login_url='/')
def sendings(request):
    result = None
    error = ''
    form = SendingsForm()
    if request.method == 'POST':
        form = SendingsForm(request.POST)
        if form.is_valid():
            try:
                min_date = datetime.strptime(request.POST["min_date"], '%d.%m.%Y').strftime('%Y-%m-%d')
                max_date = datetime.strptime(request.POST["max_date"], '%d.%m.%Y').strftime('%Y-%m-%d')
                result = Sendings.objects.filter(user=request.user, date__range=(min_date, max_date))
            except:
                result = Sendings.objects.filter(user=request.user, date__range=(request.POST["min_date"], request.POST["max_date"]))

            if not result:
                error = u'Не найдено отправок удовлетворяющих фильтру поиска.'
    else:
        form = SendingsForm()
    return render_to_response('sendings.html', {'form': form, 'layout': "inline", 'result': result, 'error': error}, context_instance=RequestContext(request))


@login_required(login_url='/')
def prepays(request):
    result = None
    error = ''
    form = SendingsForm()
    if request.method == 'POST':
        form = SendingsForm(request.POST)
        if form.is_valid():
            try:
                min_date = datetime.strptime(request.POST["min_date"], '%d.%m.%Y').strftime('%Y-%m-%d')
                max_date = datetime.strptime(request.POST["max_date"], '%d.%m.%Y').strftime('%Y-%m-%d')
                result = Prepays.objects.filter(user=request.user, date__range=(min_date, max_date))
            except:
                result = Prepays.objects.filter(user=request.user, date__range=(request.POST["min_date"], request.POST["max_date"]))
            if not result:
                error = u'Не найдено проплат удовлетворяющих фильтру поиска.'
    else:
        form = SendingsForm()
    return render_to_response('prepays.html', {'form': form, 'result': result, 'error': error}, context_instance=RequestContext(request))


# @login_required(login_url='/index')
def vin_request(request):
    success = False

    if request.method == 'POST':
        if not request.user.is_authenticated():
            form = getVinRequestForm(('car_engine', 'car_engine_size'), request.POST)
            del form.fields['car_additional_information']
        else:
            form = getVinRequestForm(('client_name', 'client_phone', 'email'), request.POST)
        if form.is_valid():
            success = True
            order = form.save(commit=False)
            if request.user.is_authenticated():
                order.user = request.user
            order.car_additional_information = ",".join(request.POST.getlist("car_additional_information"))
            details = []
            for i in range(len(request.POST.getlist("details_name"))):
                details_name = request.POST.getlist("details_name")[i]
                details_number = request.POST.getlist("details_number")[i]
                if details_name != "" and details_number != "":
                    details.append(details_name + ' ' + details_number)
            order.order_info = "\n".join(details)
            order.order_status = OrderStatus.objects.get(status='Принят')
            if not request.user.is_authenticated():
                order.client_name = u'Не зарегистрирован, ' + request.POST["client_name"]
            order.save()
            vin_request = VinRequest(order=order)
            vin_request.save()
            return HttpResponseRedirect("/vin_request/")
    else:
        if not request.user.is_authenticated():
            form = getVinRequestForm(('car_engine', 'car_engine_size'))
            del form.fields['car_additional_information']
        else:
            form = getVinRequestForm(('client_name', 'client_phone', 'email'))

    return render_to_response('vin_request.html',
                               {'form': form, 'success': success}, context_instance=RequestContext(request))


@login_required(login_url='/')
def show_vin(request):
    result = None
    error = ''
    if request.method == 'POST':
        form = SendingsForm(request.POST)
        if form.is_valid():
            try:
                min_date = datetime.strptime(request.POST["min_date"], '%d.%m.%Y').strftime('%Y-%m-%d') + ' 00:00:01'
                max_date = datetime.strptime(request.POST["max_date"], '%d.%m.%Y').strftime('%Y-%m-%d') + ' 23:59:00'
                result = Order.objects.filter(user=request.user, creation_date__range=(min_date, max_date))
            except:
                result = VinRequest.objects.filter(order__in=Order.objects.filter(user=request.user,
                    creation_date__range=(request.POST["min_date"] + ' 00:00:01',
                                          request.POST["max_date"] + ' 23:59:00')))
            if not result:
                error = u'Не найдено подборов удовлетворяющих фильтру поиска.'
    else:
        form = SendingsForm()
    return render_to_response('show_vin.html', {'form': form, 'result': result, 'error': error}, context_instance=RequestContext(request))


@login_required(login_url='/')
def get_vin_by_id(request):
    print "get_vin_by_id"
    order = Order.objects.filter(id=request.POST["vin_id"])
    vin_details = OrderItem.objects.filter(order=order)
    data = {'vin_request': order, 'vin_details': vin_details, 'vin_request_id': order[0].vinrequest_set.all()[0].id}
    output = dumps(data, cls=DjangoJSONEncoder)
    return HttpResponse(output, mimetype="application/json")


@login_required(login_url='/')
def save_del_details(request):
    if request.method == 'POST':
        vin_request = Order.objects.filter(user=request.user, id=request.POST["vin_id"])[0]
        vin_details = vin_request.order_info.split(";")
        # vin_details.pop()
        for i in range(len(request.POST.getlist("details_name[]"))):
            name = request.POST.getlist("details_name[]")[i]
            number = request.POST.getlist("details_number[]")[i]
            if i < len(vin_details):
                vin_details[i] = name + " " + number + "\n"
            else:
                vin_details.append(name + " " + number + "\n")
        for i in range(len(request.POST.getlist("details_name[]")), len(vin_details)):
            del vin_details[i]
        vin_request.order_info = " ".join(vin_details)
        vin_request.save()
    return HttpResponse('')


def order_details(request):
    detail_count_list = request.POST.getlist("num_offered_detail[]")
    detail_status_list = request.POST.getlist("statuses[]")
    order = Order.objects.filter(id=request.POST["vin_id"])
    order_details = OrderItem.objects.filter(order=order)
    for i in range(len(order_details)):
        order_details[i].count = detail_count_list[i]
        if detail_status_list[i] == 'true':
            order_details[i].status = ItemStatus.objects.get(status=u'Оформлен')
        else:
            order_details[i].status = ItemStatus.objects.get(status=u'Сообщен')
        order_details[i].save()
    return HttpResponse('')


@login_required(login_url='/')
def orders(request):
    result = None
    error = ''
    form = OrdersForm()
    if request.method == 'POST':
        form = OrdersForm(request.POST)
        if form.is_valid():
            try:
                min_date = datetime.strptime(request.POST["min_date"], '%d.%m.%Y').strftime('%Y-%m-%d') + ' 00:00:01'
                max_date = datetime.strptime(request.POST["max_date"], '%d.%m.%Y').strftime('%Y-%m-%d') + ' 23:59:00'
                result = OrderItem.objects.filter(user=request.user, creation_date__range=(min_date, max_date))
            except:
                status = request.POST["status"]
                if status == u'Все':
                    result = OrderItem.objects.filter(user=request.user, creation_date__range=(request.POST["min_date"] + ' 00:00:01', request.POST["max_date"] + ' 23:59:00'))
                else:
                    if status == u'Принят':
                        status = u'Сообщен'
                        result = OrderItem.objects.filter(status=ItemStatus.objects.get(status=status))
                    elif status == u'Заказан':
                        result = OrderItem.objects.filter(status__in=[ItemStatus.objects.get(status=u'Заказан'), ItemStatus.objects.get(status=u'Оформлен')])
                    else:
                        result = OrderItem.objects.filter(status=ItemStatus.objects.get(status=status))
            if not result:
                error = u'Не найдено заказов удовлетворяющих фильтру поиска.'
    else:
        form = OrdersForm()
    return render_to_response('orders.html', {'form': form, 'result': result, 'error': error}, context_instance=RequestContext(request))


def search_product(request):
    print "SEARCH"
    detail_code = request.GET['detail_id']
    if request.user.is_authenticated():
        profile = Profile.objects.get(user=request.user)
        discount = profile.discount_group.discount
    else:
        discount = 0
    if detail_code == "":
        result = None
    else:
        result = Product.objects.filter(code__icontains=detail_code.replace('-', '').replace(' ', ''))
    return render_to_response('search.html',  dict(result=result, discount=discount, detail_id=request.GET['detail_id'], error=u'Ничего не найдено.'), context_instance=RequestContext(request))