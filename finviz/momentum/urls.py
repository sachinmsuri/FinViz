from django.urls import path
from . import views
from momentum.dash_apps import momentum

urlpatterns = [
    path('momentum', views.momentum, name="momentum")
]