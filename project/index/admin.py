from django.contrib import admin
from .models import Poster, PropertyType, Price, SavedSearch, PosterRent


admin.site.register(PropertyType)
admin.site.register(Price)




class PosterAdmin(admin.ModelAdmin):
	list_display = ['user','id_user', 'created', 'active']

admin.site.register(Poster, PosterAdmin)
admin.site.register(SavedSearch)
admin.site.register(PosterRent)