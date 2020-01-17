from rest_framework import generics
from index.models import Poster
from index.api.serializers import PosterSerializer
from rest_framework import permissions
from .pagination import PostLimitOffsetPagination
from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination
    )
from django.db.models import Q

permission_classes = [permissions.AllowAny]
class PosterListView(generics.ListAPIView):
	lookup_field = 'pk'
	serializer_class = PosterSerializer
	pagination_class = PostLimitOffsetPagination
	def get_queryset(self):
	    name = self.request.GET.get('name')
	    pricemin = self.request.GET.get('pricemin')
	    pricemax = self.request.GET.get('pricemax')
	    bedmin = self.request.GET.get('bedmin')
	    bedmax = self.request.GET.get('bedmax')
	    propertytype = self.request.GET.get('propertytype')
	    print(propertytype.replace('%', ' ').replace('-', '&'), 'propertytype')
	    qs = Poster.objects.all()
	    if name is not None:
	        if name == 'Any':
	            if propertytype == 'Any':
	                qs2 = qs.filter(
                    Bedrooms__gte =  int(bedmin),
                    Bedrooms__lte =  int(bedmax),
                    Price__gte =  int(pricemin),
                    Price__lte = int(pricemax)
    	            )
	                qs = qs2
	                return qs
	            else:
	                propertyty = propertytype.replace('%', ' ').replace('-', '&').split(',')
	                qs2 = qs.filter(
	                Bedrooms__gte =  int(bedmin),
	                Bedrooms__lte =  int(bedmax),
	                Price__gte =  int(pricemin),
	                Price__lte = int(pricemax),
	                Property_type__in = propertyty
                    )
	                qs = qs2
	                return qs
	        else:
	            if propertytype == 'Any':
	                qs1 = ['ACT', 'NT', 'NT']
	                qs11 = ['BARTON', 'DARWIN', 'PARAP']
	                state = []
	                suburb = []
	                name = name.replace(' ', '')
	                name = name.split('_')
	                for i in name:
	                    a = i.find('-') #gets the position of -, it seperates the state and suburbs
	                    state.append(i[a+1:])
	                    suburb.append(i[0:a])
	                qs2 = qs.filter(
                        suburb__in = suburb,
                        state__in =  state,
                        #Property_type__in = ['Villa'],
                        Bedrooms__gte =  int(bedmin),
                        Bedrooms__lte =  int(bedmax),
                        Price__gte =  int(pricemin),
                        Price__lte = int(pricemax)
        	            )
	                print('state isss', name, pricemin, pricemax, bedmin, bedmax)
	                qs = qs2
	                return qs
	            else:
	                propertyty = propertytype.replace('%', ' ').replace('-', '&').split(',')
	                qs1 = ['ACT', 'NT', 'NT']
	                qs11 = ['BARTON', 'DARWIN', 'PARAP']
	                state = []
	                suburb = []
	                name = name.replace(' ', '')
	                name = name.split('_')
	                for i in name:
	                    a = i.find('-') #gets the position of -, it seperates the state and suburbs
	                    state.append(i[a+1:])
	                    suburb.append(i[0:a])
	                qs2 = qs.filter(
                        suburb__in = suburb,
                        state__in =  state,
                        #Property_type__in = ['Villa'],
                        Bedrooms__gte =  int(bedmin),
                        Bedrooms__lte =  int(bedmax),
                        Price__gte =  int(pricemin),
                        Price__lte = int(pricemax),
                        Property_type__in = propertyty
        	            )
	                print('state isss', name, pricemin, pricemax, bedmin, bedmax)
	                qs = qs2
	                return qs
	    else:
	       qs2 = qs.filter(
                Bedrooms__gte =  int(bedmin),
                Bedrooms__lte =  int(bedmax),
                Price__gte =  int(pricemin),
                Price__lte = int(pricemax)
	            )
	       print('noname')
	       qs = qs2
	       return qs
	    return qs



permission_classes = [permissions.AllowAny]
class DetailView(generics.ListAPIView):
	lookup_field = 'pk'
	serializer_class = PosterSerializer
	pagination_class = PostLimitOffsetPagination
	def get_queryset(self):
	    id = self.request.GET.get('id')
	    qs = Poster.objects.all()
	    if id is not None:
	        qs1 = qs.filter(id_user=id)
	        qs = qs1
	        return qs
	    return qs





