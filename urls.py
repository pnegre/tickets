# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('',

	(r'login$', 'tickets.views.doLogin'),
	(r'logout$', 'tickets.views.logout'),
	
	(r'open$', 'tickets.views.doList', {'typ': 'O'}),
	(r'closed$', 'tickets.views.doList', {'typ': 'T'}),
	(r'pending$', 'tickets.views.doList', {'typ': 'P'}),
	
	(r'ticket/(?P<ticket_id>\d+)$', 'tickets.views.doTicket'),
	
	(r'new$', 'tickets.views.newTicket'),

)
