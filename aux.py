# -*- coding: utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist

from tickets.models import *

##################################
# Torna el projecte associat a l'usuari
##################################
def getProject(user_):
    try:
        p = ProjectUser.objects.get(user=user_)
    except:
        p = ProjectUser(user=user_,project=Project.objects.all()[0])
        p.save()

    return p.project


##################################
# Pot veure l'usuari totes les incidències
# o només les que té assignades?
##################################
def userCanSeeAll(us):
    proj = getProject(us)
    pUser = ProjectUser.objects.get(project=proj,user=us)
    return pUser.see_all == 1


##################################
# Retorna els tickets assignat a l'usuari,
# tinguent en compte si els pot veure tots o no
##################################
def getTicketsAssignedToUser(us, typ):
    proj = getProject(us)
    pUser = ProjectUser.objects.get(project=proj,user=us)
    tickets = Ticket.objects.filter(state=typ, project=proj)

    if pUser.see_all == 1:
        pass
    else:
        tickets = tickets.filter(assigned_user=us) | tickets.filter(assigned_user=None)

    return tickets.order_by('date').reverse()


##################################
# Torna els possibles usuaris
# per assignar a incidències
##################################
def getPossibleUsers(project):
    result = []
    for p in ProjectUser.objects.filter(project=project):
        result.append(p.user)
    return result
