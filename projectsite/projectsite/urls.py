from django.contrib import admin
from django.urls import path

from fire.views import HomePageView
from fire import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', HomePageView.as_view(), name='home'),

]
