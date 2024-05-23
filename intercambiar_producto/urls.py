from django.urls import path
from .views import *

urlpatterns = [
    path("<slug:slug_intercambio>/", intercambiar_listar_mis_productos_view, name='intercambio listado'),
    path("<slug:slug_intercambio>/realizar_intercambio", realizar_intercambio_view, name='realizar intercambio'),
]