from django.conf.urls import patterns, include, url
from mainsite.views import index
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('', ('^index/$',index),
	# url(r'^admin/', include(admin.site.urls)),
    # Examples:
    # url(r'^$', 'voodoo.views.home', name='home'),
    # url(r'^voodoo/', include('voodoo.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
