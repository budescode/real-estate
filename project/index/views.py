from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse,JsonResponse
from .forms import PosterForm, PosterRentForm
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.models import User
# from account.forms import CreateProfileForm, CategoryForm
# from account.models import CreateProfile, Profile
from .models import Poster, SavedSearch, PosterRent, SavedHeaders, SavedDetail
import json
from administrator.models import CountryDetails
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests
# from django.core.paginator import Paginator




def home(request):
	qs = CountryDetails.objects.all()

	return render(request, 'index/index.html', {'qs':qs})

def about(request):
	return render(request, 'about.html')

def contact(request):
	return render(request, 'contact.html')

def blog(request):
	return render(request, 'blog.html')

def get_saved_property(request):
    qs = SavedHeaders.objects.filter(user=request.user)
    qs2 = SavedDetail.objects.filter(user=request.user)
    return render(request, 'mysavedproperty.html', {'qs':qs, 'qs2':qs2})

#this is to save the property
def save_search_details(request):
    namesave = request.POST.get('namesave')
    searchlist = request.POST.get('searchlist')
    # searchlist = searchlist.replace("'", '')

    searchlist = searchlist.split(',')
    pricemin = request.POST.get('pricemin')
    pricemax = request.POST.get('pricemax')
    bedmin = request.POST.get('bedmin')
    bedmax = request.POST.get('bedmax')
    notification = request.POST.get('notification')
    propertytype = request.POST.get('propertytype')
    print(propertytype)

    if notification == 'true':
        notification=True
    elif notification == 'false':
        notification = False
        # , SavedHeaders, SavedDetail
    qs = SavedHeaders.objects.create(user=request.user,property_type=propertytype, name=namesave, pricemin=pricemin, pricemax=pricemax, bedmin=bedmin, bedmax=bedmax, notification=notification)
    for i in searchlist:
        SavedDetail.objects.create(user=request.user, search=i, header=qs)

    print(namesave,searchlist,pricemin, pricemax,bedmin, bedmax, notification)


    return JsonResponse({"done":'done'})





# this function is used to filter the searched items from users
def filter_search(request):

# 	print(filterlist,sortby ,'listttt')
# 	for i in filterlist:
# 	    print(i)
# 	return HttpResponse('done')

	qs = CountryDetails.objects.all()
	sort = '-created'
	filterlist = ['none']
	if not request.method == 'POST':
	    #if the method isn't post, it get its data off the session
# 		print('hiddensearchsession', request.session['hiddensearchsession'])

		hiddensearch = request.session['hiddensearchsession']
		print(hiddensearch)
		mylist = request.session['mylistsession']
		propertytype1 = request.session['propertytype1']
		bedmin1 = request.session['bedmin1']
		bedmax1 = request.session['bedmax1']
		pricemax1 = request.session['pricemax1']
		pricemin1 = request.session['pricemin1']
# 		category = request.session['categorysession']
# 		state = request.session['state']
		firstbedmin = request.session['firstbedmin']
		firstbedmax = request.session['firstbedmax']
		firstpricemin = request.session['firstpricemin']
		firstpricemax = request.session['firstpricemax']
		firstpropertytype = request.session['firstpropertytype']
		filterlist = request.session['filterlist']
		sort = request.session['sort']
		if sort == None:
		    print('yeah nine')
		    sort = '-created'





		#print('valuessssss', mylist, propertytype1, bedmin1, bedmax1, pricemax1, pricemin1)

# 		return HttpResponse('done')
	if request.method == 'POST':
		hiddensearch = request.POST.get("hiddensearch") #it brings a string of the postalcode
		print(hiddensearch)
		#print('hiddensearch is',hiddensearch)
		if hiddensearch:
		    hiddensearch0 = hiddensearch.replace('X', '')
		    hiddensearch1 =  hiddensearch0.split(',')
		    mylist = list(dict.fromkeys(hiddensearch1)) #to remove duplicate from hiddensearch1
		else:
		    mylist = ['']
		request.session['hiddensearchsession'] = hiddensearch
		request.session['mylistsession'] = mylist
		filterlist = request.POST.get('filterlist')

		if filterlist:
			filterlist = filterlist.split(',')
			request.session['filterlist'] = filterlist
		else:
		    fillterlist = ['']
		    request.session['filterlist'] = filterlist
		sort = request.POST.get('sortby')
		request.session['sort'] = sort
		if sort == None:
		    print('yeahh')
		    sort = '-created'
		elif sort == 'Relevant':
		    sort = '-created'
		else:
		    print('nahhh')
		print('sortbyyyy', sort)

# 		category = request.POST.get("category") #it brings a string of the category rent or buy
# 		request.session['categorysession'] = category

# 		state = request.POST.get("state")
# 		request.session['state'] = state
# 		print('the state isss', state, mylist )

		propertytype1 = request.POST.get("propertytype1")
		firstpropertytype = propertytype1 #I will return it as default value back to the template.

		propertytype1 =  propertytype1.split(',')
		request.session['propertytype1'] = propertytype1
		request.session['firstpropertytype'] = firstpropertytype


		bedmin1 = request.POST.get("Bed(min)")
		firstbedmin = bedmin1 #I will return it as default value back to the template.

		request.session['bedmin1'] = bedmin1
		request.session['firstbedmin'] = firstbedmin


		bedmax1 = request.POST.get("Bed(max)")
		firstbedmax = bedmax1 #I will return it as default value back to the template.

		request.session['bedmax1'] = bedmax1
		request.session['firstbedmax'] = firstbedmax
		#print('enhh', propertytype1, bedmin1, bedmax1, price_range[0], price_range[1])
# 		return HttpResponse('ok')

# 		pricemax1 = request.POST.get("Price(max)")
# 		pricemax1 = ''.join(pricemax1.split())
# 		pricemax1 = ''.join(pricemax1.split(','))
# 		pricemax1 = pricemax1[1:]

		pricemax1 = request.POST.get("pricemax")
		firstpricemax = pricemax1
		pricemax1 = pricemax1[1:]
		pricemax1 = pricemax1.replace(',', '')
		request.session['pricemax1'] = pricemax1
		request.session['firstpricemax'] = firstpricemax


# 		pricemin1 = request.POST.get("Price(min)")
# 		pricemin1 = ''.join(pricemin1.split())
# 		pricemin1 = ''.join(pricemin1.split(','))
# 		pricemin1 = pricemin1[1:]
		pricemin1 = request.POST.get("pricemin")
		firstpricemin = pricemin1
		pricemin1 = pricemin1[1:]
		pricemin1 = pricemin1.replace(',', '')
		request.session['pricemin1'] = pricemin1
		request.session['firstpricemin'] = firstpricemin

# 	print('testttt', pricemin1, pricemax1,propertytype1, bedmin1, bedmax1)

# 	return HttpResponse('done')

	category = 'Poster'
	if category == 'Poster':
		category = Poster
		category1 = 'Poster'


	elif category == 'PosterRent':
		category = PosterRent
		category1 = 'PosterRent'
		#print('PosterRent')



	if bedmin1 == 'B' or bedmin1 == 'A' or bedmin1 == 'Bed (min)' or bedmin1 == 'Any' or bedmin1 == 'ny':
		bedminsearch = 0
	elif bedmin1 == 'S' or bedmin1 == 'Studio':
		bedminsearch = 0
	else:
		bedminsearch = int(bedmin1)

	if bedmax1 == 'B' or bedmax1 == 'A' or bedmax1=='Bed (max)' or bedmax1 =='Any' or bedmax1 =='ny':
		bedmaxsearch = 100

	elif bedmax1 == 'S' or bedmax1 == 'Studio':
		bedmaxsearch = 0

	else:
		bedmaxsearch = int(bedmax1)

	if pricemin1 == 'rice(min)' or pricemin1 == 'ny' or pricemin1== 'Price (min)' or pricemin1== 'Any':
		priceminsearch = 0

	else:
		priceminsearch = int(pricemin1)


	if pricemax1 == 'rice(max)' or pricemax1 == 'ny' or pricemax1=='Price (max)' or pricemax1=='Any':
		pricemaxsearch = 1000000000000
	else:
		pricemaxsearch = int(pricemax1)



	generallist = []
	# this is the list where all the filtered items will be



	list2 = ['TAS GLEBEA' ,'NT DARWIN']
	#print(bedminsearch, bedmaxsearch, priceminsearch, pricemaxsearch)
#
	# it'll remove duplicate from the list that has the postal code

	searchlist = []
	# this list contains all the Poster that has the postal code needed
	#print('mylist', len(mylist), mylist, mylist[0] )
# 	print(fillterlist)
# 	return HttpResponse('done')
	print('filterrrr', filterlist)
	if mylist == ['']:
	   # print('zobobobo')
		if 'All property types' in propertytype1:
			if filterlist:
				if 'Swimming_pool' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Swimming_pool=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Garage' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Garage=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Balcony' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Balcony=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Outdoor_area' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Outdoor_area=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Undercover_parking' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Undercover_parking=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Shed' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Shed=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Fully_fenced' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Fully_fenced=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Outdoor_spa' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Outdoor_spa=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Tennis_court' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Tennis_court=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Ensuite' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Ensuite=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'DishWasher' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,DishWasher=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Study' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Study=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Built_in_robes' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Built_in_robes=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Alarm_system' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Alarm_system=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Broadband' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Broadband=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Floorboards' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Floorboards=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Gym' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Gym=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Rumpus_room' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Rumpus_room=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Workshop' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Workshop=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Air_conditioning' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Air_conditioning=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Solar_panels' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Solar_panels=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Heating' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Heating=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'High_energy_efficiency' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,High_energy_efficiency=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Water_tank' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Water_tank=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Solar_hot_water' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Solar_hot_water=True ).order_by(sort)
					searchlist.extend(searchlist1)


				else:
					searchlist = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch).order_by(sort)
					print('nahhhh')
			else:
				searchlist = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch).order_by(sort)
				print('okayyyyy')
		else:
			for i in propertytype1:

				# searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch, Property_type=i)
				# searchlist.extend(searchlist1)
				if filterlist:
					if 'Swimming_pool' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Swimming_pool=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Garage' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Garage=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Balcony' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Balcony=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Outdoor_area' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Outdoor_area=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Undercover_parking' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Undercover_parking=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Shed' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Shed=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Fully_fenced' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Fully_fenced=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Outdoor_spa' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Outdoor_spa=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Tennis_court' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Tennis_court=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Ensuite' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Ensuite=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'DishWasher' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,DishWasher=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Study' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Study=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Built_in_robes' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Built_in_robes=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Alarm_system' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Alarm_system=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Broadband' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Broadband=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Floorboards' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Floorboards=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Gym' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Gym=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Rumpus_room' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Rumpus_room=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Workshop' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Workshop=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Air_conditioning' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Air_conditioning=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Solar_panels' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Solar_panels=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Heating' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Heating=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'High_energy_efficiency' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,High_energy_efficiency=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Water_tank' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Water_tank=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Solar_hot_water' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Solar_hot_water=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)


					else:
						searchlist = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch, Property_type=i).order_by(sort)
						print('nahhhh')
				else:
					searchlist = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch, Property_type=i).order_by(sort)
					print('okayyyyy')

	else:
		for i in mylist:
			findvalue = i.find(' - ')

			suburb = i[0:findvalue]
			state = i[findvalue+3:].replace(' ', '')
			print(suburb, state)
			if suburb == '':
				if 'All property types' in propertytype1:
					if filterlist:
						if 'Swimming_pool' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Swimming_pool=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Garage' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Garage=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Balcony' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Balcony=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Outdoor_area' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Outdoor_area=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Undercover_parking' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Undercover_parking=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Shed' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Shed=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Fully_fenced' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Fully_fenced=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Outdoor_spa' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Outdoor_spa=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Tennis_court' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Tennis_court=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Ensuite' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Ensuite=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'DishWasher' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,DishWasher=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Study' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Study=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Built_in_robes' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Built_in_robes=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Alarm_system' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Alarm_system=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Broadband' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Broadband=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Floorboards' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Floorboards=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Gym' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Gym=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Rumpus_room' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Rumpus_room=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Workshop' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Workshop=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Air_conditioning' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Air_conditioning=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Solar_panels' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Solar_panels=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Heating' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Heating=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'High_energy_efficiency' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,High_energy_efficiency=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Water_tank' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Water_tank=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Solar_hot_water' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Solar_hot_water=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)


						else:
							searchlist = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,state= state).order_by(sort)
							print('nahhhh')
					else:
						searchlist = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,state= state).order_by(sort)
						print('okayyyyy')
				else:
					for a in propertytype1:
						post = category.objects.filter(Property_type=a, state= state, Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch).order_by(sort)
						searchlist.extend(post)
			else:
				print(state, suburb, 'zobo', filterlist)
				if 'All property types' in propertytype1:
					post = category.objects.filter(state__icontains= state, suburb__icontains=suburb, Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch).order_by(sort)
					if filterlist:
						print('yaya')
						if 'Swimming_pool' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Swimming_pool=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Garage' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Garage=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Balcony' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Balcony=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Outdoor_area' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Outdoor_area=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Undercover_parking' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Undercover_parking=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Shed' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Shed=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Fully_fenced' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Fully_fenced=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Outdoor_spa' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Outdoor_spa=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Tennis_court' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Tennis_court=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Ensuite' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Ensuite=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'DishWasher' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,DishWasher=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Study' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Study=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Built_in_robes' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Built_in_robes=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Alarm_system' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Alarm_system=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Broadband' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Broadband=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Floorboards' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Floorboards=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Gym' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Gym=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Rumpus_room' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Rumpus_room=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Workshop' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Workshop=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Air_conditioning' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Air_conditioning=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Solar_panels' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Solar_panels=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Heating' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Heating=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'High_energy_efficiency' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,High_energy_efficiency=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Water_tank' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Water_tank=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Solar_hot_water' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Solar_hot_water=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)


						else:
							searchlist = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,state__icontains= state, suburb__icontains=suburb,).order_by(sort)
							print('nahhhh')
					else:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,state__icontains= state, suburb__icontains=suburb,).order_by(sort)
						searchlist.extend(searchlist1)
				else:
					for a in propertytype1:
						if filterlist:
							if 'Swimming_pool' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Swimming_pool=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Garage' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Garage=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Balcony' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Balcony=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Outdoor_area' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Outdoor_area=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Undercover_parking' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Undercover_parking=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Shed' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Shed=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Fully_fenced' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Fully_fenced=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Outdoor_spa' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Outdoor_spa=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Tennis_court' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Tennis_court=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Ensuite' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Ensuite=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'DishWasher' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,DishWasher=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Study' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Study=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Built_in_robes' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Built_in_robes=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Alarm_system' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Alarm_system=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Broadband' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Broadband=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Floorboards' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Floorboards=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Gym' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Gym=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Rumpus_room' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Rumpus_room=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Workshop' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Workshop=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Air_conditioning' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Air_conditioning=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Solar_panels' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Solar_panels=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Heating' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Heating=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'High_energy_efficiency' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,High_energy_efficiency=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Water_tank' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Water_tank=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Solar_hot_water' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Solar_hot_water=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)


							else:
								searchlist = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Property_type=a, state= state, suburb__icontains=suburb).order_by(sort)
								print('nahhhh')
						else:
							searchlist = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Property_type=a, state= state, suburb__icontains=suburb).order_by(sort)
							print('okayyyyy')

			print('propertytype1 is', propertytype1)

	pagin = list(dict.fromkeys(searchlist))	# it'll remove duplicate from the generallist

	try:
	    user = User.objects.get(username=request.user.username)
	    saved = SavedSearch.objects.filter(user=request.user)
	    #print('saved is', saved)
	except User.DoesNotExist:
	    saved='None'
	   # print('saved is', saved)
	    pass

# 	print('lastttttt', saved)

	context = {'sort':sort, 'saved':saved, 'firstbedmin':firstbedmin, 'firstpropertytype':firstpropertytype, 'firstbedmax':firstbedmax, 'firstpricemax':firstpricemax, 'firstpricemin':firstpricemin, 'saved':saved,'mylist':mylist,'qs':qs,'pagin':pagin, 'category1':category1,'generallist':generallist, 'bedminsearch':bedminsearch, 'bedmaxsearch':bedmaxsearch, 'priceminsearch':priceminsearch, 'pricemaxsearch':pricemaxsearch}


	return render(request, 'filter_search.html', context)

# batmobi748/




# this function is used to display filter the searched items from users in map
def mapview_search(request):

# 	print(filterlist,sortby ,'listttt')
# 	for i in filterlist:
# 	    print(i)
# 	return HttpResponse('done')

	qs = CountryDetails.objects.all()
	sort = '-created'
	filterlist = ['none']
	if not request.method == 'POST':
	    #if the method isn't post, it get its data off the session
# 		print('hiddensearchsession', request.session['hiddensearchsession'])

		hiddensearch = request.session['hiddensearchsession']
		print(hiddensearch)
		mylist = request.session['mylistsession']
		propertytype1 = request.session['propertytype1']
		bedmin1 = request.session['bedmin1']
		bedmax1 = request.session['bedmax1']
		pricemax1 = request.session['pricemax1']
		pricemin1 = request.session['pricemin1']
# 		category = request.session['categorysession']
# 		state = request.session['state']
		firstbedmin = request.session['firstbedmin']
		firstbedmax = request.session['firstbedmax']
		firstpricemin = request.session['firstpricemin']
		firstpricemax = request.session['firstpricemax']
		firstpropertytype = request.session['firstpropertytype']
		filterlist = request.session['filterlist']
		sort = request.session['sort']
		if sort == None:
		    print('yeah nine')
		    sort = '-created'





		#print('valuessssss', mylist, propertytype1, bedmin1, bedmax1, pricemax1, pricemin1)

# 		return HttpResponse('done')
	if request.method == 'POST':
		hiddensearch = request.POST.get("hiddensearch") #it brings a string of the postalcode
		print(hiddensearch)
		#print('hiddensearch is',hiddensearch)
		if hiddensearch:
		    hiddensearch0 = hiddensearch.replace('X', '')
		    hiddensearch1 =  hiddensearch0.split(',')
		    mylist = list(dict.fromkeys(hiddensearch1)) #to remove duplicate from hiddensearch1
		else:
		    mylist = ['']
		request.session['hiddensearchsession'] = hiddensearch
		request.session['mylistsession'] = mylist
		filterlist = request.POST.get('filterlist')

		if filterlist:
			filterlist = filterlist.split(',')
			request.session['filterlist'] = filterlist
		else:
		    fillterlist = ['']
		    request.session['filterlist'] = filterlist
		sort = request.POST.get('sortby')
		request.session['sort'] = sort
		if sort == None:
		    print('yeahh')
		    sort = '-created'
		elif sort == 'Relevant':
		    sort = '-created'
		else:
		    print('nahhh')
		print('sortbyyyy', sort)

# 		category = request.POST.get("category") #it brings a string of the category rent or buy
# 		request.session['categorysession'] = category

# 		state = request.POST.get("state")
# 		request.session['state'] = state
# 		print('the state isss', state, mylist )

		propertytype1 = request.POST.get("propertytype1")
		firstpropertytype = propertytype1 #I will return it as default value back to the template.

		propertytype1 =  propertytype1.split(',')
		request.session['propertytype1'] = propertytype1
		request.session['firstpropertytype'] = firstpropertytype


		bedmin1 = request.POST.get("Bed(min)")
		firstbedmin = bedmin1 #I will return it as default value back to the template.

		request.session['bedmin1'] = bedmin1
		request.session['firstbedmin'] = firstbedmin


		bedmax1 = request.POST.get("Bed(max)")
		firstbedmax = bedmax1 #I will return it as default value back to the template.

		request.session['bedmax1'] = bedmax1
		request.session['firstbedmax'] = firstbedmax
		#print('enhh', propertytype1, bedmin1, bedmax1, price_range[0], price_range[1])
# 		return HttpResponse('ok')

# 		pricemax1 = request.POST.get("Price(max)")
# 		pricemax1 = ''.join(pricemax1.split())
# 		pricemax1 = ''.join(pricemax1.split(','))
# 		pricemax1 = pricemax1[1:]

		pricemax1 = request.POST.get("pricemax")
		firstpricemax = pricemax1
		pricemax1 = pricemax1[1:]
		pricemax1 = pricemax1.replace(',', '')
		request.session['pricemax1'] = pricemax1
		request.session['firstpricemax'] = firstpricemax


# 		pricemin1 = request.POST.get("Price(min)")
# 		pricemin1 = ''.join(pricemin1.split())
# 		pricemin1 = ''.join(pricemin1.split(','))
# 		pricemin1 = pricemin1[1:]
		pricemin1 = request.POST.get("pricemin")
		firstpricemin = pricemin1
		pricemin1 = pricemin1[1:]
		pricemin1 = pricemin1.replace(',', '')
		request.session['pricemin1'] = pricemin1
		request.session['firstpricemin'] = firstpricemin

# 	print('testttt', pricemin1, pricemax1,propertytype1, bedmin1, bedmax1)

# 	return HttpResponse('done')

	category = 'Poster'
	if category == 'Poster':
		category = Poster
		category1 = 'Poster'


	elif category == 'PosterRent':
		category = PosterRent
		category1 = 'PosterRent'
		#print('PosterRent')



	if bedmin1 == 'B' or bedmin1 == 'A' or bedmin1 == 'Bed (min)' or bedmin1 == 'Any' or bedmin1 == 'ny':
		bedminsearch = 0
	elif bedmin1 == 'S' or bedmin1 == 'Studio':
		bedminsearch = 0
	else:
		bedminsearch = int(bedmin1)

	if bedmax1 == 'B' or bedmax1 == 'A' or bedmax1=='Bed (max)' or bedmax1 =='Any' or bedmax1 =='ny':
		bedmaxsearch = 100

	elif bedmax1 == 'S' or bedmax1 == 'Studio':
		bedmaxsearch = 0

	else:
		bedmaxsearch = int(bedmax1)

	if pricemin1 == 'rice(min)' or pricemin1 == 'ny' or pricemin1== 'Price (min)' or pricemin1== 'Any':
		priceminsearch = 0

	else:
		priceminsearch = int(pricemin1)


	if pricemax1 == 'rice(max)' or pricemax1 == 'ny' or pricemax1=='Price (max)' or pricemax1=='Any':
		pricemaxsearch = 1000000000000
	else:
		pricemaxsearch = int(pricemax1)



	generallist = []
	# this is the list where all the filtered items will be



	list2 = ['TAS GLEBEA' ,'NT DARWIN']
	#print(bedminsearch, bedmaxsearch, priceminsearch, pricemaxsearch)
#
	# it'll remove duplicate from the list that has the postal code

	searchlist = []
	# this list contains all the Poster that has the postal code needed
	#print('mylist', len(mylist), mylist, mylist[0] )
# 	print(fillterlist)
# 	return HttpResponse('done')
	print('filterrrr', filterlist)
	if mylist == ['']:
	   # print('zobobobo')
		if 'All property types' in propertytype1:
			if filterlist:
				if 'Swimming_pool' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Swimming_pool=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Garage' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Garage=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Balcony' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Balcony=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Outdoor_area' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Outdoor_area=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Undercover_parking' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Undercover_parking=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Shed' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Shed=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Fully_fenced' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Fully_fenced=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Outdoor_spa' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Outdoor_spa=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Tennis_court' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Tennis_court=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Ensuite' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Ensuite=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'DishWasher' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,DishWasher=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Study' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Study=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Built_in_robes' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Built_in_robes=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Alarm_system' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Alarm_system=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Broadband' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Broadband=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Floorboards' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Floorboards=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Gym' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Gym=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Rumpus_room' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Rumpus_room=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Workshop' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Workshop=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Air_conditioning' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Air_conditioning=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Solar_panels' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Solar_panels=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Heating' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Heating=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'High_energy_efficiency' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,High_energy_efficiency=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Water_tank' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Water_tank=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Solar_hot_water' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Solar_hot_water=True ).order_by(sort)
					searchlist.extend(searchlist1)


				else:
					searchlist = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch).order_by(sort)
					print('nahhhh')
			else:
				searchlist = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch).order_by(sort)
				print('okayyyyy')
		else:
			for i in propertytype1:

				# searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch, Property_type=i)
				# searchlist.extend(searchlist1)
				if filterlist:
					if 'Swimming_pool' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Swimming_pool=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Garage' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Garage=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Balcony' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Balcony=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Outdoor_area' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Outdoor_area=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Undercover_parking' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Undercover_parking=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Shed' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Shed=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Fully_fenced' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Fully_fenced=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Outdoor_spa' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Outdoor_spa=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Tennis_court' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Tennis_court=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Ensuite' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Ensuite=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'DishWasher' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,DishWasher=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Study' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Study=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Built_in_robes' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Built_in_robes=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Alarm_system' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Alarm_system=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Broadband' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Broadband=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Floorboards' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Floorboards=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Gym' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Gym=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Rumpus_room' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Rumpus_room=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Workshop' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Workshop=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Air_conditioning' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Air_conditioning=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Solar_panels' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Solar_panels=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Heating' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Heating=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'High_energy_efficiency' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,High_energy_efficiency=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Water_tank' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Water_tank=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Solar_hot_water' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Solar_hot_water=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)


					else:
						searchlist = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch, Property_type=i).order_by(sort)
						print('nahhhh')
				else:
					searchlist = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch, Property_type=i).order_by(sort)
					print('okayyyyy')

	else:
		for i in mylist:
			findvalue = i.find(' - ')

			suburb = i[0:findvalue]
			state = i[findvalue+3:].replace(' ', '')
			print(suburb, state)
			if suburb == '':
				if 'All property types' in propertytype1:
					if filterlist:
						if 'Swimming_pool' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Swimming_pool=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Garage' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Garage=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Balcony' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Balcony=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Outdoor_area' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Outdoor_area=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Undercover_parking' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Undercover_parking=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Shed' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Shed=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Fully_fenced' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Fully_fenced=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Outdoor_spa' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Outdoor_spa=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Tennis_court' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Tennis_court=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Ensuite' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Ensuite=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'DishWasher' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,DishWasher=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Study' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Study=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Built_in_robes' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Built_in_robes=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Alarm_system' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Alarm_system=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Broadband' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Broadband=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Floorboards' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Floorboards=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Gym' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Gym=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Rumpus_room' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Rumpus_room=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Workshop' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Workshop=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Air_conditioning' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Air_conditioning=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Solar_panels' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Solar_panels=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Heating' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Heating=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'High_energy_efficiency' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,High_energy_efficiency=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Water_tank' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Water_tank=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Solar_hot_water' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Solar_hot_water=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)


						else:
							searchlist = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,state= state).order_by(sort)
							print('nahhhh')
					else:
						searchlist = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,state= state).order_by(sort)
						print('okayyyyy')
				else:
					for a in propertytype1:
						post = category.objects.filter(Property_type=a, state= state, Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch).order_by(sort)
						searchlist.extend(post)
			else:
				print(state, suburb, 'zobo', filterlist)
				if 'All property types' in propertytype1:
					post = category.objects.filter(state__icontains= state, suburb__icontains=suburb, Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch).order_by(sort)
					if filterlist:
						print('yaya')
						if 'Swimming_pool' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Swimming_pool=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Garage' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Garage=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Balcony' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Balcony=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Outdoor_area' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Outdoor_area=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Undercover_parking' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Undercover_parking=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Shed' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Shed=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Fully_fenced' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Fully_fenced=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Outdoor_spa' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Outdoor_spa=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Tennis_court' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Tennis_court=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Ensuite' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Ensuite=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'DishWasher' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,DishWasher=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Study' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Study=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Built_in_robes' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Built_in_robes=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Alarm_system' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Alarm_system=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Broadband' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Broadband=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Floorboards' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Floorboards=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Gym' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Gym=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Rumpus_room' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Rumpus_room=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Workshop' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Workshop=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Air_conditioning' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Air_conditioning=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Solar_panels' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Solar_panels=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Heating' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Heating=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'High_energy_efficiency' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,High_energy_efficiency=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Water_tank' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Water_tank=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Solar_hot_water' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Solar_hot_water=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)


						else:
							searchlist = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,state__icontains= state, suburb__icontains=suburb,).order_by(sort)
							print('nahhhh')
					else:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,state__icontains= state, suburb__icontains=suburb,).order_by(sort)
						searchlist.extend(searchlist1)
				else:
					for a in propertytype1:
						if filterlist:
							if 'Swimming_pool' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Swimming_pool=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Garage' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Garage=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Balcony' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Balcony=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Outdoor_area' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Outdoor_area=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Undercover_parking' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Undercover_parking=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Shed' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Shed=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Fully_fenced' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Fully_fenced=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Outdoor_spa' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Outdoor_spa=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Tennis_court' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Tennis_court=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Ensuite' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Ensuite=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'DishWasher' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,DishWasher=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Study' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Study=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Built_in_robes' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Built_in_robes=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Alarm_system' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Alarm_system=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Broadband' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Broadband=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Floorboards' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Floorboards=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Gym' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Gym=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Rumpus_room' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Rumpus_room=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Workshop' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Workshop=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Air_conditioning' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Air_conditioning=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Solar_panels' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Solar_panels=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Heating' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Heating=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'High_energy_efficiency' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,High_energy_efficiency=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Water_tank' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Water_tank=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Solar_hot_water' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Solar_hot_water=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)


							else:
								searchlist = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Property_type=a, state= state, suburb__icontains=suburb).order_by(sort)
								print('nahhhh')
						else:
							searchlist = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Property_type=a, state= state, suburb__icontains=suburb).order_by(sort)
							print('okayyyyy')

			print('propertytype1 is', propertytype1)

	pagin = list(dict.fromkeys(searchlist))	# it'll remove duplicate from the generallist

	try:
	    user = User.objects.get(username=request.user.username)
	    saved = SavedSearch.objects.filter(user=request.user)
	    #print('saved is', saved)
	except User.DoesNotExist:
	    saved='None'
	   # print('saved is', saved)
	    pass

# 	print('lastttttt', saved)

	context = {'sort':sort, 'saved':saved, 'firstbedmin':firstbedmin, 'firstpropertytype':firstpropertytype, 'firstbedmax':firstbedmax, 'firstpricemax':firstpricemax, 'firstpricemin':firstpricemin, 'saved':saved,'mylist':mylist,'qs':qs,'pagin':pagin, 'category1':category1,'generallist':generallist, 'bedminsearch':bedminsearch, 'bedmaxsearch':bedmaxsearch, 'priceminsearch':priceminsearch, 'pricemaxsearch':pricemaxsearch}


	return render(request, 'index/mapview.html', context)

# batmobi748/



def delete_saved_property(request, id):
    qs = SavedHeaders.objects.get(id=id)
    qs.delete()
    return redirect('home:get_saved_property')


# this function is used to filter the searched items from users
def property_search_detail(request, id):
	mylist = []
	filterlist = []
	head = SavedHeaders.objects.get(id=id, user=request.user)
	details = SavedDetail.objects.filter(header=head, user=request.user)
	sort = '-created'
	for i in details:
		mylist.append(i.search)
	propertytype1 = head.property_type
	firstpropertytype = propertytype1 #I will return it as default value back to the template.

	propertytype1 =  propertytype1.split(',')

	bedmin1 = head.bedmin
	firstbedmin = bedmin1 #I will return it as default value back to the template.


	bedmax1 = head.bedmax
	firstbedmax = bedmax1 #I will return it as default value back to the template.

	pricemax1 = head.pricemax
	firstpricemax = pricemax1
	pricemax1 = pricemax1[1:]
	pricemax1 = pricemax1.replace(',', '')


	pricemin1 = head.pricemin
	firstpricemin = pricemin1
	pricemin1 = pricemin1[1:]
	pricemin1 = pricemin1.replace(',', '')

	category = 'Poster'
	if category == 'Poster':
		category = Poster
		category1 = 'Poster'


	elif category == 'PosterRent':
		category = PosterRent
		category1 = 'PosterRent'
		#print('PosterRent')



	if bedmin1 == 'B' or bedmin1 == 'A' or bedmin1 == 'Bed (min)' or bedmin1 == 'Any' or bedmin1 == 'ny':
		bedminsearch = 0
	elif bedmin1 == 'S' or bedmin1 == 'Studio':
		bedminsearch = 0
	else:
		bedminsearch = int(bedmin1)

	if bedmax1 == 'B' or bedmax1 == 'A' or bedmax1=='Bed (max)' or bedmax1 =='Any' or bedmax1 =='ny':
		bedmaxsearch = 100

	elif bedmax1 == 'S' or bedmax1 == 'Studio':
		bedmaxsearch = 0

	else:
		bedmaxsearch = int(bedmax1)

	if pricemin1 == 'rice(min)' or pricemin1 == 'ny' or pricemin1== 'Price (min)' or pricemin1== 'Any':
		priceminsearch = 0

	else:
		priceminsearch = int(pricemin1)


	if pricemax1 == 'rice(max)' or pricemax1 == 'ny' or pricemax1=='Price (max)' or pricemax1=='Any':
		pricemaxsearch = 1000000000000
	else:
		pricemaxsearch = int(pricemax1)



	generallist = []
	# this is the list where all the filtered items will be



	list2 = ['TAS GLEBEA' ,'NT DARWIN']
	#print(bedminsearch, bedmaxsearch, priceminsearch, pricemaxsearch)
#
	# it'll remove duplicate from the list that has the postal code

	searchlist = []
	# this list contains all the Poster that has the postal code needed
	#print('mylist', len(mylist), mylist, mylist[0] )
# 	print(fillterlist)
# 	return HttpResponse('done')
# 	print('filterrrr', filterlist)

	if mylist == ['']:
	   # print('zobobobo')
		if 'All property types' in propertytype1:
			if filterlist:
				if 'Swimming_pool' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Swimming_pool=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Garage' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Garage=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Balcony' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Balcony=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Outdoor_area' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Outdoor_area=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Undercover_parking' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Undercover_parking=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Shed' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Shed=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Fully_fenced' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Fully_fenced=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Outdoor_spa' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Outdoor_spa=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Tennis_court' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Tennis_court=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Ensuite' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Ensuite=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'DishWasher' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,DishWasher=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Study' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Study=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Built_in_robes' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Built_in_robes=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Alarm_system' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Alarm_system=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Broadband' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Broadband=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Floorboards' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Floorboards=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Gym' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Gym=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Rumpus_room' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Rumpus_room=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Workshop' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Workshop=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Air_conditioning' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Air_conditioning=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Solar_panels' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Solar_panels=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Heating' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Heating=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'High_energy_efficiency' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,High_energy_efficiency=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Water_tank' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Water_tank=True ).order_by(sort)
					searchlist.extend(searchlist1)
				elif 'Solar_hot_water' in filterlist:
					searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Solar_hot_water=True ).order_by(sort)
					searchlist.extend(searchlist1)


				else:
					searchlist = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch).order_by(sort)
					print('nahhhh')
			else:
				searchlist = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch).order_by(sort)
				print('okayyyyy')
		else:
			for i in propertytype1:

				# searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch, Property_type=i)
				# searchlist.extend(searchlist1)
				if filterlist:
					if 'Swimming_pool' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Swimming_pool=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Garage' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Garage=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Balcony' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Balcony=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Outdoor_area' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Outdoor_area=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Undercover_parking' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Undercover_parking=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Shed' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Shed=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Fully_fenced' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Fully_fenced=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Outdoor_spa' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Outdoor_spa=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Tennis_court' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Tennis_court=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Ensuite' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Ensuite=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'DishWasher' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,DishWasher=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Study' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Study=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Built_in_robes' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Built_in_robes=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Alarm_system' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Alarm_system=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Broadband' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Broadband=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Floorboards' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Floorboards=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Gym' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Gym=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Rumpus_room' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Rumpus_room=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Workshop' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Workshop=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Air_conditioning' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Air_conditioning=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Solar_panels' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Solar_panels=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Heating' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Heating=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'High_energy_efficiency' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,High_energy_efficiency=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Water_tank' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Water_tank=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)
					elif 'Solar_hot_water' in filterlist:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Solar_hot_water=True , Property_type=i ).order_by(sort)
						searchlist.extend(searchlist1)


					else:
						searchlist = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch, Property_type=i).order_by(sort)
						print('nahhhh')
				else:
					searchlist = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch, Property_type=i).order_by(sort)
					print('okayyyyy')

	else:
		for i in mylist:
			findvalue = i.find(' - ')

			suburb = i[0:findvalue]
			state = i[findvalue+3:].replace(' ', '')
			print(suburb, state)
			if suburb == '':
				if 'All property types' in propertytype1:
					if filterlist:
						if 'Swimming_pool' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Swimming_pool=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Garage' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Garage=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Balcony' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Balcony=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Outdoor_area' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Outdoor_area=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Undercover_parking' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Undercover_parking=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Shed' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Shed=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Fully_fenced' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Fully_fenced=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Outdoor_spa' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Outdoor_spa=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Tennis_court' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Tennis_court=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Ensuite' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Ensuite=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'DishWasher' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,DishWasher=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Study' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Study=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Built_in_robes' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Built_in_robes=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Alarm_system' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Alarm_system=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Broadband' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Broadband=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Floorboards' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Floorboards=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Gym' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Gym=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Rumpus_room' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Rumpus_room=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Workshop' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Workshop=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Air_conditioning' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Air_conditioning=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Solar_panels' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Solar_panels=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Heating' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Heating=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'High_energy_efficiency' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,High_energy_efficiency=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Water_tank' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Water_tank=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Solar_hot_water' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Solar_hot_water=True ,state= state ).order_by(sort)
							searchlist.extend(searchlist1)


						else:
							searchlist = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,state= state).order_by(sort)
							print('nahhhh')
					else:
						searchlist = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,state= state).order_by(sort)
						print('okayyyyy')
				else:
					for a in propertytype1:
						post = category.objects.filter(Property_type=a, state= state, Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch).order_by(sort)
						searchlist.extend(post)
			else:
				print(state, suburb, 'zobo', filterlist)
				if 'All property types' in propertytype1:
					post = category.objects.filter(state__icontains= state, suburb__icontains=suburb, Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch).order_by(sort)
					if filterlist:
						print('yaya')
						if 'Swimming_pool' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Swimming_pool=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Garage' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Garage=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Balcony' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Balcony=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Outdoor_area' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Outdoor_area=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Undercover_parking' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Undercover_parking=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Shed' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Shed=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Fully_fenced' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Fully_fenced=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Outdoor_spa' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Outdoor_spa=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Tennis_court' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Tennis_court=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Ensuite' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Ensuite=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'DishWasher' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,DishWasher=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Study' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Study=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Built_in_robes' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Built_in_robes=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Alarm_system' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Alarm_system=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Broadband' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Broadband=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Floorboards' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Floorboards=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Gym' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Gym=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Rumpus_room' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Rumpus_room=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Workshop' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Workshop=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Air_conditioning' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Air_conditioning=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Solar_panels' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Solar_panels=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Heating' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Heating=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'High_energy_efficiency' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,High_energy_efficiency=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Water_tank' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Water_tank=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)
						elif 'Solar_hot_water' in filterlist:
							searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Solar_hot_water=True ,state__icontains= state, suburb__icontains=suburb, ).order_by(sort)
							searchlist.extend(searchlist1)


						else:
							searchlist = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,state__icontains= state, suburb__icontains=suburb,).order_by(sort)
							print('nahhhh')
					else:
						searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,state__icontains= state, suburb__icontains=suburb,).order_by(sort)
						searchlist.extend(searchlist1)
				else:
					for a in propertytype1:
						if filterlist:
							if 'Swimming_pool' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Swimming_pool=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Garage' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Garage=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Balcony' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Balcony=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Outdoor_area' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Outdoor_area=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Undercover_parking' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Undercover_parking=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Shed' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Shed=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Fully_fenced' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Fully_fenced=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Outdoor_spa' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Outdoor_spa=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Tennis_court' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Tennis_court=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Ensuite' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Ensuite=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'DishWasher' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,DishWasher=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Study' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Study=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Built_in_robes' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Built_in_robes=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Alarm_system' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Alarm_system=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Broadband' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Broadband=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Floorboards' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Floorboards=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Gym' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Gym=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Rumpus_room' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Rumpus_room=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Workshop' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Workshop=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Air_conditioning' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Air_conditioning=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Solar_panels' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Solar_panels=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Heating' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Heating=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'High_energy_efficiency' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,High_energy_efficiency=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Water_tank' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Water_tank=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)
							elif 'Solar_hot_water' in filterlist:
								searchlist1 = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Solar_hot_water=True ,Property_type=a, state= state, suburb__icontains=suburb ).order_by(sort)
								searchlist.extend(searchlist1)


							else:
								searchlist = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Property_type=a, state= state, suburb__icontains=suburb).order_by(sort)
								print('nahhhh')
						else:
							searchlist = category.objects.all().filter(Bedrooms__gte = bedminsearch, Bedrooms__lte = bedmaxsearch, Price__gte = priceminsearch, Price__lte = pricemaxsearch,Property_type=a, state= state, suburb__icontains=suburb).order_by(sort)
							print('okayyyyy')

			print('propertytype1 is', propertytype1)

	pagin = list(dict.fromkeys(searchlist))	# it'll remove duplicate from the generallist

	try:
	    user = User.objects.get(username=request.user.username)
	    saved = SavedSearch.objects.filter(user=request.user)
	    #print('saved is', saved)
	except User.DoesNotExist:
	    saved='None'
	   # print('saved is', saved)
	    pass

# 	print('lastttttt', saved)

	context = {'sort':sort, 'saved':saved, 'firstbedmin':firstbedmin, 'firstpropertytype':firstpropertytype, 'firstbedmax':firstbedmax, 'firstpricemax':firstpricemax, 'firstpricemin':firstpricemin, 'saved':saved,'mylist':mylist,'pagin':pagin, 'category1':category1,'generallist':generallist, 'bedminsearch':bedminsearch, 'bedmaxsearch':bedmaxsearch, 'priceminsearch':priceminsearch, 'pricemaxsearch':pricemaxsearch}


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
			#print('dataaaaaaaaaaaaaa', data)
			latitude = data['results'][0]['geometry']['location']['lat']
			longitude = data['results'][0]['geometry']['location']['lng']
			print('long ang lat',longitude, latitude)


			user = User.objects.get(username=request.user.username)
			qs.user = user
			qs.latitude = latitude
			qs.longitude = longitude

			qs.save()

			return render(request, 'post_success.html')
	else:
		form = PosterForm()
	qs = CountryDetails.objects.all()
	#qs = json.dumps(qs1)
	context = {"state": state, 'suburb':suburb, 'postcode':postcode, 'form':form, 'qs':qs}
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