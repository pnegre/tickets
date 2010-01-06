# -*- coding: utf-8 -*-
from django.db import models


class Project(models.Model):
	name = models.CharField(max_length=200)
	
	def __unicode__(self):
		return self.name



class User(models.Model):	
	email = models.CharField(max_length=200)
	full_name = models.CharField(max_length=200)
	active = models.BooleanField(default=True)
	project = models.ForeignKey(Project)
	
	def __unicode__(self):
		return self.email


class Place(models.Model):
	name = models.CharField(max_length=500)
	project = models.ForeignKey(Project)
	
	def __unicode__(self):
		return self.name + " | " + self.project.name


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
	
	def __unicode__(self):
		return self.description[0:50]



class Comment(models.Model):
	text = models.TextField()
	author = models.ForeignKey(User)
	ticket = models.ForeignKey(Ticket)
	date = models.DateTimeField(auto_now_add=True)
	
	def __unicode__(self):
		return self.text[0:50]

