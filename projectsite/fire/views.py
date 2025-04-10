from django.shortcuts import render
from django.views.generic.list import ListView
from fire.models import Locations, Incident, FireStation

def map_station(request):
    fireStations = FireStation.objects.values('name', 'latitude', 'longitude')
    
    for fs in fireStations:
        fs['latitude'] = float(fs['latitude'])
        fs['longitude'] = float(fs['longitude'])
    
    fireStations_list = list(fireStations)

    context = (
        {
            'fireStations': fireStations_list,
        }
    )
    return render(request, 'map_station.html', context)

class HomePageView(ListView):
    model = Locations
    context_object_name = 'home'
    template_name = "home.html"
