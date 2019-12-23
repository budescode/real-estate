from django.contrib import admin
from .models import Poster, PropertyType, Price, SavedSearch, PosterRent , SavedHeaders, SavedDetail, saveReport


admin.site.register(PropertyType)
admin.site.register(Price)




class PosterAdmin(admin.ModelAdmin):
	list_display = ['user','id_user', 'created', 'active', 'state', 'suburb', 'postcode']
	search_fields = ['id_user', 'state', 'suburb', 'postcode']

admin.site.register(Poster, PosterAdmin)
admin.site.register(SavedSearch)
admin.site.register(PosterRent)
admin.site.register(SavedHeaders)
admin.site.register(SavedDetail)
admin.site.register(saveReport)

