from django.urls import path, include
from . import views
from .views import alert_data, fuel_data, demand_graph, solar_graph, wind_graph, energy_data,processed_data

urlpatterns = [
    path('', views.main),
    path('alert_data/', alert_data, name='alert'),
    path('fuel_data/', fuel_data, name='fuel'),
    path('demand_graph/', demand_graph, name='demand'),
    path('solar_graph/', solar_graph, name='solar'),
    path('wind_graph/', wind_graph, name='wind'),
    ##지워라
    path('energy_data/', energy_data, name='energy'),
    path('pro/', processed_data, name='pro')
]