from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Sucursal(models.Model):
    nombre = models.CharField(max_length=200, primary_key=True)
    ciudad = models.CharField(max_length=200, null=False)

    def __str__(self):
        return self.nombre


class PerfilEmpleado(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    dni = models.CharField(max_length=8)  
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre