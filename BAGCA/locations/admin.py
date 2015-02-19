from django.contrib import admin
from locations.models import Locations

class LocationsAdmin(admin.ModelAdmin):

    list_display = ('location', )

    search_fields = ['location']

admin.site.register(Locations, LocationsAdmin)