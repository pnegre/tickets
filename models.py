# -*- coding: utf-8 -*-
from django.db import models


class User(models.Model):
	email = models.TextField()
	full_name = models.CharField(max_length=200)
	
	def __unicode__(self):
		return self.email


class Ticket(models.Model):
	description = models.TextField()
	reporter_email = models.CharField(max_length=200)
	date = models.DateField(auto_now=True)



class Comment(models.Model):
	text = models.TextField()
	author = models.ForeignKey(User)
	ticket = models.ForeignKey(Ticket)
	date = models.DateField(auto_now=True)

