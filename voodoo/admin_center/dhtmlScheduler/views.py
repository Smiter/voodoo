from django.contrib.auth.models import User
from django.shortcuts import render_to_response

from voodoo.admin_center.dhtmlScheduler.models import Event, Event2
from django.views.generic.simple import direct_to_template


def eventsXML(request, event_model):
    """
    For now, return the whole event DB.
    """
    eventList = event_model.objects.all()
    users = User.objects.all()
    return render_to_response('events.xml',
                              {'eventList' : eventList, 'userList' : users},
                                mimetype="application/xhtml+xml")


def dataprocessor(request, event_model):
    """
    QueryDict data format:
    <QueryDict:{
    u'ids': [u'1295982759946'],
    u'1295982759946_id': [u'1295982759946'],
    u'1295982759946_end_date': [u'2011-01-11 00:05'],
    u'1295982759946_text': [u'New event'],
    u'1295982759946_start_date': [u'2011-01-11 00:00'],
    u'1295982759946_!nativeeditor_status': [u'inserted']
    }>

    Response Data format:

    <data>
       <action type="some" sid="r2" tid="r2" />
       <action type="some" sid="r3" tid="r3" />
    </data>


    type
    the type of the operation (update, insert, delete, invalid, error);
    sid
    the original row ID (the same as gr_id);
    tid
    the ID of the row after the operation (may be the same as gr_id,
    or some different one - it can be used during a new row adding,
    when a temporary ID, created on the client-side, is replaced with the ID,
    taken from the DB or by any other business rule).

    """
    responseList = []
    
    if request.method == 'POST':

        idList = request.POST['ids'].split(',')
        
        for id in idList:
            command = request.POST[id + '_!nativeeditor_status']
            if command == 'inserted':
                e = event_model()
                e.start_date = request.POST[id + '_start_date']
                e.end_date = request.POST[id + '_end_date']
                e.client_name = request.POST[id + '_client_name']
                e.client_number = request.POST[id + '_client_number']
                e.work_description = request.POST[id + '_work_description']
                e.car_description = request.POST[id + '_car_description']
                try:
                    if request.POST.get(id + '_worker'):
                        user = User.objects.get(username=request.POST[id + '_worker'])
                    else:
                        user = request.user
                except User.DoesNotExist:
                    print "USER DOES NOT EXIST"
                    user = request.user
                e.worker = user
                e.price = request.POST[id + '_price']
                e.save()
                response = {'type': 'insert', 'sid': request.POST[id + '_id'], 'tid': e.id}

            elif command == 'updated':
                e = event_model(pk=request.POST[id + '_id'])
                e.start_date = request.POST[id + '_start_date']
                e.end_date = request.POST[id + '_end_date']
                e.client_name = request.POST[id + '_client_name']
                e.client_number = request.POST[id + '_client_number']
                e.work_description = request.POST[id + '_work_description']
                e.car_description = request.POST[id + '_car_description']
                try:
                    if request.POST.get(id + '_worker'):
                        user = User.objects.get(username=request.POST[id + '_worker'])
                    else:
                        user = request.user
                except User.DoesNotExist:
                    print "USER DOES NOT EXIST"
                    user = request.user
                e.worker = user
                e.price = request.POST[id + '_price']
                e.save()
                response = {'type': 'update', 'sid': e.id, 'tid': e.id}

            elif command == 'deleted':
                e = event_model(pk=request.POST[id + '_id'])
                e.delete()
                response = {'type': 'delete', 'sid': request.POST[id + '_id'], 'tid': '0'}
                
            else:
                response = {'type': 'error', 'sid': request.POST[id + '_id'], 'tid': '0'}
                
            responseList.append(response)
            
    return render_to_response('dataprocessor.xml', {"responseList": responseList},
                                    mimetype="application/xhtml+xml")


def calendar(request):
    return direct_to_template(request, 'calendar.html')
#    return render_to_response('calendar.html')


def showCalendar(request, template_name):
    return direct_to_template(request, template_name)
