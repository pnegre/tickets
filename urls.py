# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('',

	(r'^$', 'tickets.views.doLogin'),
	(r'^login$', 'tickets.views.doLogin'),
	(r'^logout$', 'tickets.views.logout'),
	
	(r'^open$', 'tickets.views.doList', {'typ': 'O'}, "tickets-open"),
	(r'^closed$', 'tickets.views.doList', {'typ': 'T'}, "tickets-closed"),
	(r'^pending$', 'tickets.views.doList', {'typ': 'P'}, "tickets-pending"),
	
	(r'^ticket/(?P<ticket_id>\d+)$', 'tickets.views.doTicket'),
	
	(r'^new$', 'tickets.views.newTicket'),

)
