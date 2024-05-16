from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import ModificarContrasenaView

urlpatterns = [
    path("", views.iniciar_sesion_view, name='iniciar_sesion'),
    path("cerrar_sesion/", views.cerrar_sesion_view, name="cerrar_sesion"),

    path("reiniciar_contrasena/", 
         auth_views.PasswordResetView.as_view(template_name="authenticate/reset_contrasena.html"), 
         name="reset_password"),

    path("reiniciar_contrasena_envio/", 
         auth_views.PasswordResetDoneView.as_view(template_name="authenticate/reset_contrasena_envio.html"), 
         name="password_reset_done"),

    path("reiniciar/<uidb64>/<token>/", 
         auth_views.PasswordResetConfirmView.as_view(template_name="authenticate/reset_contrasena_token.html"), 
         name="password_reset_confirm"),

    path("reiniciar_contrasena_exitoso", 
         auth_views.PasswordResetCompleteView.as_view(template_name="authenticate/reset_contrasena_exitoso.html"), 
         name="password_reset_complete"),
    
    path("modificar_contrasena/", 
         ModificarContrasenaView.as_view(template_name="authenticate/modificar_contrasena.html"),
         name="modificar_contrasena"),
    
    path("modificar_contrasena_exitoso/",
         views.modificar_contrasena_exitoso,
         name="modificar_contrasena_exitoso"),
]
