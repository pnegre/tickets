# -*- coding: utf-8 -*-

from django.contrib import admin
from tickets.models import *

admin.site.register(Ticket)
admin.site.register(Comment)
admin.site.register(Place)
admin.site.register(Project)
