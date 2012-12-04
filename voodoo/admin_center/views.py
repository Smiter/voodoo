# Create your views here.
from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template

def admin_center(request):
    #TODO add checking for super user
    if request.user.is_authenticated():
        return direct_to_template(request, 'admin_center.html')
    else:
        return HttpResponseRedirect('/admin_center/login/')

#def admin_center_login(request):
##    autentification
##    
#    return direct_to_template(request, 'login.html')