# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from tickets.models import *

#def checkEmail(emal,password):
	#user = User.objects.filter(email=emal)
	#if email == 'aa' and password == 'bb': return True
	#return False
	


def logout(request):
    try:
        del request.session['userid']
    except KeyError:
        pass
    return HttpResponseRedirect('login')



def doLogin(request):
	if request.method == 'POST':
		# Check if user is valid
		user = User.objects.filter(email=request.POST['email'])
		if user:
			u = user[0]
			request.session['userid'] = u.id
			request.session['fullname'] = u.full_name
			return HttpResponseRedirect('index')
		else:
			return render_to_response( 'tickets/login.html', { 'bad_login': 1 } )
	
	return render_to_response(
		'tickets/login.html', {} )


def doIndex(request):
	try:
		user = request.session['userid']
	except KeyError:
		return HttpResponseRedirect('login')
	
	return render_to_response(
		'tickets/index.html', { 'fullname': request.session['fullname'] } )

