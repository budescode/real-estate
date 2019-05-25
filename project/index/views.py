from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from .forms import PosterForm
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.models import User
# from account.forms import CreateProfileForm, CategoryForm
# from account.models import CreateProfile, Profile
from .models import Poster

def home(request):

	return render(request, 'index.html')

def about(request):
	return render(request, 'about.html')

def contact(request):
	return render(request, 'contact.html')

def blog(request):
	return render(request, 'blog.html')


# batmobi748/




@login_required(login_url='/account/login/')
def post(request):
	user = User.objects.get(username=request.user.username)
	print(user)
	if request.method == 'POST':		
		form = PosterForm(request.POST or None, request.FILES or None)
		if form.is_valid():
			qs = form.save(commit=False)
			
			user = User.objects.get(username=request.user.username)
			qs.user = user
			qs.save()
			return render(request, 'post_success.html')


	else:
		form = PosterForm() 
	context = {"form": form}
	return render(request, "sell.html", context)


@login_required(login_url='/account/login/')
def Mypost(request):
	user = User.objects.get(username=request.user.username)
	qs = Poster.objects.filter(active=False, user=user)
	context = {'qs':qs}
	return render(request, "mypost.html", context)


def Delete(request, id):
	user = User.objects.get(username=request.user.username)
	try:
		qs = Poster.objects.get(id_user=id,  user=user)
		qs.delete()
	except Poster.DoesNotExist:
		return HttpResponse("Post does not exist")
	return redirect('home:mypost')

def Edit(request, id):
	user = User.objects.get(username=request.user.username)
	qs = Poster.objects.get(id_user=id,  user=user)
	if request.method == 'POST':		
		form = PosterForm(request.POST or None, request.FILES or None, instance=qs)
		if form.is_valid():
			qs = form.save(commit=False)
			
			user = User.objects.get(username=request.user.username)
			qs.user = user
			qs.save()
			return render(request, 'editpost_success.html')


	else:
		form = PosterForm(request.POST or None, request.FILES or None, instance=qs)
	context = {"form": form}
	return render(request, "editpost.html", context)
