from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.core.urlresolvers import reverse
from forms import SignupForm
import logging
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.views.generic.simple import direct_to_template
from django.contrib.auth.forms import AuthenticationForm
import json


# @login_required


def index(request):
    # logging.error(request.errors)
    return direct_to_template(request, 'index.html')


def signup(request):
    if request.method == 'POST':
        form = SignupForm()
        return render_to_response('signup.html', {'form': form})
    else:
        form = SignupForm()
        return render_to_response('signup.html', {'form': form})


def login(request):
    msg = []
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
            msg.append("login successful")
            response_data['user'] = user.username

            # return HttpResponseRedirect('/index')
            # return direct_to_template(request, 'index.html')
        else:
            msg.append("disabled account")

    else:
        if not form.is_valid():
            msg.append("invalid login")
            for field in form:
                if field.html_name:
                    if field.errors:
                        if field.html_name == 'username':
                            response_data['username_error'] = field.html_name + ' is requered.'

                        if field.html_name == 'password':
                            response_data['password_error'] = field.html_name + ' is requered.'

    response_data['msg'] = msg
    return HttpResponse(json.dumps(response_data), mimetype="application/json")
