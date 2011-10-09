# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import simplejson
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.decorators import login_required, permission_required

from datetime import datetime
from tickets.models import *

import urllib2, urllib

from tickets.forms import *
from tickets.aux import *



#######################
# Llista de tickets (oberts, tancats...)
#######################
@permission_required('tickets.admintickets')
def doList(request,typ):
	proj = getProject(request.user)
	tickets = Ticket.objects.filter(state=typ,project=proj).order_by('date').reverse()
	d = {'O': 'OBERTA', 'T': 'TANCADA', 'P': 'PENDENT'}
	return render_to_response(
		'tickets/index.html', { 
			'user': request.user,
			'tickets': tickets,
			'state': d[typ],
	} )



#######################
# Tickets i comentaris
#######################
EMAIL_TEXT = u"Aquest missatge l'ha enviat el programa d'incidències per avisar-vos que hi ha un comentari referent a la incidència que reportàreu:"
@permission_required('tickets.admintickets')
def doTicket(request,ticket_id):
	ticket = Ticket.objects.filter(id=ticket_id)[0]
	
	if request.method == "POST":
		fields = request.POST
		if fields['action'] == 'new':
			comment = Comment(text=fields['text'], ticket=ticket, author=request.user)
			comment.save()
			if fields.has_key('email'):
				send_mail(
					'[Es Liceu] Ticket ' + str(ticket.id), 
					EMAIL_TEXT + "\n\n" + ticket.description + "\n\n" + 
						"Comentari: \n\n" + fields['text'] + "\n\n" + 
						"Autor: " + request.user.full_name + " (" + request.user.email + ")", 
					'tickets@esliceu.com', 
					[ ticket.reporter_email ]
				)
		elif fields['action'] == 'open':
			s = ticket.state
			ticket.state = 'O'
			ticket.save()
			if s == 'T':
				return redirect("tickets-closed")
			else:
				return redirect("tickets-pending")
		elif fields['action'] == 'close':
			ticket.state = 'T'
			ticket.date_resolved = datetime.datetime.now()
			ticket.save()
			return redirect("tickets-open")
		elif fields['action'] == 'delete':
			comments = Comment.objects.filter(ticket__id=ticket_id)
			if comments:
				for c in comments: c.delete()
			ticket.delete()
			return redirect("tickets-open")
		elif fields['action'] == 'pending':
			ticket.state = 'P'
			ticket.save()
			return redirect("tickets-open")
		
	
	ticket = Ticket.objects.filter(id=ticket_id)[0]
	comments = Comment.objects.filter(ticket__id=ticket_id).order_by('date').reverse()
	
	return render_to_response(
		'tickets/ticket.html', {
			'user': request.user,
			'ticket': ticket,
			'comments': comments,
	} )



#######################
# Nou ticket (com a usuari registrat)
#######################
@permission_required('tickets.admintickets')
def newTicket(request):
	if request.POST:
		form = NewTicketForm(request.user,request.POST)
		if form.is_valid():
			form.save(request.user)
			return redirect("tickets-open")
	
	form = NewTicketForm(request.user)
	return render_to_response(
		'tickets/newticket.html', {
			'user': request.user,
			'form': form,
	} )



#######################
# Nou ticket (com a usuari "anònim")
#######################
@login_required
def userTicket(request):
	if request.POST:
		form = NewTicketFormUser(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			form.save(request.user)
			return render_to_response(
				'tickets/userticket.html', {
					'message_ok': "Incidència introduïda correctament",
					'form': form,
			})
	
	form = NewTicketFormUser()
	return render_to_response(
		'tickets/userticket.html', {
			'form': form,
	} )


@login_required
def getPlaces(request):
	places = Place.objects.all()
	r = dict(map(lambda x: (x.id, x.name), places))
	return HttpResponse(simplejson.dumps(r), mimetype='application/javascript')


@login_required
def getProjects(request):
	projects = Project.objects.all()
	r = dict(map(lambda x: (x.id, x.name), projects))
	return HttpResponse(simplejson.dumps(r), mimetype='application/javascript')



@permission_required('tickets.admintickets')
def getTickets(request):
	proj = getProject(request.user)
	tickets = Ticket.objects.filter(state='O',project=proj).order_by('date');
	r = dict(map(lambda x: (x.id, {
		'id': x.id,
		'description': x.description[:50], 
		'reporter_email': x.reporter_email,
	}), tickets))
	return HttpResponse(simplejson.dumps(r), mimetype='application/javascript')


@permission_required('tickets.admintickets')
def getTicket(request,ticket_id):
	x = tickets = Ticket.objects.get(id=ticket_id);
	r = {
		'description': x.description,
		'reporter_email': x.reporter_email,
		'date': str(x.date),
		'place': x.place.name,
	}
	return HttpResponse(simplejson.dumps(r), mimetype='application/javascript')

