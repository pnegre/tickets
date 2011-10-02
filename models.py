# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import *


class Project(models.Model):
	name = models.CharField(max_length=200)
	
	def __unicode__(self):
		return self.name


# Associate user with project
class ProjectUser(models.Model):
	project = models.ForeignKey(Project)
	user = models.ForeignKey(User)
	
	def __unicode__(self):
		return self.user.username + " | " + unicode(self.project)


class Place(models.Model):
	name = models.CharField(max_length=500)
	
	def __unicode__(self):
		return self.name


class Ticket(models.Model):
	STATE_CHOICES = (
		(u'O', u'Oberta'),
		(u'T', u'Tancada'),
		(u'P', u'Pendent'),
    )
	
	description = models.TextField()
	reporter_email = models.CharField(max_length=200)
	date = models.DateTimeField(auto_now_add=True)
	place = models.ForeignKey(Place)
	date_resolved = models.DateTimeField(blank=True, null=True)
	state = models.CharField(max_length=2, choices=STATE_CHOICES)
	project = models.ForeignKey(Project)
	priority = models.IntegerField(default=5)
	
	def __unicode__(self):
		return self.description[0:50]
	
	class Meta:
		permissions = (
			('adminTickets','Pot administrar tickets'),
		)



class Comment(models.Model):
	text = models.TextField()
	author = models.ForeignKey(User)
	ticket = models.ForeignKey(Ticket)
	date = models.DateTimeField(auto_now_add=True)
	
	def __unicode__(self):
		return self.text[0:50]

