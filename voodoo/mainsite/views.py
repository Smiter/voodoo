#coding=utf-8

from django.http import *
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.views.generic.simple import direct_to_template
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import *
from django.db import models
import json
from django.shortcuts import redirect
import logging
from datetime import datetime
from django.core.serializers import serialize
from django.utils.simplejson import dumps, loads, JSONEncoder
from django.db.models.query import QuerySet
from django.contrib.auth.decorators import login_required


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


@login_required(login_url='/index')
def notice_of_payment(request):
    success = False
    if request.method == 'POST':
        form = PrepaysForm(request.POST)
        if form.is_valid():
            success = True
            # form.save()
            notice = form.save(commit=False)
            notice.user = request.user
            notice.save()

            form = PrepaysForm()
    else:
        form = PrepaysForm()

    return render_to_response('notice_of_payment.html',
                               {'form': form, 'success': success}, context_instance=RequestContext(request))


@login_required(login_url='/index')
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
            form = OrderDispatchForm(initial=initial)
    else:
        form = OrderDispatchForm(initial=initial)

    return render_to_response('order_dispatch.html',
                               {'form': form, 'success': success}, context_instance=RequestContext(request))


@login_required(login_url='/index')
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
                error = u'Ненайдено отправок удовлетворяющих фильтру поиска.'
    else:
        form = SendingsForm()

    return render_to_response('sendings.html', {'form': form, 'layout':"inline", 'result': result, 'error': error}, context_instance=RequestContext(request))


@login_required(login_url='/index')
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
                error = u'Ненайдено отправок удовлетворяющих фильтру поиска.'
    else:
        form = SendingsForm()

    return render_to_response('prepays.html', {'form': form, 'result': result, 'error': error}, context_instance=RequestContext(request))


# @login_required(login_url='/index')
def vin_request(request):
    success = False

    if request.method == 'POST':
        if not request.user.is_authenticated():
            form = getVinRequestForm((), request.POST)
        else:
            form = getVinRequestForm(('client_name', 'client_phone', 'client_code', 'client_additional_information', 'email', 'delivery_adress'), request.POST)
        # form = VinRequestForm(request.POST)
        if form.is_valid():
            print request.POST
            success = True
            vin_request = form.save(commit=False)
            if request.user.is_authenticated():
                vin_request.user = request.user
            vin_request.car_additional_information = ",".join(request.POST.getlist("car_additional_information"))
            details = ""
            for i in range(len(request.POST.getlist("details_name"))):
                details_name = request.POST.getlist("details_name")[i]
                details_number = request.POST.getlist("details_number")[i]
                print "------------"
                print details_name
                print details_number
                if details_name != "" and details_number != "":
                    details = details + details_name + ', ' + details_number + ' sh.;'
                    print details
            vin_request.order_info = details
            vin_request.save()
            if not request.user.is_authenticated():
                form = getVinRequestForm(())
            else:
                form = getVinRequestForm(('client_name', 'client_phone', 'client_code', 'client_additional_information', 'email', 'delivery_adress'))
    else:
        if not request.user.is_authenticated():
            form = getVinRequestForm(())
        else:
            form = getVinRequestForm(('client_name', 'client_phone', 'client_code', 'client_additional_information', 'email', 'delivery_adress'))

    return render_to_response('vin_request.html',
                               {'form': form, 'success': success}, context_instance=RequestContext(request))


@login_required(login_url='/index')
def show_vin(request):
    result = None
    error = ''
    form = SendingsForm()
    if request.method == 'POST':
        form = SendingsForm(request.POST)
        
        if form.is_valid():
            try:
                min_date = datetime.strptime(request.POST["min_date"], '%d.%m.%Y').strftime('%Y-%m-%d') + ' 00:00:01'
                max_date = datetime.strptime(request.POST["max_date"], '%d.%m.%Y').strftime('%Y-%m-%d') + ' 23:59:00'
                result = VinRequest.objects.filter(user=request.user, date__range=(min_date, max_date))
            except:
                result = VinRequest.objects.filter(user=request.user, date__range=(request.POST["min_date"] + ' 00:00:01', request.POST["max_date"] + ' 23:59:00'))
            if not result:
                error = u'Ненайдено отправок удовлетворяющих фильтру поиска.'
    else:
        form = SendingsForm()

    return render_to_response('show_vin.html', {'form': form, 'result': result, 'error': error}, context_instance=RequestContext(request))


@login_required(login_url='/index')
def get_vin_by_id(request):
    print "get_vin_by_id"
    vin_request = VinRequest.objects.filter(user=request.user,
        id=request.POST["vin_id"])
    vin_details = VinDetails.objects.filter(vin=vin_request)
    data = {'vin_request': vin_request, 'vin_details': vin_details}
    output = dumps(data, cls=DjangoJSONEncoder)
    return HttpResponse(output, mimetype="application/json")


@login_required(login_url='/index')
def save_del_details(request):
    print "\nsave_details\n"
    if request.method == 'POST':
        vin_details = VinDetails.objects.filter(vin=VinRequest(id=request.POST["vin_id"]))
        for i in range(len(request.POST.getlist("details_name[]"))):
            name = request.POST.getlist("details_name[]")[i]
            number = request.POST.getlist("details_number[]")[i]
            if i < len(vin_details):
                vin_details[i].name = name
                vin_details[i].number = number
                vin_details[i].save()
            else:
                vin_detail = VinDetails(vin=VinRequest(id=request.POST["vin_id"]),
                 name=name,
                 number=number)
                vin_detail.save()

        for i in range(len(request.POST.getlist("details_name[]")), len(vin_details)):
            vin_details[i].delete()

    return HttpResponse('')


def order_details(request):
    print "\norder_details\n"
    return HttpResponse('')


@login_required(login_url='/index')
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
                result = Order.objects.filter(user=request.user, order_time__range=(min_date, max_date))
            except:
                print request.POST
                if request.POST["status"] == u'Все':
                    result = Order.objects.filter(user=request.user, order_time__range=(request.POST["min_date"] + ' 00:00:01', request.POST["max_date"] + ' 23:59:00'))
                else:
                    result = Order.objects.filter(user=request.user, status=request.POST["status"], order_time__range=(request.POST["min_date"] + ' 00:00:01', request.POST["max_date"] + ' 23:59:00'))
            # print result[0].items.all()[0].product.name
            if not result:
                error = u'Ненайдено отправок удовлетворяющих фильтру поиска.'
    else:
        form = OrdersForm()
    
    return render_to_response('orders.html', {'form': form, 'result': result, 'error': error}, context_instance=RequestContext(request))


def catalog(request):
    return render_to_response('catalog.html',  dict(products=Product.objects.all()), context_instance=RequestContext(request))

