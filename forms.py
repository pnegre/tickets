# -*- coding: utf-8 -*-

from django import forms
from tickets.models import *

class LoginForm(forms.Form):
	email = forms.CharField(max_length=100)
	password = forms.CharField(max_length=100,widget=forms.PasswordInput())



class NewTicketForm(forms.Form):
	text = forms.CharField(widget=forms.Textarea(attrs={'rows': 10, 'cols': 60}))
	place = forms.ChoiceField()
	
	def __init__(self,user,*args,**kwrds):
		super(NewTicketForm,self).__init__(*args,**kwrds)
		self.fields['place'].choices = [[x.id,x.name] for x in Place.objects.filter(project=user.project)]
	
	def save(self,user):
		data = self.cleaned_data
		place = Place.objects.get(id=data['place'])
		ticket = Ticket(
			description = data['text'],
			state = 'O',
			reporter_email = user.email,
			place = place,
			project = user.project,
		)
		ticket.save()
		