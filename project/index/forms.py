from django.contrib.auth.models import User
from django import forms
from .models import PosterRent, Poster
from administrator.models import CountryDetails



class PosterForm(forms.ModelForm):
	class Meta:
		model = Poster
		exclude = ['user']
		widgets = {
		'unit': forms.Textarea(attrs={'rows':1, 'cols':1}),
		'street_number': forms.Textarea(attrs={'rows':1, 'cols':1}),
		'street_name': forms.Textarea(attrs={'rows':1, 'cols':1}),
		'suburb': forms.Textarea(attrs={'rows':1, 'cols':1}),
		'postcode': forms.Textarea(attrs={'rows':1, 'cols':1}),
		'state': forms.Textarea(attrs={'rows':1, 'cols':1}),
		}

	def clean_postcode(self):
		postcode = self.cleaned_data.get('postcode')

		qs = CountryDetails.objects.filter(postcode=postcode)
		if not qs.exists():
			raise forms.ValidationError("Enter a valid postcode")
		return postcode

	def clean_suburb(self):
		suburb = self.cleaned_data.get('suburb')

		qs = CountryDetails.objects.filter(suburb=suburb)
		if not qs.exists():
			raise forms.ValidationError("Enter a valid suburb")
		return suburb


	def clean_state(self):
		state = self.cleaned_data.get('state')

		qs = CountryDetails.objects.filter(state=state)
		if not qs.exists():
			raise forms.ValidationError("Enter a valid state")
		return state

class PosterRentForm(forms.ModelForm):
	class Meta:
		model = PosterRent
		exclude = ['user']
		widgets = {
		'unit': forms.Textarea(attrs={'rows':1, 'cols':1}),
		'street_number': forms.Textarea(attrs={'rows':1, 'cols':1}),
		'street_name': forms.Textarea(attrs={'rows':1, 'cols':1}),
		'suburb': forms.Textarea(attrs={'rows':1, 'cols':1}),
		'postcode': forms.Textarea(attrs={'rows':1, 'cols':1}),
		'state': forms.Textarea(attrs={'rows':1, 'cols':1}),
		}

	def clean_postcode(self):
		postcode = self.cleaned_data.get('postcode')

		qs = CountryDetails.objects.filter(postcode=postcode)
		if not qs.exists():
			raise forms.ValidationError("Enter a valid postcode")
		return postcode

	def clean_suburb(self):
		suburb = self.cleaned_data.get('suburb')

		qs = CountryDetails.objects.filter(suburb=suburb)
		if not qs.exists():
			raise forms.ValidationError("Enter a valid suburb")
		return suburb


	def clean_state(self):
		state = self.cleaned_data.get('state')

		qs = CountryDetails.objects.filter(state=state)
		if not qs.exists():
			raise forms.ValidationError("Enter a valid state")
		return state



# class SeekerForm(forms.ModelForm):
# 	class Meta:
# 		model = Seeker
# 		exclude = ['']
