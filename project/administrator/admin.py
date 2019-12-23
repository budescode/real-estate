from django.contrib import admin

# Register your models here.
from .models import CountryDetails


class CountryDetailsAdmin(admin.ModelAdmin):
	exclude = []
	list_display = ['suburb', 'state', 'postcode']
	search_fields = ['suburb', 'state', 'postcode']
admin.site.register(CountryDetails, CountryDetailsAdmin)