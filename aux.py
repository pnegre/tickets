# -*- coding: utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist

from tickets.models import *


def getProject(user_):
	try:
		p = ProjectUser.objects.get(user=user_)
	except:
		p = ProjectUser(user=user_,project=Project.objects.all()[0])
		p.save()
	
	return p.project

def getProjectUser(proj, us):
	return ProjectUser.objects.get(project=proj,user=us)
