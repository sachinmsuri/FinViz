from django.urls import path
from . import views
from annualreports.dash_apps import annualreports


# Create your views here.

urlpatterns = [
    path('annualreports', views.annualreports, name="annualreports")
]