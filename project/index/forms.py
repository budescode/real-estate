from django.contrib.auth.models import User
from django import forms
from .models import Poster, Seeker

class PosterForm(forms.ModelForm):
	class Meta:
		model = Poster
		exclude = ['']
class SeekerForm(forms.ModelForm):
	class Meta:
		model = Seeker
		exclude = ['']
