from django.shortcuts import render
from django.views.generic import TemplateView
import json
from .models import FireStation
from fire.models import Locations, Incident, FireStation
from django.db import connection
from django.http import JsonResponse
from django.db.models.functions import ExtractMonth
from django.db.models import Count
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Locations, Incident, FireStation, Firefighters, FireTruck, WeatherConditions
from datetime import datetime
from django.contrib import messages

class HomePageView(TemplateView):
    template_name = 'home.html'

class ChartView(TemplateView):
    template_name = 'chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any additional context data for your chart here
        return context

    def get_queryset(self, *args, **kwargs):
        pass

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
    fire_stations = [
        {
            'name': 'Puerto Princesa Fire Station',
            'lat': 9.7407,
            'lng': 118.7314,
            'address': 'Rizal Avenue, Puerto Princesa City',
            'type': 'station'
        },
        {
            'name': 'El Nido Fire Station',
            'lat': 11.1927,
            'lng': 119.3859,
            'address': 'Balinsasayaw Road, El Nido',
            'type': 'station'
        },
        {
            'name': 'Coron Fire Station',
            'lat': 11.9986,
            'lng': 120.2043,
            'address': 'National Highway, Coron',
            'type': 'station'
        },
        {
            'name': "Brooke's Point Fire Station",
            'lat': 8.7814,
            'lng': 117.8340,
            'address': 'Municipal Compound, Brookes Point',
            'type': 'station'
        },
        {
            'name': 'Roxas Fire Station',
            'lat': 10.3157,
            'lng': 119.3359,
            'address': 'Municipal Fire Station, Roxas',
            'type': 'station'
        }
    ]
    
    # Add fire incidents data
    fire_incidents = [
        {
            'name': 'Residential Fire',
            'lat': 9.7500,
            'lng': 118.7400,
            'address': 'San Pedro, Puerto Princesa City',
            'type': 'incident',
            'date': '2024-01-15',
            'status': 'Resolved',
            'severity': 'Medium'
        },
        {
            'name': 'Commercial Building Fire',
            'lat': 11.1800,
            'lng': 119.3900,
            'address': 'El Nido Town Proper',
            'type': 'incident',
            'date': '2024-01-20',
            'status': 'Active',
            'severity': 'High'
        }
    ]
    
    return render(request, 'jqvmap.html', {
        'fire_stations': json.dumps(fire_stations),
        'fire_incidents': json.dumps(fire_incidents)
    })

class HomePageView(TemplateView):
    model = Locations
    context_object_name = 'home'
    template_name = "home.html"

class ChartView(TemplateView):
    template_name = 'chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self, *args, **kwargs):
        pass

def PieCountbySeverity(request): 
    query = '''SELECT severity_level, COUNT(*) as count FROM fire_incident GROUP BY severity_level;''' 
    data = {}
    with connection.cursor() as cursor: 
        cursor.execute(query)
        rows = cursor.fetchall()
    
    if rows: 
        # Construct the dictionary with severity level as keys and count as values 
        data = {severity: count for severity, count in rows}
    else:
        data = {}
    return JsonResponse(data)

def LineCountbyMonth(request):
    current_year = datetime.now().year
    result = {month: 0 for month in range(1, 13)}
    incidents_per_month = Incident.objects.filter(date_time__year=current_year) \
        .values_list('date_time', flat=True)

    # Counting the number of incidents per month
    for date_time in incidents_per_month:
        month = date_time.month
        result[month] += 1
        
    # If you want to convert month numbers to month names, you can use a dictionary mapping
    month_names = {
        1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
        7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
        }
    
    result_with_month_names = {
        month_names[int(month)]: count for month, count in result.items()}
    
    return JsonResponse(result_with_month_names)

def MultilineIncidentTop3Country(request):
    query ='''
    SELECT fl.country,strftime('%m', fi.date_time) AS month,COUNT(fi.id) AS incident_count 
    FROM fire_incident fi 
    JOIN fire_locations fl ON fi.location_id = fl.id WHERE fl.country 
    IN (SELECT fl_top.country FROM fire_incident fi_top 
        JOIN fire_locations fl_top ON fi_top.location_id = fl_top.id 
        WHERE strftime('%Y', fi_top.date_time) = strftime('%Y', 'now') 
        GROUP BY fl_top.country 
        ORDER BY COUNT(fi_top.id) DESC LIMIT 3 ) 
        AND strftime('%Y', fi.date_time) = strftime('%Y', 'now') 
        GROUP BY fl.country, month 
        ORDER BY fl.country, month; '''
    
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        
    # Initialize a dictionary to store the result
    result = {}
    
    # Initialize a set of months from January to December
    months = set(str(i).zfill(2) for i in range(1, 13))

    # Loop through the query results
    for row in rows:
        country = row[0]
        month = row[1]
        total_incidents = row[2]
        # If the country is not in the result dictionary initialize it with all months set to zero
        if country not in result:
            result[country] = {month: 0 for month in months}
            
            # Update the incident count for the corresponding month
        result[country][month] = total_incidents

    # Ensure there are always 3 countries in the result
    while len(result) < 3:
    # Placeholder name for missing countries
        missing_country = f"Country {len(result) + 1}"
        result[missing_country] = {month: 0 for month in months}

    for country in result:
        result[country] = dict(sorted(result[country].items()))
        
    return JsonResponse(result)

# def multipleBarbySeverity(request):
#     query = '''
#     SELECT fi.severity_level, strftime('%m', fi.date_time) AS month, COUNT(fi.id) AS incident_count
#     FROM fire_incident fi
#     GROUP BY fi.severity_level, month
#     '''
    
#     with connection.cursor() as cursor:
#         cursor.execute(query)
#         rows = cursor.fetchall()
    
#     result = {}
#     months = set(str(i).zfill(2) for i in range(1, 13))
    
#     for row in rows:
#         level = str(row[0]) # Ensure the severity level is a string
#         month = row[1]
#         total_incidents = row[2]
        
#         if level not in result:
#             result[level] = {month: 0 for month in months}
            
#         result[level][month] = total_incidents
        
#     # Sort months within each severity level
#     for level in result:
#         result[level] = dict(sorted(result[level].items()))
    
#     return JsonResponse(result)


def BarChartData(request):
    # Example: Number of incidents per month for the current year
    current_year = datetime.now().year
    incidents = Incident.objects.filter(date_time__year=current_year)
    data = incidents.annotate(month=ExtractMonth('date_time')).values('month').annotate(count=Count('id')).order_by('month')
    # Prepare data for Chart.js
    labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    values = [0] * 12
    for entry in data:
        month_idx = entry['month'] - 1
        values[month_idx] = entry['count']
    return JsonResponse({
        "labels": labels,
        "values": values,
        "label": "Incidents"
    })

def DoughnutChartData(request):
    # Ensure all three severity levels are always present
    severity_levels = ["Major", "Minor", "Moderate"]
    counts = {level: 0 for level in severity_levels}
    data = Incident.objects.values('severity_level').annotate(count=Count('id'))
    for entry in data:
        level = entry['severity_level']
        if level in counts:
            counts[level] = entry['count']
    return JsonResponse({
        "labels": severity_levels,
        "values": [counts["Major"], counts["Minor"], counts["Moderate"]]
    })

# Location Views
class LocationListView(ListView):
    model = Locations
    template_name = 'fire/location_list.html'
    context_object_name = 'locations'

class LocationCreateView(CreateView):
    model = Locations
    template_name = 'fire/location_form.html'
    fields = ['name', 'latitude', 'longitude', 'address', 'city', 'country']
    success_url = reverse_lazy('location-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Location added!")
        return response

class LocationUpdateView(UpdateView):
    model = Locations
    template_name = 'fire/location_form.html'
    fields = ['name', 'latitude', 'longitude', 'address', 'city', 'country']
    success_url = reverse_lazy('location-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Location updated!")
        return response

class LocationDeleteView(DeleteView):
    model = Locations
    template_name = 'fire/location_confirm_delete.html'
    success_url = reverse_lazy('location-list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Location deleted!")
        return super().delete(request, *args, **kwargs)

# Similar view classes for Incident
class IncidentListView(ListView):
    model = Incident
    template_name = 'fire/incident_list.html'
    context_object_name = 'incidents'

# Incident CRUD Views
class IncidentCreateView(CreateView):
    model = Incident
    template_name = 'fire/incident_form.html'
    fields = ['location', 'date_time', 'severity_level', 'description']
    success_url = reverse_lazy('incident-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Incident added!")
        return response

class IncidentUpdateView(UpdateView):
    model = Incident
    template_name = 'fire/incident_form.html'
    fields = ['location', 'date_time', 'severity_level', 'description']
    success_url = reverse_lazy('incident-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Incident updated!")
        return response

class IncidentDeleteView(DeleteView):
    model = Incident
    template_name = 'fire/incident_confirm_delete.html'
    success_url = reverse_lazy('incident-list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Incident deleted!")
        return super().delete(request, *args, **kwargs)

# FireStation CRUD Views
class FireStationListView(ListView):
    model = FireStation
    template_name = 'fire/firestation_list.html'
    context_object_name = 'firestations'

class FireStationCreateView(CreateView):
    model = FireStation
    template_name = 'fire/firestation_form.html'
    fields = ['name', 'address', 'city', 'country']
    success_url = reverse_lazy('firestation-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Fire Station added!")
        return response

class FireStationUpdateView(UpdateView):
    model = FireStation
    template_name = 'fire/firestation_form.html'
    fields = ['name', 'address', 'city', 'country']
    success_url = reverse_lazy('firestation-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Fire Station updated!")
        return response

class FireStationDeleteView(DeleteView):
    model = FireStation
    template_name = 'fire/firestation_confirm_delete.html'
    success_url = reverse_lazy('firestation-list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Fire Station deleted!")
        return super().delete(request, *args, **kwargs)

# Firefighter CRUD Views
class FirefighterListView(ListView):
    model = Firefighters
    template_name = 'fire/firefighter_list.html'
    context_object_name = 'firefighters'

class FirefighterCreateView(CreateView):
    model = Firefighters
    template_name = 'fire/firefighter_form.html'
    fields = ['name', 'rank', 'experience_level', 'station']
    success_url = reverse_lazy('firefighter-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Firefighter added!")
        return response

class FirefighterUpdateView(UpdateView):
    model = Firefighters
    template_name = 'fire/firefighter_form.html'
    fields = ['name', 'rank', 'experience_level', 'station']
    success_url = reverse_lazy('firefighter-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Firefighter updated!")
        return response

class FirefighterDeleteView(DeleteView):
    model = Firefighters
    template_name = 'fire/firefighter_confirm_delete.html'
    success_url = reverse_lazy('firefighter-list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Firefighter deleted!")
        return super().delete(request, *args, **kwargs)

# FireTruck CRUD Views
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import FireTruck

class FireTruckListView(ListView):
    model = FireTruck
    template_name = 'fire/firetruck_list.html'
    context_object_name = 'firetrucks'

class FireTruckCreateView(CreateView):
    model = FireTruck
    template_name = 'fire/firetruck_form.html'
    fields = ['truck_number', 'model', 'capacity', 'station']
    success_url = reverse_lazy('firetruck-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Fire Truck added!")
        return response

class FireTruckUpdateView(UpdateView):
    model = FireTruck
    template_name = 'fire/firetruck_form.html'
    fields = ['truck_number', 'model', 'capacity', 'station']
    success_url = reverse_lazy('firetruck-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Fire Truck updated!")
        return response

class FireTruckDeleteView(DeleteView):
    model = FireTruck
    template_name = 'fire/firetruck_confirm_delete.html'
    success_url = reverse_lazy('firetruck-list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Fire Truck deleted!")
        return super().delete(request, *args, **kwargs)

# WeatherConditions CRUD Views
class WeatherCreateView(CreateView):
    model = WeatherConditions
    template_name = 'fire/weather_form.html'
    fields = ['incident', 'temperature', 'humidity', 'wind_speed', 'weather_description']
    success_url = reverse_lazy('weather-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Weather added!")
        return response

class WeatherUpdateView(UpdateView):
    model = WeatherConditions
    template_name = 'fire/weather_form.html'
    fields = ['incident', 'temperature', 'humidity', 'wind_speed', 'weather_description']
    success_url = reverse_lazy('weather-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Weather updated!")
        return response

class WeatherDeleteView(DeleteView):
    model = WeatherConditions
    template_name = 'fire/weather_confirm_delete.html'
    success_url = reverse_lazy('weather-list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Weather deleted!")
        return super().delete(request, *args, **kwargs)

# Similar view classes for WeatherConditions
class WeatherListView(ListView):
    model = WeatherConditions
    template_name = 'fire/weather_list.html'
    context_object_name = 'weather_conditions'
