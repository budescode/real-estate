from django.urls import path
from django.conf.urls import url, include
from . import views
from django.contrib.auth import views as auth_views
# from mysite.core import views as core_views
app_name='home'
urlpatterns = [
    path('', views.home, name="home" ),
	path('about/', views.about, name="about" ),
	path('contact/', views.contact, name="contact" ),
	path('blog/', views.blog, name="blog" ),
	path('sell/', views.post, name="post" ),
	path('rent/', views.rent_view, name="rent" ),
    path('index/<slug:id>/<slug:category>/', views.details, name="details" ),

	path('mypost/', views.Mypost, name="mypost" ),
	path('delete/<slug:id>/', views.Delete, name="delete" ),
	path('edit/<slug:id>/', views.Edit, name="edit" ),
	path('edit/<slug:id>/', views.Edit, name="edit" ),
	path('filterstate/', views.filterDetails, name="filterDetails" ),
	path('filter_search/', views.filter_search, name="filter_search" ),
    path('savesearch/', views.savesearch, name="savesearch" ),
    path('mysavedsearch/', views.mysavedsearch, name="mysavedsearch" ),
    path('deletesavesearch/', views.deletesavesearch, name="deletesavesearch" ),



]



