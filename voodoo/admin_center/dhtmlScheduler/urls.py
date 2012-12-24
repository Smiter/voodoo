from django.conf.urls.defaults import *

urlpatterns = patterns('',
	# Should be changed for production
#    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/Users/js/Documents/cal/dhtmlScheduler/static',
#                                                              'show_indexes': True}),
    (r'^$', 'voodoo.admin_center.dhtmlScheduler.views.calendar'),
    (r'eventsXML$', 'voodoo.admin_center.dhtmlScheduler.views.eventsXML'),
    (r'dataprocessor$', 'voodoo.admin_center.dhtmlScheduler.views.dataprocessor'),

)
