from django.db import models
from django.contrib.auth.models import User

class PerfilCliente(models.Model):
    ciudad = models.CharField(max_length=100)
    edad = models.IntegerField()
    usuario = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    contrasenia = models.CharField(max_length=100)

  
