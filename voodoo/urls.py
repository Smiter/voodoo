#coding=utf-8

from django.conf.urls import patterns, include, url
from mainsite.views import *
from django.contrib import admin
admin.autodiscover()
from registration.models import RegistrationProfile
admin.site.unregister(RegistrationProfile)


urlpatterns = patterns('',
    ('^index/$', index),
    ('^login/$', login),
    (r'^admin/jsi18n/', 'django.views.i18n.javascript_catalog'),
    ('^notice_of_payment/$', notice_of_payment),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('voodoo.mainsite.RegistrationBackend.urls')),
)
