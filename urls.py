# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns('',

	(r'^$', 'tickets.views.doList', {'typ': 'O'}, "tickets-open"),

	(r'^open$', 'tickets.views.doList', {'typ': 'O'}, "tickets-open"),
	(r'^closed$', 'tickets.views.doList', {'typ': 'T'}, "tickets-closed"),
	(r'^pending$', 'tickets.views.doList', {'typ': 'P'}, "tickets-pending"),

	(r'^ticket/(?P<ticket_id>\d+)$', 'tickets.views.doTicket', {}, "ticket-show"),

	(r'^new$', 'tickets.views.newTicket', {}, "tickets-new"),

	(r'^userticket$', 'tickets.views.userTicket', {}, "user-ticket"),
	(r'^getplaces$', 'tickets.views.getPlaces', {}, "get-places"),
	(r'^getprojects$', 'tickets.views.getProjects', {}, "get-projects"),
	(r'^gettickets$', 'tickets.views.getTickets', {}, "get-tickets"),
	(r'^getticket/(?P<ticket_id>\d+)$', 'tickets.views.getTicket', {}, 'get-ticket'),

)
