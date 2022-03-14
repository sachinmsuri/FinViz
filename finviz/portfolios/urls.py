from django.urls import path
from . import views
from portfolios.dash_apps import portfolios

urlpatterns = [
    path('portfolios',  views.create_portfolio ,name="portfolios")
    ]