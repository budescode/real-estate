from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse ,QueryDict
from django.contrib.auth.models import User
from .forms import CreateProfileForm, RegisterForm, LoginForm, CategoryForm, ChangePasswordCodeForm, ChangePasswordForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import *

from .models import Profile, ChangePasswordCode
from django.shortcuts import get_list_or_404, get_object_or_404

import urllib
from django.core.mail import send_mail
from django.conf import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template



def googlelogin(request):
    logout(request)
    return redirect('social:begin', 'google-oauth2')

def fblogin(request):
    logout(request)
    return redirect('social:begin', 'facebook')



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


def login_Page(request):
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



def change_password(request):
	if request.method == 'POST':
		form = ChangePasswordCodeForm(request.POST)
		if form.is_valid():
			# try:
			email = form.cleaned_data.get('user_email')
			detail = ChangePasswordCode.objects.filter(user_email=email)
			if detail.exists():
				# messages.add_message(request, messages.INFO, 'invalid')
				for i in detail:
					i.delete()
				form.save()
				test = ChangePasswordCode.objects.get(user_email=email)
				subject = "Change Password"
				from_email = settings.EMAIL_HOST_USER
				# Now we get the list of emails in a list form.
				to_email = [email]
				#Opening a file in python, with closes the file when its done running
				detail2 = "http://anandrathi.pythonanywhere.com/account/"+ str(test.user_id)
				with open(settings.BASE_DIR + "/templates/account/change_password_email.txt") as sign_up_email_txt_file:
					sign_up_message = sign_up_email_txt_file.read()
				message = EmailMultiAlternatives(subject=subject, body=sign_up_message,from_email=from_email, to=to_email )
				html_template = get_template("account/change_password_email.html").render({'detail2':detail2})
				message.attach_alternative(html_template, "text/html")
				message.send()
				return redirect('account:change_password_confirm')
			else:
				form.save()
				test = ChangePasswordCode.objects.get(user_email=email)
				subject = 'Change Password'
				from_email= settings.EMAIL_HOST_USER
				to_email = [email]

				html = "http://anandrathi.pythonanywhere.com/account/"+ str(test.user_id)
				message = 'hi, click on the link below to change your password' + html
				send_mail(subject, message, from_email, to_email, fail_silently = False )
				return redirect('account:change_password_confirm')

		else:
			return HttpResponse('Invalid Email Address')
	else:
		form = ChangePasswordCodeForm()
	return render(request, 'account/change_password.html', {'form':form})


def change_password_confirm(request):
	return render(request, 'account/change_password_confirm.html', {})
def change_password_code(request, pk):
	test = ChangePasswordCode.objects.get(pk=pk)
	detail_email = test.user_email
	u = User.objects.get(email=detail_email)
	if request.method == 'POST':
		form = ChangePasswordForm(request.POST)
		if form.is_valid():
			u = User.objects.get(email=detail_email)
			new_password = form.cleaned_data.get('new_password')
			confirm_new_password = form.cleaned_data.get('confirm_new_password')


			if new_password == confirm_new_password:
				u.set_password(confirm_new_password)
				u.save()
				test.delete()
				return redirect('account:change_password_success')
			else:
				return HttpResponse('your new password should match with the confirm password')


		else:
			return HttpResponse('Invalid Details')
	else:
		form = ChangePasswordForm()
	return render(request, 'account/change_password_code.html', {'test':test, 'form':form, 'u':u})



def change_password_success(request):
	return render(request, 'account/change_password_success.html', {})