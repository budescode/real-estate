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
	
	# path('register-seeker/', views.register_seeker, name="register_seeker" ),
	# path('register-poster/', views.register_poster, name="register_poster" ),
	# path('post/', views.post, name="post" ),
	# path('login/', views.login_page, name="login" ),
	# path('loginpage/', views.login_view, name="login_view" ),
	# path('logout/', views.logout_page, name="logout_page" ),
	# path('filter/', views.search_field, name="search_field" ),


]



