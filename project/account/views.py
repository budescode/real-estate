from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse ,QueryDict
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm, CreateProfileForm, CategoryForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import *

from .models import Profile
from django.shortcuts import get_list_or_404, get_object_or_404

import urllib





def profile(request):
	return render(request, 'account/profile.html')



def register(request):
	if request.method == 'POST':
		# form = CreateProfieForm1(request.POST or None)
		
		form = CreateProfileForm(request.POST or None, request.FILES or None)
		form2 = CategoryForm(request.POST or None, request.FILES or None)
		# form3 = SellerCategoryForm(request.POST or None)
	
		
		if form.is_valid():
			phone_number  = form.cleaned_data.get("phone_number")
			first_name = form.cleaned_data.get("first_name")
			last_name = form.cleaned_data.get("last_name")
			email  = form.cleaned_data.get("email")
			password  = form.cleaned_data.get("password")
			
			created_user =  User.objects.create_user(phone_number, email, password)
			created_user.first_name = first_name
			created_user.last_name = last_name
			created_user.save()
			

			if form2.is_valid():
				category  = form2.cleaned_data.get("category")
				seller_category = form2.cleaned_data.get("select")
				if category:
					if seller_category:
						Profile.objects.create(user=created_user, category=category, select=seller_category)
					else:
						Profile.objects.create(user=created_user, category=category)

					return render(request, "account/registration_success.html")	
				
				# if category == 'Seller':
				# 	Profile.objects.create(user=created_user, category=category)
				# 	context={'form3':form3}
				# 	return render(request, "account/category.html")
				# elif category == 'Buyer':
				# 	Profile.objects.create(user=created_user, category=category)
				# 	context={'username':created_user.username}
					

	else:
		form = CreateProfileForm(request.POST or None) 
		form2 = CategoryForm(request.POST or None, request.FILES or None)
		# form3 = SellerCategoryForm(request.POST or None, request.FILES or None)
	context = {"form": form, 'form2':form2}
	return render(request, "account/register.html", context)



# if request.method == "POST":
# 	user_form = UserForm(request.POST, request.FILES, instance=user)
# 	formset = ProfileInlineFormset(request.POST, request.FILES, instance=user)

# 		if user_form.is_valid():
# 			created_user = user_form.save(commit=False)
# 			formset = ProfileInlineFormset(request.POST, request.FILES, instance=created_user)

# 				if formset.is_valid():
# 					created_user.save()
# 					formset.save()
# 					return HttpResponseRedirect('/accounts/profile/')



def registration_success(request):
	return render(request, 'account/registration_success.html', {})


def login_page(request):
	if request.method == 'POST':
		form = LoginForm(request.POST or None)
		if form.is_valid():
			phone_number  = form.cleaned_data.get("phone_number")
			password  = form.cleaned_data.get("password")
			user = authenticate(username=phone_number, password=password)
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
	



def Upgrade(request):
	return render(request, 'account/upgrade.html')