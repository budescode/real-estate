from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse ,QueryDict
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm, CreateProfileForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import *

from .models import CreateProfile


import urllib






def register(request):
	if request.method == 'POST':
		# form = CreateProfieForm1(request.POST or None)
		form = CreateProfileForm(request.POST or None, request.FILES or None)
		
		
		if form.is_valid():
			username  = form.cleaned_data.get("username")
			email  = form.cleaned_data.get("email")
			password  = form.cleaned_data.get("password")
			first_name  = form.cleaned_data.get("category")
			new_user  = User.objects.create_user(username, email, password)
			new = User.objects.get(username=username)
			new.first_name = first_name
			new.save()
			context={'username':username, 'first_name':first_name}
			return render(request, "account/registration_success.html", context)

	else:
		form = CreateProfileForm(request.POST or None) 
	context = {"form": form}
	return render(request, "account/register.html", context)







def registration_success(request):
	return render(request, 'account/registration_success.html', {})


def login_page(request):
	if request.method == 'POST':
		form = LoginForm(request.POST or None)
		if form.is_valid():
			username  = form.cleaned_data.get("username")
			password  = form.cleaned_data.get("password")
			user = authenticate(username=username, password=password)
			if user is not None:
			 	if user.is_active:
			 		login(request, user)
			 		return redirect('/')
			 	else:
			 		return HttpResponse('Disabled account')
			else:
				return HttpResponse('Invalid login')
	else:
		form = LoginForm()
	context = {"form": form}
	return render(request, "account/login.html", context)


def logout_page(request):
	logout(request)
	return render(request, "account/logout.html", {})
	



