from django.urls import path, include
from django.conf.urls import url
from . import views


app_name = 'index_api'
#from index.api.views import SchoolCreateView, AddressCreateView, StudentCreateView, SubjectCreateView ,SchoolListView, AddressListView, StudentListView, SubjectListView


urlpatterns = [
path('posterlistapi/', views.PosterListView.as_view(), name='posterapilist'),
]