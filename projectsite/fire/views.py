from django.shortcuts import render
from django.views.generic.list import ListView
from fire.models import Locations, Incident


class HomePageView(ListView):
    model = Locations
    context_object_name = 'home'
    template_name = "home.html"
