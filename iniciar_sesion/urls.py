from django.urls import path
from . import views

urlpatterns = [
    path("", views.iniciar_sesion_view, name='iniciar_sesion'),
]