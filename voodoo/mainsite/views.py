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
            response_data['msg'] = "login successful"
            response_data['user'] = user.username
        else:
            response_data['msg'] = "disabled account"

    else:
        if not form.is_valid():
            response_data['msg'] = "invalid login"
            for field in form:
                if field.html_name:
                    if field.errors:
                        if field.html_name == 'username':
                            response_data['username_error'] = field.html_name + ' is requered.'

                        if field.html_name == 'password':
                            response_data['password_error'] = field.html_name + ' is requered.'

    return HttpResponse(json.dumps(response_data), mimetype="application/json")


def notice_of_payment(request):
    success = False
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/index')
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


def order_dispatch(request):
    success = False
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/index')

    profile = Profile.objects.get(user=request.user)
    initial = {"city_recipient": profile.city, "name_recipient": request.user.username}
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


def sendings(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/index')
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

    return render_to_response('sendings.html', {'form': form, 'result': result, 'error': error}, context_instance=RequestContext(request))


def prepays(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/index')
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


def vin_request(request):
    success = False
    import json
    
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/index')

    if request.method == 'POST':
        form = VinRequestForm(request.POST)
        if form.is_valid():
            success = True
            vin_request = form.save(commit=False)
            vin_request.user = request.user
            vin_request.save()
            for i in range(len(request.POST.getlist("details_name"))):
                vin_details = VinDetails(vin=vin_request,
                 name=request.POST.getlist("details_name")[i],
                 number=request.POST.getlist("details_number")[i])
                vin_details.save()
            
            for i in request.POST.getlist("car_additionals"):
                car_additional = CarAdditional(name=i)
                car_additional.save()
                vin_request.car_additionals.add(car_additional)
            form = VinRequestForm()
    else:
        form = VinRequestForm()

    return render_to_response('vin_request.html',
                               {'form': form, 'success': success}, context_instance=RequestContext(request))

    
def show_vin(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/index')
    result = None
    error = ''
    form = SendingsForm()
    if request.method == 'POST':
        form = SendingsForm(request.POST)
        if form.is_valid():
            try:
                min_date = datetime.strptime(request.POST["min_date"], '%d.%m.%Y').strftime('%Y-%m-%d')
                max_date = datetime.strptime(request.POST["max_date"], '%d.%m.%Y').strftime('%Y-%m-%d')
                # result = Prepays.objects.filter(user=request.user, date__range=(min_date, max_date))
            except:
                pass
                # result = Prepays.objects.filter(user=request.user, date__range=(request.POST["min_date"], request.POST["max_date"]))
            if not result:
                error = u'Ненайдено отправок удовлетворяющих фильтру поиска.'
    else:
        form = SendingsForm()

    return render_to_response('show_vin.html', {'form': form, 'result': result, 'error': error}, context_instance=RequestContext(request))