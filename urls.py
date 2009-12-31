# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('',

	(r'login$', 'tickets.views.doLogin'),
	(r'logout$', 'tickets.views.logout'),
	(r'index$', 'tickets.views.doIndex'),

)
