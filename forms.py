# -*- coding: utf-8 -*-

from django import forms
from tickets.models import *
from tickets.aux import *


class NewTicketForm(forms.Form):
	text = forms.CharField(widget=forms.Textarea(attrs={'rows': 10, 'cols': 60}))
	place = forms.ChoiceField()
	
	def __init__(self,user,*args,**kwrds):
		super(NewTicketForm,self).__init__(*args,**kwrds)
		self.fields['place'].choices = [[x.id,x.name] for x in Place.objects.all()]
	
	def save(self,user):
		data = self.cleaned_data
		place = Place.objects.get(id=data['place'])
		ticket = Ticket(
			description = data['text'],
			state = 'O',
			reporter_email = user.email,
			place = place,
			project = getProject(user),
		)
		ticket.save()


class NewTicketFormUser(forms.Form):
	text = forms.CharField(widget=forms.Textarea(attrs={'rows': 10, 'cols': 60}))
	place = forms.ChoiceField(choices = [[x.id,x.name] for x in Place.objects.all()])
	project = forms.ChoiceField(choices = [[x.id,x.name] for x in Project.objects.all()])
	
	def save(self,user):
		data = self.cleaned_data
		project = Project.objects.get(id=data['project'])
		place = Place.objects.get(id=data['place'])
		ticket = Ticket(
			description = data['text'],
			state = 'O',
			reporter_email = user.email,
			place = place,
			project = project,
		)
		ticket.save()

