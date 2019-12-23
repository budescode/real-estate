from rest_framework import generics
from administrator.models import CountryDetails
from administrator.api.serializers import CountryDetailsSerializer
from rest_framework import permissions

permission_classes = [permissions.AllowAny]
class CountryDetailsListView(generics.ListAPIView):
	lookup_field = 'pk'
	serializer_class = CountryDetailsSerializer
	def get_queryset(self):
		return CountryDetails.objects.all()