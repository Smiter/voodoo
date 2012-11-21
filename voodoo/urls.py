#coding=utf-8

from django.conf.urls import patterns, include, url
from mainsite.views import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from registration.views import register
from mainsite.forms import UserRegistrationForm
from django.views.generic.simple import direct_to_template
from django.contrib.auth import views as auth_views
import regbackend

admin.autodiscover()

urlpatterns = patterns('', ('^signup/$', signup),
                      ('^index/$', index),
                      ('^login/$', login),
                       # url(r'^index/$',
                       #     auth_views.login,
                       #     {'template_name': 'index.html'},
                       #     name='auth_login'),


                       url(r'^accounts/register/$',
                           register,
                           {'backend': 'registration.backends.default.DefaultBackend',
                            'form_class': UserRegistrationForm
                            },
                           name='registration_register'),
                       # url(r'^logout/(?P<next_page>.*)/$', 'django.contrib.auth.views.logout', name='auth_logout_next'),
                       url(r'^admin/', include(admin.site.urls)),
                       (r'^accounts/', include('registration.backends.default.urls')),
                       )
