from django.urls import path
from django.conf.urls import url, include
from . import views
from django.contrib.auth import views as auth_views
# from mysite.core import views as core_views
app_name='administrator'
urlpatterns = [
    path('', views.administrator, name="administrator" ),
	path('userposts/', views.userpostsview, name="userposts" ),
	path('deleteposts/', views.deletePost, name="deleteposts" ),
	path('viewdetails/', views.viewDetails, name="viewdetails" ),
	path('upload/', views.upload_csv, name="upload_csv" ),


]

