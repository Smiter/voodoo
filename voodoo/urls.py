#coding=utf-8

from django.contrib.auth import views as auth_views
from django.conf.urls import patterns, include, url
from mainsite.views import *
from russian_admin import admin
from voodoo.admin_center.views import *
from mainsite.basket.views import *
admin.autodiscover()
# from registration.models import RegistrationProfile
# admin.site.unregister(RegistrationProfile)
# from django.contrib import admin
js_info_dict = {'packages': ('django.conf', 'django.contrib.admin',), }


urlpatterns = patterns('',
    ('^$', index),
    ('^login/$', login),
    (r'^admin/jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),
    ('^notice_of_payment/$', notice_of_payment),
    ('^order_dispatch/$', order_dispatch),
    ('^sendings/$', sendings),
    ('^prepays/$', prepays),
    ('^vin_request/$', vin_request),
    ('^show_vin/$', show_vin),
    ('^get_vin_by_id/$', get_vin_by_id),
    ('^save_del_details/$', save_del_details),
    ('^order_details/$', order_details),
    ('^basket/$', get_basket),
    ('^add_to_cart/$', add_to_cart),
    ('^update_basket/$', update_basket),
    ('^del_item/$', del_item),
    ('^orders/$', orders),
    ('^make_order/$', make_order),
    ('^search_product/$', search_product),
    # ('^catalog/$', catalog),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin-tools/', include('admin_tools.urls')),
    (r'^accounts/', include('voodoo.mainsite.RegistrationBackend.urls')),
    (r'^admin_center/service/', include('voodoo.admin_center.dhtmlScheduler.urls')),
    # operation center
    ('^admin_center/$', admin_center),
    url(r'^admin_center/login/$', auth_views.login, {'template_name': 'admin_login.html'}, name='auth_login'),
    ('^admin_center/order_create$', order_create),
    ('^admin_center/orders_import$', orders_import),
    ('^admin_center/order_edit/(?P<id>\d+)/$', order_edit),
    ('^admin_center/orders_management$', orders_management),
    ('^admin_center/xls_import$', xls_import),
    ('^admin_center/user_management$', user_management),
    (r'^admin_center/autocomplete_client_phone/$', autocomplete_client_phone),
    (r'^admin_center/autocomplete_code/$', autocomplete_code),
    (r'^admin_center/autocomplete_brand/$', autocomplete_brand),
    ('^admin_center/items_management$', items_management),
    
#    ('^admin_center/service$', include('voodoo.admin_center.dhtmlScheduler.urls')),

)