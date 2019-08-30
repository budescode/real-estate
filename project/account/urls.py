from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
# from django.contrib.auth.views import login, logout
from django.views.generic.base import TemplateView
from django.contrib.auth import views
from . import views
from django.contrib.auth import views as auth_views



from django.contrib.auth.views import PasswordResetView

from django.urls import path


app_name = "account"
urlpatterns = [

	path('logout/', views.logout_page, name='logout'),
	path('register/', views.register, name='register'),
	path('profile/', views.profile, name="profile" ),
	path('upgrade/', views.Upgrade, name="upgrade" ),
	path('register_success/', views.registration_success, name='registration_success'),
	path('change_password/', views.change_password, name='change_password'),
	path('login/', views.login_Page, name='login'),
	path('change_password_confirm/', views.change_password_confirm, name='change_password_confirm'),
	path('<slug:pk>', views.change_password_code, name='change_password_code'),
	path('change_password_success/', views.change_password_success, name='change_password_success'),




]







