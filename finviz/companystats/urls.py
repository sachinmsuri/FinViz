from django.urls import path
from . import views
from companystats.dash_apps import companystats


# Create your views here.

urlpatterns = [
    path('companystats', views.companystats, name="companystats")
]