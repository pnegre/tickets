# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import simplejson
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist

from datetime import datetime
from tickets.models import *

import urllib2, urllib

from tickets.forms import *
from tickets.aux import *



# TODO: segur que això va per POST?????
def checkEmail(email,password):
	try:
		req = urllib2.urlopen('https://www.google.com/accounts/ClientLogin',urllib.urlencode({
			'accountType': 'HOSTED',
			'Email'      : email,
			'Passwd'     : password,
			'service'    : 'apps',
		}))
		return True
	except:
		return False



#######################
# Llista de tickets (oberts, tancats...)
#######################
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
			ticket.date_resolved = datetime.now()
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
def userTicket(request):
	if request.POST:
		form = NewTicketFormUser(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			if checkEmail(data['user'],data['password']):
				form.save()
				return render_to_response(
					'tickets/userticket.html', {
						'message_ok': "Incidència introduïda correctament",
						'form': form,
				})
		
		return render_to_response(
			'tickets/userticket.html', {
				'message_fail': "Usuari i/o password no correctes",
				'form': form,
		})
	
	form = NewTicketFormUser()
	return render_to_response(
		'tickets/userticket.html', {
			'form': form,
	} )



def getPlaces(request,project):
	places = Place.objects.filter(project__id=project)
	r = dict(map(lambda x: (x.id, x.name), places))
	return HttpResponse(simplejson.dumps(r), mimetype='application/javascript')



def getProjects(request):
	projects = Project.objects.all()
	r = dict(map(lambda x: (x.id, x.name), projects))
	return HttpResponse(simplejson.dumps(r), mimetype='application/javascript')


