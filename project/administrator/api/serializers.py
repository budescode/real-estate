from rest_framework import serializers
from administrator.models import CountryDetails

class CountryDetailsSerializer(serializers.ModelSerializer):
	class Meta:
		model = CountryDetails
		fields = ['state', 'suburb']