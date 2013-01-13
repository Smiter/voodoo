from django.conf.urls.defaults import *
from voodoo.admin_center.dhtmlScheduler.models import Event, Event2


urlpatterns = patterns('',
    ('^calendar1/$', 'voodoo.admin_center.dhtmlScheduler.views.showCalendar', {'template_name': 'calendar1.html'}),
    ('^calendar2/$', 'voodoo.admin_center.dhtmlScheduler.views.showCalendar', {'template_name': 'calendar2.html'}),
    (r'eventsXML1$', 'voodoo.admin_center.dhtmlScheduler.views.eventsXML', {'event_model': Event}),
    (r'eventsXML2$', 'voodoo.admin_center.dhtmlScheduler.views.eventsXML', {'event_model': Event2}),
    (r'dataprocessor1$', 'voodoo.admin_center.dhtmlScheduler.views.dataprocessor', {'event_model': Event}),
    (r'dataprocessor2$', 'voodoo.admin_center.dhtmlScheduler.views.dataprocessor', {'event_model': Event2}),

)
