from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Producto(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=100, blank=True)
    categoria = models.CharField(max_length=100, blank=True)
    horario_disponibilidad = models.CharField(max_length=100, blank=True)
    sucursal = models.CharField(max_length=100, blank=True)
    imagen_principal = models.ImageField(upload_to='productos/')
    imagen_extra1 = models.ImageField(upload_to='imagenes/', blank=True, null=True)
    imagen_extra2 = models.ImageField(upload_to='imagenes/', blank=True, null=True)
    imagen_extra3 = models.ImageField(upload_to='imagenes/', blank=True, null=True)
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre + "-" + str(self.imagen_principal))
        return super().save(*args , **kwargs)

    def __str__(self):
        return self.nombre
