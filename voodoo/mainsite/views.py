from django.http import *
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.views.generic.simple import direct_to_template
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import *
import json
from django.shortcuts import redirect
import logging


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
    if request.method == 'POST':
        if request.user.is_authenticated():
            form = NoticeOfPaymentForm(request.POST)
            if form.is_valid():
                success = True
                # form.save()
                notice = form.save(commit=False)
                notice.user = request.user
                notice.save()

                form = NoticeOfPaymentForm()
    else:
        form = NoticeOfPaymentForm()

    return render_to_response('notice_of_payment.html',
                               {'form': form, 'success': success}, context_instance=RequestContext(request))


def order_dispatch(request):
    success = False
    if request.method == 'POST':
        if request.user.is_authenticated():
            form = OrderDispatchForm(request.POST)
            if form.is_valid():
                success = True
                order = form.save(commit=False)
                order.user = request.user
                order.save()
                form = OrderDispatchForm()
    else:
        form = OrderDispatchForm()

    return render_to_response('order_dispatch.html',
                               {'form': form, 'success': success}, context_instance=RequestContext(request))


def sendings(request):
    form = SendingsForm()
    
    return render_to_response('sendings.html', {'form': form}, context_instance=RequestContext(request))