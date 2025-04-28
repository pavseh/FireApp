from django.contrib import admin
from django.urls import path
from fire import views
from fire.views import HomePageView, ChartView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', HomePageView.as_view(), name='home'),
    path('stations', views.map_station, name='map-station'),
    path('maps/jqvmap.html', views.jqvmap_view, name='jqvmap'),
    path('chart/', ChartView.as_view(), name='chart'),
]
