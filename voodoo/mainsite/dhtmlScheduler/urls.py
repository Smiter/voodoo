from django.conf.urls.defaults import *

urlpatterns = patterns('',
	# Should be changed for production
#    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/Users/js/Documents/cal/dhtmlScheduler/static',
#                                                              'show_indexes': True}),
    (r'cal/$', 'voodoo.mainsite.dhtmlScheduler.views.calendar'),
    (r'eventsXML$', 'voodoo.mainsite.dhtmlScheduler.views.eventsXML'),
    (r'dataprocessor$', 'voodoo.mainsite.dhtmlScheduler.views.dataprocessor'),

)
