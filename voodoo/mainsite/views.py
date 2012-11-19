from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from forms import SignupForm

# @login_required
def index(request):
    return render_to_response('index.html')


def signup(request):
    if request.method == 'POST':
        form = SignupForm()
        return render_to_response('signup.html', {'form': form})
    else:
        form = SignupForm()    
        return render_to_response('signup.html', {'form': form})
