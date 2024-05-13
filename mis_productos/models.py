from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import post_delete
from django.dispatch import receiver
from gestion_de_sucursales.models import Sucursal 

class Producto(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    dias = models.CharField(max_length=100, default="")
    horario_inicio = models.CharField(max_length=100)
    horario_fin = models.CharField(max_length=100)
    sucursal = models.CharField(max_length=100)
    imagen_principal = models.ImageField(upload_to='imagenes/')
    imagen_extra1 = models.ImageField(upload_to='imagenes/', blank=True, null=True)
    imagen_extra2 = models.ImageField(upload_to='imagenes/', blank=True, null=True)
    imagen_extra3 = models.ImageField(upload_to='imagenes/', blank=True, null=True)
    slug = models.SlugField(null=True, blank=True)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre + "-" + str(self.imagen_principal))
        return super().save(*args , **kwargs)

    def __str__(self):
        return self.nombre
    
