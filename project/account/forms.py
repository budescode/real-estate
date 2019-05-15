from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm, CharField
from django.contrib.auth.hashers import make_password,is_password_usable,check_password
import string
import random 
from django.forms import BaseModelFormSet
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import MinimumLengthValidator, validate_password, password_validators_help_text_html
from django.shortcuts import render,redirect
from datetime import *
from django.http import HttpResponseRedirect, HttpResponse,QueryDict
from .models import CreateProfile







	
class RegisterForm(forms.Form):
    username = forms.CharField()
    
    image = forms.FileField()
    first_name = forms.CharField(widget=forms.TextInput( 
        attrs={'class':'form-control', 'placeholder':'Enter First Name'}))
    last_name = forms.CharField(widget=forms.TextInput( 
        attrs={'class':'form-control', 'placeholder':'Enter Last Name'}))
    phone_number = forms.IntegerField()
    email    = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    def clea_pass(self):
    	cd = self.cleaned_data
    	if cd['password'] != cd['password2']:
    		raise forms.ValidationError('Passwords don\'t match.')
    	return cd['password']


    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("Username is taken")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput( 
        attrs={'class':'form-control', 'placeholder':'Enter username'}))
    password = forms.CharField(widget=forms.PasswordInput( 
        attrs={'class':'form-control', 'placeholder':'Enter Password'}))
    # def clean(self, *args, **kwargs):
    #     username = self.cleaned_data.get("username")
    #     password = self.cleaned_data.get("password")
    #     if username and password :
    #         user = authenticate(username=username, password=password)
    #         if not user:
    #             raise forms.ValidationError("Invalid Log in details. Try Again....")
    #         if not user.is_active:
    #             raise forms.ValidationError("This User is no longer active.")
    #         return super(LoginForm, self).clean(*args, **kwargs)





class CreateProfileForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput( 
        attrs={'class':'form-control', 'placeholder':'Enter Password'}))
    class Meta:
        model = CreateProfile 
        fields = ['username', 'email', 'password', 'category']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("Username is taken")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email



