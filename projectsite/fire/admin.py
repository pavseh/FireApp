from django.contrib import admin

from .models import Incident, Locations, Firefighters, FireStation, FireTruck, WeatherConditions

admin.site.register(Incident)
admin.site.register(Locations)
admin.site.register(Firefighters)
admin.site.register(FireStation)
admin.site.register(FireTruck)
admin.site.register(WeatherConditions)
