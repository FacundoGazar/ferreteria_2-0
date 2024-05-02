from django.urls import path
from django.contrib.auth import views as auth_views
from gestion_de_usuarios import views

urlpatterns = [
    path("", views.registrar, name='registrar'),
    path("registrar/", views.register, name='register'),
]