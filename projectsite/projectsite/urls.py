from django.contrib import admin
from django.urls import path
from fire import views
from fire.views import (
    HomePageView, ChartView, PieCountbySeverity, LineCountbyMonth, 
    MultilineIncidentTop3Country, BarChartData, DoughnutChartData,
    # Location views
    LocationListView, LocationCreateView, LocationUpdateView, LocationDeleteView,
    # Incident views
    IncidentListView, IncidentCreateView, IncidentUpdateView, IncidentDeleteView,
    # FireStation views
    FireStationListView, FireStationCreateView, FireStationUpdateView, FireStationDeleteView,
    # Firefighter views
    FirefighterListView, FirefighterCreateView, FirefighterUpdateView, FirefighterDeleteView,
    # FireTruck views
    FireTruckListView, FireTruckCreateView, FireTruckUpdateView, FireTruckDeleteView,
    # WeatherCondition views
    WeatherListView, WeatherCreateView, WeatherUpdateView, WeatherDeleteView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', HomePageView.as_view(), name='home'),
    path('stations', views.map_station, name='map-station'),
    path('maps/jqvmap.html', views.jqvmap_view, name='jqvmap'),
    path('chart/', ChartView.as_view(), name='chart'),
    path('chart/pieChart/', PieCountbySeverity, name='pie-chart'),
    path('chart/lineChart/', LineCountbyMonth, name='line-chart'),
    path('chart/multiBarChart/', MultilineIncidentTop3Country, name='multi-bar-chart'),
    path('chart/barChart/', BarChartData, name='bar-chart'),
    path('chart/doughnutChart/', DoughnutChartData, name='doughnut-chart'),
    
    # Location URLs
    path('locations/', LocationListView.as_view(), name='location-list'),
    path('locations/create/', LocationCreateView.as_view(), name='location-create'),
    path('locations/<int:pk>/update/', LocationUpdateView.as_view(), name='location-update'),
    path('locations/<int:pk>/delete/', LocationDeleteView.as_view(), name='location-delete'),
    
    # Incident URLs
    path('incidents/', IncidentListView.as_view(), name='incident-list'),
    path('incidents/create/', IncidentCreateView.as_view(), name='incident-create'),
    path('incidents/<int:pk>/update/', IncidentUpdateView.as_view(), name='incident-update'),
    path('incidents/<int:pk>/delete/', IncidentDeleteView.as_view(), name='incident-delete'),
    
    # FireStation URLs
    path('firestations/', FireStationListView.as_view(), name='firestation-list'),
    path('firestations/create/', FireStationCreateView.as_view(), name='firestation-create'),
    path('firestations/<int:pk>/update/', FireStationUpdateView.as_view(), name='firestation-update'),
    path('firestations/<int:pk>/delete/', FireStationDeleteView.as_view(), name='firestation-delete'),
    
    # Firefighter URLs
    path('firefighters/', FirefighterListView.as_view(), name='firefighter-list'),
    path('firefighters/create/', FirefighterCreateView.as_view(), name='firefighter-create'),
    path('firefighters/<int:pk>/update/', FirefighterUpdateView.as_view(), name='firefighter-update'),
    path('firefighters/<int:pk>/delete/', FirefighterDeleteView.as_view(), name='firefighter-delete'),
    
    # FireTruck URLs
    path('firetrucks/', FireTruckListView.as_view(), name='firetruck-list'),
    path('firetrucks/create/', FireTruckCreateView.as_view(), name='firetruck-create'),
    path('firetrucks/<int:pk>/update/', FireTruckUpdateView.as_view(), name='firetruck-update'),
    path('firetrucks/<int:pk>/delete/', FireTruckDeleteView.as_view(), name='firetruck-delete'),
    
    # Weather URLs
    path('weather/', WeatherListView.as_view(), name='weather-list'),
    path('weather/create/', WeatherCreateView.as_view(), name='weather-create'),
    path('weather/<int:pk>/update/', WeatherUpdateView.as_view(), name='weather-update'),
    path('weather/<int:pk>/delete/', WeatherDeleteView.as_view(), name='weather-delete'),
]