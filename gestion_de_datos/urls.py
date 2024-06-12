from django.urls import path
from .views import *

urlpatterns = [
    path("", gestion_de_datos_view, name='gestion_de_datos'),
    path("estadisticas_intercambios/", estadisticas_intercambios_view, name='estadisticas_intercambios'),
    path("estadisticas_servicios/", estadisticas_servicios_view, name='estadisticas_servicios'),
    path("estadisticas_generales/", estadisticas_generales_view, name='estadisticas_generales'),
]