#coding=utf-8

from django.contrib.auth import views as auth_views
from django.conf.urls import patterns, include, url
from mainsite.views import *
from russian_admin import admin
from voodoo.admin_center.views import *
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
    # url(r'^captcha/', include('captcha.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin-tools/', include('admin_tools.urls')),
    (r'^accounts/', include('voodoo.mainsite.RegistrationBackend.urls')),
    # operation center
    ('^admin_center/$', admin_center),
#    ('^admin_center_login/$', admin_center_login),
    url(r'^admin_center/login/$', auth_views.login, {'template_name': 'login.html'}, name='auth_login'),
)
