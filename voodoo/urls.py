#coding=utf-8

from django.contrib.auth import views as auth_views
from django.conf.urls import patterns, include, url
from mainsite.views import *
from voodoo.admin_center.views import *
from mainsite.basket.views import *
# from registration.models import RegistrationProfile
# admin.site.unregister(RegistrationProfile)
from django.contrib import admin
from django.views.generic.simple import direct_to_template
from voodoo.admin_center.models import Supplier, DiscountGroup
from django.contrib.auth.decorators import login_required
admin.autodiscover()
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
    url(r'^captcha/', include('captcha.urls')),
    url(r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('voodoo.mainsite.RegistrationBackend.urls')),
    (r'^admin_center/service/', include('voodoo.admin_center.dhtmlScheduler.urls')),
    # operation center
    ('^admin_center/$', admin_center),
    url(r'^admin_center/login/$', auth_views.login, {'template_name': 'admin_login.html'}, name='auth_login'),
    ('^admin_center/order_create$', order_create),
    ('^admin_center/orders_import$', orders_import),
    ('^admin_center/order_edit/(?P<id>\d+)/$', order_edit),
    ('^admin_center/order_delete/(?P<id>\d+)/$', order_delete),
    ('^admin_center/orders_management$', orders_management),
    ('^admin_center/xls_import$', xls_import),
    ('^admin_center/user_management$', user_management),
    (r'^admin_center/autocomplete_client_phone/$', autocomplete_client_phone),
    (r'^admin_center/autocomplete_code/$', autocomplete_code),
    (r'^admin_center/autocomplete_brand/$', autocomplete_brand),
    ('^admin_center/items_management$', items_management),
    ('^admin_center/item_edit$', item_edit),
    ('^admin_center/item_ajax_edit/(?P<id>\d+)/$', item_ajax_edit),
    ('^admin_center/item_delete/(?P<id>\d+)/$', item_delete),
    ('^admin_center/feeds_currency$', feeds_currency),
    ('^admin_center/feeds_status$', feeds_status),
    ('^admin_center/orders_import_submit$', orders_import_submit),
    ('^admin_center/delete/(?P<modelname>[^/]+)/(?P<id>\d+)/$', delete_model),
    ('^admin_center/edit/(?P<modelname>[^/]+)/(?P<id>(\d+)|add)/$', edit_model),
    ('^admin_center/suppliers_list$', login_required(direct_to_template, login_url='/admin_center/login/'), {'template': 'suppliers_list.html',
         'extra_context': {'results': Supplier.objects.all}}),
    ('^admin_center/discount_list$', login_required(direct_to_template, login_url='/admin_center/login/'), {'template': 'discount_list.html',
         'extra_context': {'results': DiscountGroup.objects.all}}),
#    ('^admin_center/service$', include('voodoo.admin_center.dhtmlScheduler.urls')),

)