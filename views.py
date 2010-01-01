# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from tickets.models import *

import urllib2, urllib


# TODO: segur que això va per POST?????
def checkEmail(email,password):
	return True # Eliminar això en la versió de producció
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
        del request.session['userid']
    except KeyError:
        pass
    return HttpResponseRedirect('login')



def doLogin(request):
	if request.method == 'POST':
		user = User.objects.filter(email=request.POST['email'])
		if user:
			u = user[0]
			if u.active and checkEmail(request.POST['email'],request.POST['pass']):
				request.session['userid'] = u.id
				request.session['fullname'] = u.full_name
				return HttpResponseRedirect('/tickets/open')
		return render_to_response( 'tickets/login.html', { 'bad_login': 1 } )
	
	return render_to_response(
		'tickets/login.html', {} )


def doList(request,typ):
	try:
		user = request.session['userid']
	except KeyError:
		return HttpResponseRedirect('/tickets/login')
	
	tickets = Ticket.objects.filter(state=typ)
	
	d = {'O': 'OBERTA', 'T': 'TANCADA', 'P': 'PENDENT'}
	
	return render_to_response(
		'tickets/index.html', { 
			'session': request.session,
			'tickets': tickets,
			'state': d[typ],
	} )


def doTicket(request,ticket_id):
	try:
		user = request.session['userid']
	except KeyError:
		return HttpResponseRedirect('/tickets/login')
	
	ticket = Ticket.objects.filter(id=ticket_id)[0]
	
	if request.method == "POST":
		fields = request.POST
		if fields['action'] == 'new':
			us = User.objects.filter(id=user)[0]
			comment = Comment(text=fields['text'], ticket=ticket, author=us)
			comment.save()
		elif fields['action'] == 'open':
			ticket.state = 'O'
			ticket.save()
			return redirect('/tickets/closed')
		elif fields['action'] == 'close':
			ticket.state = 'T'
			ticket.save()
			return redirect('/tickets/open')
		
	
	ticket = Ticket.objects.filter(id=ticket_id)[0]
	comments = Comment.objects.filter(ticket__id=ticket_id)
	
	return render_to_response(
		'tickets/ticket.html', {
			'session': request.session,
			'ticket': ticket,
			'comments': comments,
	} )


def newTicket(request):
	try:
		user = request.session['userid']
	except KeyError:
		return HttpResponseRedirect('/tickets/login')
	
	message = None
	if request.method == 'POST':
		fields = request.POST
		us = User.objects.filter(id=user)[0]
		plc = Place.objects.filter(id=fields['place'])[0]
		ticket = Ticket(
			description=fields['text'],
			state='O',
			reporter_email=us.email,
			place=plc
		)
		ticket.save()
		message = 'OK'
	
	places = Place.objects.all()
	
	return render_to_response(
		'tickets/newticket.html', {
			'session': request.session,
			'places': places,
			'message': message
	} )