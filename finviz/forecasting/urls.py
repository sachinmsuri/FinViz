from django.urls import path
from . import views
from forecasting.dash_apps import forecasting

urlpatterns = [
    path('forecasting', views.forecasting, name="forecasting")
]