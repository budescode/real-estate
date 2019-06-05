from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from index.models import Poster
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse,JsonResponse

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
	return render(request, 'administrator/index.html', context)

@login_required(login_url='/account/login/')
def userpostsview(request):
	user_post = Poster.objects.all()
	context = {"user_post":user_post}
	return render(request, 'administrator/userposts.html', context)

def deletePost(request):
	post_pk = request.POST.get("post_pk")
	post = Poster.objects.get(id_user=post_pk)
	# post.delete()
	print(post.user)
	return JsonResponse({"msg":"deleted"})

def viewDetails(request):
	post_pk = request.POST.get("post_pk")
	post = Poster.objects.get(id_user=post_pk)
	image = post.image
	img = serializers.serialize('json', [post])
	print(post)
	return JsonResponse({"msg":img})



