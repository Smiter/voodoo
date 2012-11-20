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
    username = request.POST['username']
    password = request.POST['password']
    logging.error(username)
    logging.error(password)
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            msg.append("login successful")
            # return HttpResponseRedirect('/index')
            # return direct_to_template(request, 'index.html')
        else:
            msg.append("disabled account")
            
    else:
            msg.append("invalid login")

    return HttpResponse(msg)