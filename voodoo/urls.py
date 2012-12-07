#coding=utf-8

from django.conf.urls import patterns, include, url
from mainsite.views import *
from russian_admin import admin
admin.autodiscover()
# from registration.models import RegistrationProfile
# admin.site.unregister(RegistrationProfile)
# from django.contrib import admin
js_info_dict = {'packages': ('django.conf', 'django.contrib.admin',), }


urlpatterns = patterns('',
    ('^index/$', index),
    ('^login/$', login),
    (r'^admin/jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),
    ('^notice_of_payment/$', notice_of_payment),
    ('^order_dispatch/$', order_dispatch),
    ('^sendings/$', sendings),
    ('^prepays/$', prepays),
    ('^vin_request/$', vin_request),
    ('^show_vin/$', show_vin),
    ('^get_vin_by_id/$', get_vin_by_id),
    # url(r'^captcha/', include('captcha.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin-tools/', include('admin_tools.urls')),
    (r'^accounts/', include('voodoo.mainsite.RegistrationBackend.urls')),
)
