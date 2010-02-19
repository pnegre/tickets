# -*- coding: utf-8 -*-

from django import forms

class LoginForm(forms.Form):
	email = forms.CharField(max_length=100)
	password = forms.CharField(max_length=100,widget=forms.PasswordInput())
