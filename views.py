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



def logout(request):
    try:
        del request.session['theuser']
    except KeyError:
        pass
    return redirect(doLogin)



def doLogin(request):	
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			try:
				user = User.objects.get(email=data['email'])
				if user.active and checkEmail(data['email'],data['password']):
					request.session['theuser'] = user
					return redirect("tickets-open")
			except ObjectDoesNotExist:
				pass
		
		form = LoginForm()
		return render_to_response('tickets/login.html', { "form": form, "error": 1 } )
	
	else:
		form = LoginForm()
		return render_to_response(
			'tickets/login.html', { "form": form } )



#######################
# Llista de tickets (oberts, tancats...)
#######################
def doList(request,typ):	
	tickets = Ticket.objects.filter(state=typ,project=request.user.project).order_by('date').reverse()
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
	message = None
	if request.method == 'POST':
		fields = request.POST
		plc = Place.objects.filter(id=fields['place'])[0]
		ticket = Ticket(
			description=fields['text'],
			state='O',
			reporter_email=request.user.email,
			place=plc,
			project = request.user.project,
		)
		ticket.save()
		message = 'OK'
	
	places = Place.objects.filter(project=request.user.project)
	
	return render_to_response(
		'tickets/newticket.html', {
			'user': request.user,
			'places': places,
			'message': message
	} )


#######################
# Nou ticket (com a usuari "anònim")
#######################
def userTicket(request):
	projects = Project.objects.all();
	
	message = None
	if request.method == 'POST':
		fields = request.POST
		message = 'NO'
		if checkEmail(fields['email'],fields['pass']):
			try: 
				
				ticket = Ticket(
					description = fields['descrip'],
					state = 'O',
					reporter_email = fields['email'],
					place = Place.objects.filter(id=fields['lloc'])[0],
					project = Project.objects.filter(id=fields['tipus'])[0],
				)
				ticket.save()
				message = 'OK'
			except:
				pass
	
	return render_to_response(
		'tickets/userticket.html', {
			'message': message,
			'projects': projects,
	} )


def getPlaces(request,project):
	places = Place.objects.filter(project__id=project)
	r = dict(map(lambda x: (x.id, x.name), places))
	return HttpResponse(simplejson.dumps(r), mimetype='application/javascript')
