from django.urls import path
from . import views
from searchstocks.dash_apps.finished_apps import example

urlpatterns = [
    path('', views.search_stock, name="search_stock")
]