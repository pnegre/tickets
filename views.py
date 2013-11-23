# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import simplejson
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.decorators import login_required, permission_required

import datetime
from tickets.models import *

import urllib2, urllib

from tickets.forms import *
from tickets.aux import *



#######################
# Llista de tickets (oberts, tancats...)
#######################
@permission_required('tickets.adminTickets')
def doList(request,typ):
    tickets = getTicketsAssignedToUser(request.user, typ)
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
@permission_required('tickets.adminTickets')
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
                        "Autor: " + request.user.email, 
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
        elif fields['action'] == 'changeuser':
            if fields['assigneduser'] == "-1":
                ticket.assigned_user = None
            else:
                aus = User.objects.get(id=fields['assigneduser'])
                ticket.assigned_user = aus
            ticket.save()
            return redirect("tickets-open")
        
    
    ticket = Ticket.objects.filter(id=ticket_id)[0]
    comments = Comment.objects.filter(ticket__id=ticket_id).order_by('date').reverse()
    possibleUsers = getPossibleUsers(getProject(request.user))
    canChangeUser = userCanSeeAll(request.user)
    
    return render_to_response(
        'tickets/ticket.html', {
            'user': request.user,
            'ticket': ticket,
            'comments': comments,
            'possibleusers': possibleUsers,
            'canchangeuser': canChangeUser,
    } )



#######################
# Nou ticket (com a usuari registrat)
#######################
@permission_required('tickets.adminTickets')
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

##################################
# Funcions que retornen JSON per
# llocs i projectes
##################################
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



##################################
# Pillar tickets per ajax (mòbil)
##################################
@permission_required('tickets.adminTickets')
def getTickets(request):
    tickets = getTicketsAssignedToUser(request.user, 'O')
    r = []
    for t in tickets:
        cm = Comment.objects.filter(ticket=t)
        cmts = [ { 'text': c.text, 'author': c.author.username } for c in cm ]
        r.append({
            'id': t.id,
            'description': t.description, 
            'reporter_email': t.reporter_email,
            'place': t.place.name,
            'date': str(t.date),
            'comments': cmts,
        })
    return HttpResponse(simplejson.dumps(r), mimetype='application/javascript')


##################################
# Torna informació de ticket ajax (mòbil)
##################################
@permission_required('tickets.adminTickets')
def getTicket(request,ticket_id):
    x = Ticket.objects.get(id=ticket_id);
    r = {
        'description': x.description,
        'reporter_email': x.reporter_email,
        'date': str(x.date),
        'place': x.place.name,
    }
    return HttpResponse(simplejson.dumps(r), mimetype='application/javascript')

