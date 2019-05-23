from django.contrib.auth.models import User
from django import forms
from .models import Poster

class PosterForm(forms.ModelForm):
	class Meta:
		model = Poster
		exclude = ['user']
# class SeekerForm(forms.ModelForm):
# 	class Meta:
# 		model = Seeker
# 		exclude = ['']
