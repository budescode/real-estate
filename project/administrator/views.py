from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from index.models import Poster, PosterRent
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse,JsonResponse
import csv, io
from django.contrib import messages
from .models import CountryDetails
import requests

# Create your views here.
@login_required(login_url='/account/login/')
def administrator(request):
	user_total = User.objects.all().count()
	user_total_percentage = (user_total/10000)*100

	post_active_total = Poster.objects.filter(active=True).count()
	post_active_total_percentage = (post_active_total/10000)*100

	post_disabled_total = Poster.objects.filter(active=False).count()
	post_disabled_total_percentage = (post_disabled_total/10000)*100

	total_post = Poster.objects.all().count()
	total_post_percentage = (total_post/10000)*100
	context = {'total_post_percentage':total_post_percentage, 'post_disabled_total_percentage':post_disabled_total_percentage,'post_active_total_percentage':post_active_total_percentage, 'user_total_percentage':user_total_percentage, 'user_total':user_total, 'post_active_total':post_active_total, 'post_disabled_total':post_disabled_total, 'total_post':total_post}
	return render(request, 'Administrator/index.html', context)

@login_required(login_url='/account/login/')
def userpostsview(request):
	user_post = Poster.objects.all()
	context = {"user_post":user_post}
	return render(request, 'Administrator/userposts.html', context)

def deletePost(request):
	post_pk = request.POST.get("post_pk")
	post = Poster.objects.get(id_user=post_pk)
	post.delete()
	# print(post.user)
	return JsonResponse({"msg":"deleted"})

def viewDetails(request):
	post_pk = request.POST.get("post_pk")
	post = Poster.objects.get(id_user=post_pk)
	data = serializers.serialize('json', [post])
	print(post_pk)
	return JsonResponse({"data":data})

def upload_csv(request):

# 	qs = Poster.objects.all()
# 	for i in qs:
# 		i.image = 'https://www.pythonanywhere.com/user/anandrathi/files/home/anandrathi/RE/real-estate/project/media_cdn/banner.jpg'
# 		i.save()
	if request.method == 'GET':
		return render(request, 'Administrator/upload_csv.html')
	csv_file = request.FILES['file']
	if not csv_file.name.endswith('.csv'):
		messages.error(request, "This is not a csv file")
	data_set = csv_file.read().decode('UTF-8')
	io_string = io.StringIO(data_set)
	next(io_string)
	user1 = request.user.username
	user = User.objects.get(username=user1)
	for column in csv.reader(io_string, delimiter=',', quotechar="|"):
# 		address = column[41] + ' ' + column[40] + ' ' +  column[42] + ' ' + column[39] + ' '+ ', Australia'
# 		print('address is', address)
# 		r = requests.post('https://maps.googleapis.com/maps/api/geocode/json?address=address&key=AIzaSyBfZ86mdGX5E7o4PGSB7ct22axSb_JzVTY')
# 		latitude = r.json()['results'][0]['geometry']['location']['lat']
# 		longitude = r.json()['results'][0]['geometry']['location']['lng']
# 		print('the datas areee',r.json())
# 		print('address is',column[41], column[40], column[42], column[39])

		Poster.objects.create(user=request.user,
		# _, created = Poster.objects.create(
			# user = request.user,
			Property_type = column[3],
			Price = column[4],
			Bedrooms = column[5],
			Bathrooms = column[6],
			Car_spaces = column[7],
			postcode = column[38],
			state = column[39],
			suburb = column[42],
			unit = column[43],
			land_size = column[37],
			street_name = column[40],
 			street_number = column[41],
			image = column[44],
# 			image1 = column[45],
			plan = column[36],
			)
	context = {}
	return HttpResponse("done")

