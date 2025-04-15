from django.shortcuts import render
from django.views.generic import TemplateView
import json
from .models import FireStation

class HomePageView(TemplateView):
    template_name = 'home.html'

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

def jqvmap_view(request):
    # Sample fire station data for Palawan
    fire_stations = [
        {
            'name': 'Puerto Princesa Fire Station',
            'lat': 9.7407,
            'lng': 118.7314,
            'address': 'Rizal Avenue, Puerto Princesa City'
        },
        {
            'name': 'El Nido Fire Station',
            'lat': 11.1927,
            'lng': 119.3859,
            'address': 'Balinsasayaw Road, El Nido'
        },
        {
            'name': 'Coron Fire Station',
            'lat': 11.9986,
            'lng': 120.2043,
            'address': 'National Highway, Coron'
        },
        {
            'name': "Brooke's Point Fire Station",
            'lat': 8.7814,
            'lng': 117.8340,
            'address': 'Municipal Compound, Brookes Point'
        }
    ]
    
    return render(request, 'jqvmap.html', {'fire_stations': json.dumps(fire_stations)})
