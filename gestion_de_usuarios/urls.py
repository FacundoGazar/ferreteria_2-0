from django.urls import path
from django.contrib.auth import views as auth_views
from gestion_de_usuarios import views

urlpatterns = [
    path("", views.registrar, name='registrar'),
    path("registrar/", views.register, name='register'),
    path("ver_perfil/<str:username>/", views.ver_perfil, name='ver_perfil'),
    path("ver_perfil/<str:username>/", views.ver_perfil, name='ver_perfil_cliente'),
    path("ver_perfil/<str:username>/", views.ver_perfil, name='ver_perfil_admin'),
    path("ver_perfil/<str:username>/", views.ver_perfil, name='ver_perfil_empleado'),
    path("modificar_perfil/<str:username>/", views.modificar_perfil, name='modificar_perfil'),
]