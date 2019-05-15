from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from .forms import PosterForm, SeekerForm
from django.contrib.auth import authenticate, login, get_user_model, logout
from account.forms import CreateProfileForm
from account.models import CreateProfile
from .models import Poster, Seeker

def home(request):
	if request.method == 'POST':
		# form = CreateProfieForm1(request.POST or None)
		form = CreateProfileForm(request.POST or None, request.FILES or None)
		
		
		if form.is_valid():
			username  = form.cleaned_data.get("username")
			email  = form.cleaned_data.get("email")
			password  = form.cleaned_data.get("password")
			first_name  = form.cleaned_data.get("category")

			new_user  = User.objects.create(username=username, email=email, password=password, first_name=first_name)
			context={'username':username, 'first_name':first_name}
			return render(request, "registration_success.html", context)

	else:
		form = CreateProfileForm(request.POST or None) 
	

	try:
		category = request.user.first_name
	except AttributeError:
		category=""
	return render(request, 'index.html', {'category':category, "form": form})

def about(request):
	return render(request, 'about.html')

def contact(request):
	return render(request, 'contact.html')

def blog(request):
	return render(request, 'blog.html')


# batmobi748/
def login_page(request):
	return render(request, 'login.html')


def login_view(request):	
	email = request.POST.get("email")
	password = request.POST.get("password")

	user = authenticate(username=username, password=password)
	if user is not None:
		if user.is_active:
			login(request, user)
			return redirect('/')
		else:
			return HttpResponse('Disabled account')
	else:
		return HttpResponse('Invalid login')
	print(email, password)
	return HttpResponse("done")

def logout_page(request):
	logout(request)
	return render(request, 'logout.html')

def register_seeker(request):
	emailseeker = request.POST.get('emailseeker')
	password1seeker = request.POST.get('password1seeker')
	password2seeker = request.POST.get('password2seeker')
	print('seeker', emailseeker, password1seeker, password2seeker)
	return HttpResponse("done")

def register_poster(request):
	emailposter = request.POST.get('emailposter')
	password1poster = request.POST.get('password1poster')
	password2poster = request.POST.get('password2poster')
	print('poster',emailposter, password1poster, password2poster)
	return HttpResponse('done')



@login_required(login_url='/account/login/')
def post(request):
	if request.method == 'POST':
		if request.user.first_name == "Poster":
			form = PosterForm(request.POST or None, request.FILES or None)
			if form.is_valid():
				form.save()
				return render(request, 'post_success.html')
		elif request.user.first_name == "Seeker":
			form = SeekerForm(request.POST or None, request.FILES or None)
			if form.is_valid():
				form.save()
				return render(request, 'post_success.html')
		else:
			return render(request, 'first_name.html')		
		
			# new_user  = User.objects.create_user(username, email, password)
			# CreateProfie.objects.create(user=username, email=email, image=image, phone_number=phone_number, first_name=first_name, last_name=last_name)
			# return redirect('account:registration_success')

	else:
		form = PosterForm() 
	context = {"form": form}
	return render(request, "post.html", context)



@login_required(login_url='/account/login/')
def search_field(request):
	seeker = request.POST.get("seeker")
	poster = request.POST.get("poster")
	print('seeker', seeker)
	print('poster', poster)
	if seeker:
		qs = Seeker.objects.filter(f25__icontains=seeker)
		return render(request, 'filter.html', {'qs':qs})

	if poster:
		qs = Poster.objects.filter(f25__icontains=poster)
		return render(request, 'filter.html', {'qs':qs})
	else:
		return HttpResponse("search something")
