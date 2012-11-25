from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.views.generic.simple import direct_to_template
from django.contrib.auth.forms import AuthenticationForm
import json


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
