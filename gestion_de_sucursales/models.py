from django.db import models

# Create your models here.

class Sucursal(models.Model):
    nombre = models.CharField(max_length=200, primary_key=True)
    ciudad = models.CharField(max_length=200, null=False)

    def __str__(self):
        return self.nombre
