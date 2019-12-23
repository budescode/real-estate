from rest_framework import serializers
from index.models import Poster

class PosterSerializer(serializers.ModelSerializer):
	class Meta:
		model = Poster
		exclude = []