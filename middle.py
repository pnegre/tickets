# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
import sys

from tickets.views import doLogin

class middle:
	def __init__(self):
		pass
	
	#def process_request(self,request):
		#pass
	
	
	def process_view(self, request, view_func, view_args, view_kwargs):
		module = sys.modules[view_func.__module__]
		if view_func.func_name in ('doList', 'doTicket', 'newTicket'):
			try:
				uid = request.session['userid']
			except KeyError:
				return redirect(doLogin)
	
	#def process_response(self,request,exception):
		#pass