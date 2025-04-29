from django.contrib import admin
from django.urls import path
from fire import views
from fire.views import HomePageView, ChartView, PieCountbySeverity, LineCountbyMonth, MultilineIncidentTop3Country, BarChartData, DoughnutChartData

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
]