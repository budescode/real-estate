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
	path('mypost/', views.Mypost, name="mypost" ),


]



