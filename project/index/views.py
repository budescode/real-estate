from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse,JsonResponse
from .forms import PosterForm, PosterRentForm
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.models import User
# from account.forms import CreateProfileForm, CategoryForm
# from account.models import CreateProfile, Profile
from .models import Poster, SavedSearch, PosterRent
import json
from administrator.models import CountryDetails
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests
# from django.core.paginator import Paginator




def home(request):
	qs = CountryDetails.objects.all()

	return render(request, 'index.html', {'qs':qs})

def about(request):
	return render(request, 'rough.html')

def contact(request):
	return render(request, 'contact.html')

def blog(request):
	return render(request, 'blog.html')


# this function is used to filter the searched items from users
def filter_search(request):
	qs = CountryDetails.objects.all()
	if not request.method == 'POST':
	    #if the method isn't post, it get its data off the session
		print('hiddensearchsession', request.session['hiddensearchsession'])

		hiddensearch = request.session['hiddensearchsession']
		mylist = request.session['mylistsession']
		propertytype1 = request.session['propertytype1session']
		bedmin1 = request.session['bedmin1session']
		bedmax1 = request.session['bedmax1session']
		pricemax1 = request.session['pricemax1session']
		pricemin1 = request.session['pricemin1session']
		category = request.session['categorysession']
		state = request.session['state']


		print('valuessssss', mylist, propertytype1, bedmin1, bedmax1, pricemax1, pricemin1)

# 		return HttpResponse('done')
	if request.method == 'POST':
		hiddensearch = request.POST.get("hiddensearch") #it brings a string of the postalcode
		print(hiddensearch)
		if hiddensearch:
		    hiddensearch0 = hiddensearch.replace('X', '')
		    hiddensearch1 =  hiddensearch0.split(',')
		    mylist = list(dict.fromkeys(hiddensearch1)) #to remove duplicate from hiddensearch1
		else:
		    mylist = ['']
		request.session['hiddensearchsession'] = hiddensearch
		request.session['mylistsession'] = mylist

		category = request.POST.get("category") #it brings a string of the category rent or buy
		request.session['categorysession'] = category

		state = request.POST.get("state")
		request.session['state'] = state
		print('the state isss', state, mylist )

		propertytype1 = request.POST.get("propertytype1")
		propertytype1 =  propertytype1.split(',')
		request.session['propertytype1session'] = propertytype1

		bedmin1 = request.POST.get("Bed(min)")[0]
		request.session['bedmin1session'] = bedmin1

		bedmax1 = request.POST.get("Bed(max)")[0]
		request.session['bedmax1session'] = bedmax1

		pricemax1 = request.POST.get("Price(max)")
		pricemax1 = ''.join(pricemax1.split())
		pricemax1 = ''.join(pricemax1.split(','))
		pricemax1 = pricemax1[1:]
		request.session['pricemax1session'] = pricemax1

		pricemin1 = request.POST.get("Price(min)")
		pricemin1 = ''.join(pricemin1.split())
		pricemin1 = ''.join(pricemin1.split(','))
		pricemin1 = pricemin1[1:]
		request.session['pricemin1session'] = pricemin1

	if category == 'Poster':
		category = Poster
		category1 = 'Poster'


	elif category == 'PosterRent':
		category = PosterRent
		category1 = 'PosterRent'
		print('PosterRent')



	if bedmin1 == 'B' or bedmin1 == 'A' or bedmin1 == 'Bed (min)' or bedmin1 == 'Any':
		bedminsearch = 0
	elif bedmin1 == 'S' or bedmin1 == 'Studio':
		bedminsearch = 0
	else:
		bedminsearch = int(bedmin1)

	if bedmax1 == 'B' or bedmax1 == 'A' or bedmax1=='Bed (max)' or bedmax1 =='Any':
		bedmaxsearch = 100

	elif bedmax1 == 'S' or bedmax1 == 'Studio':
		bedmaxsearch = 0

	else:
		bedmaxsearch = int(bedmax1)

	if pricemin1 == 'rice(min)' or pricemin1 == 'ny' or pricemin1== 'Price (min)':
		priceminsearch = 0

	else:
		priceminsearch = int(pricemin1)


	if pricemax1 == 'rice(max)' or pricemax1 == 'ny' or pricemax1=='Price (max)':
		pricemaxsearch = 1000000000000
	else:
		pricemaxsearch = int(pricemax1)



	generallist = []
	# this is the list where all the filtered items will be



	list2 = ['TAS GLEBEA' ,'NT DARWIN']
#
	# it'll remove duplicate from the list that has the postal code

	searchlist = []
	# this list contains all the Poster that has the postal code needed
	#print('mylist', len(mylist), mylist, mylist[0] )
	if mylist == ['']:
	   # print('zobobobo')
	    searchlist = category.objects.all()
	else:
	    for i in mylist:
	        findvalue = i.find(' ')

	       # statesub = i[0:findvalue].strip()
	       # print('ok',statesub, i)
	       # ab = i.replace(' '+state, '')
	       # print('abbb', ab, len(ab))
	        postal1 = i[-5:]

	        first = postal1[:1]
	        if first == ' ':
	            print('space')
	            postal1 = postal1[-6:]
	            suburb = i.replace(postal1, '')
	            sub = suburb[0:len(suburb)]

	        else:
	            print('nahhhh', first)

	            suburb = i.replace(postal1, '')
	            sub = suburb[0:len(suburb)-1]

	        test = postal1.replace(' ', '')


	       # postal = ab[-4:].replace(' ', '')




	        print('testingggggg',sub,postal1, state)
	        if suburb == '':
	            post = category.objects.filter(state= state)
	        else:
	            post = category.objects.filter(state__icontains= state, suburb__icontains=sub)
	           # print('post isss', post, category)
	        searchlist.extend(post)
	#print('searchlist', searchlist)

	#print('bedminsearch is', bedminsearch)
# 	print('dvdhdhdhhdhd', bedminsearch, bedmaxsearch,pricemaxsearch, priceminsearch)
# 	print(propertytype1)
	for i in searchlist:

		if 'All property types' in propertytype1:
			print('yeahhh')
			if int(i.Bedrooms) >= int(bedminsearch) and int(i.Bedrooms) <= int(bedmaxsearch) and int(i.Price)>=priceminsearch and int(i.Price)<=pricemaxsearch:
			    try:
			        saved = SavedSearch.objects.get(post_id=i.id_user)
			        i.saved = True
			        generallist.append(i)
			    except SavedSearch.DoesNotExist:
			        generallist.append(i)



			else:
				pass

			# it'll append the post to the general list
		else:
			for a in propertytype1:
				if i.Property_type==a and int(i.Bedrooms) >= int(bedminsearch) and int(i.Bedrooms) <= int(bedmaxsearch) and int(i.Price)>=priceminsearch and int(i.Price)<=pricemaxsearch:
					print("yes", i.Property_type)
					try:
					    saved = SavedSearch.objects.get(post_id=i.id_user)
					    i.saved = True
					    generallist.append(i)
					except SavedSearch.DoesNotExist:
					    generallist.append(i)


	generallist = list(dict.fromkeys(generallist))	# it'll remove duplicate from the generallist
	page = request.GET.get('page', 1)

	paginator = Paginator(generallist, 30)
	try:
		pagin = paginator.page(page)
	except PageNotAnInteger:
		pagin = paginator.page(1)
	except EmptyPage:
		pagin = paginator.page(paginator.num_pages)
# 	paginator = Paginator(qs, 2) # Show 20 contacts per page
# 	page = request.GET.get('page')
# 	myposts = paginator.get_page(page)
	context = {'pagin':pagin}
	# 	page = request.GET.get('page', 1)

	# 	paginator = Paginator(generallist, 4)
	# 	try:
	# 		pagin = paginator.page(page)
	# 	except PageNotAnInteger:
	# 		pagin = paginator.page(1)
	# 	except EmptyPage:
	# 		pagin = paginator.page(paginator.num_pages)


	context = {'qs':qs,'pagin':pagin, 'category1':category1,'generallist':generallist, 'bedminsearch':bedminsearch, 'bedmaxsearch':bedmaxsearch, 'priceminsearch':priceminsearch, 'pricemaxsearch':pricemaxsearch}


	return render(request, 'filter_search.html', context)

# batmobi748/



def details(request, id, category):

    if category == 'Poster':
        category1=Poster
    elif category ==  'PosterRent':
        category1 = PosterRent

    qs = category1.objects.get(id_user = id)
    qs1 = SavedSearch.objects.filter(post_id=qs.id_user)
    if qs1:
        data = True
    else:
        data = False
    context = {'qs':qs, 'data':data}
    return render(request, 'details.html', context)




@login_required(login_url='/account/login/')
def post(request):

	state = CountryDetails.objects.values_list('state', flat=True).distinct()
	postcode = CountryDetails.objects.values_list('postcode', flat=True).distinct()
	suburb = CountryDetails.objects.values_list('suburb', flat=True).distinct()



	# for i in qs:
	# 	print(qs)
	user = User.objects.get(username=request.user.username)
	if request.method == 'POST':
		form = PosterForm(request.POST or None, request.FILES or None)
		if form.is_valid():
			street_number = form.cleaned_data['street_number']
			street_name = form.cleaned_data['street_name']
			suburb = form.cleaned_data['suburb']
			postcode = form.cleaned_data['postcode']
			state = form.cleaned_data['state']

			qs = form.save(commit=False)
			# qs = CountryDetails.objects.all()
			print('okkkkkkkk', street_number, street_name, suburb, postcode, state)
			url =  'https://maps.googleapis.com/maps/api/geocode/json?address='+ str(street_number) + ', '+ str(street_name) + ', ' +  str(suburb) + ', ' +  str(state) + ', ' + str(postcode) + '&key=AIzaSyBfZ86mdGX5E7o4PGSB7ct22axSb_JzVTY'
			r = requests.get(url = url)
			data = r.json()
			print(url)
			print('dataaaaaaaaaaaaaa', data)
			latitude = data['results'][0]['geometry']['location']['lat']
			longitude = data['results'][0]['geometry']['location']['lng']

			user = User.objects.get(username=request.user.username)
			qs.user = user
			qs.latitude = latitude
			qs.longitude = longitude

			qs.save()

			return render(request, 'post_success.html')
	else:
		form = PosterForm()
	context = {"state": state, 'suburb':suburb, 'postcode':postcode, 'form':form}
	return render(request, "sell.html", context)


@login_required(login_url='/account/login/')
def rent_view(request):
	# qs = CountryDetails.objects.all()
	state = CountryDetails.objects.values_list('state', flat=True).distinct()
	postcode = CountryDetails.objects.values_list('postcode', flat=True).distinct()
	suburb = CountryDetails.objects.values_list('suburb', flat=True).distinct()

	# for i in qs:
	# 	print(qs)
	user = User.objects.get(username=request.user.username)
	if request.method == 'POST':
		form = PosterRentForm(request.POST or None, request.FILES or None)
		if form.is_valid():
			qs = form.save(commit=False)

			user = User.objects.get(username=request.user.username)
			qs.user = user
			qs.save()
			return render(request, 'post_success.html')
	else:
		form = PosterRentForm()
	context = {"state": state, 'suburb':suburb, 'postcode':postcode, 'form':form}
	return render(request, "rent.html", context)



def filterDetails(request):
	state = request.POST.get("state")
	print(state)
	# .order_by('photo__name', 'photo__url').distinct('photo__name', 'photo__url')
	qs = CountryDetails.objects.filter(state__iexact=state).values_list('postcode', 'suburb').distinct()
	qs1 = CountryDetails.objects.filter(state__iexact=state)

	print(len(qs), len(qs1))
	result_list = list(qs.values('suburb', 'postcode'))
	return HttpResponse(json.dumps(result_list))



@login_required(login_url='/account/login/')
def Mypost(request):
	user = User.objects.get(username=request.user.username)
	qs = Poster.objects.filter(user=user)
	page = request.GET.get('page', 1)

	paginator = Paginator(qs, 20)
	try:
		pagin = paginator.page(page)
	except PageNotAnInteger:
		pagin = paginator.page(1)
	except EmptyPage:
		pagin = paginator.page(paginator.num_pages)
# 	paginator = Paginator(qs, 2) # Show 20 contacts per page
# 	page = request.GET.get('page')
# 	myposts = paginator.get_page(page)
	context = {'pagin':pagin}

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


def savesearch(request):
    post_id = request.POST.get('post_id')
    try:
        qs = SavedSearch.objects.get(user=request.user, post_id=post_id)
        qs.delete()
        print('deleted')
        return JsonResponse({"post_id":post_id, 'msg':'deleted'})
    except SavedSearch.DoesNotExist:
        SavedSearch.objects.create(user=request.user, post_id=post_id)
        print('saved')
        return JsonResponse({"post_id":post_id, 'msg':'saved'})

def deletesavesearch(request):
    post_id = request.POST.get('post_id')
    qs = SavedSearch.objects.get(user=request.user, post_id=post_id)
    qs.delete()
    return JsonResponse({"post_id":post_id})

def mysavedsearch(request):
    qs = []
    searcheditems = SavedSearch.objects.filter(user = request.user)
    for i in searcheditems:
        p = Poster.objects.filter(id_user = i.post_id)
        qs.extend(p)
        #qs.extend(p)
        print(p, type(p))
    return render(request, 'mysavedsearch.html', {'qs':qs})