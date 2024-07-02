from django.db import models
from django.contrib.auth.models import User 
from django.utils.text import slugify 
from gestion_de_sucursales.models import Sucursal 
from django.utils import timezone
from datetime import timedelta

class ConfiguracionServicio(models.Model):
    costo_publicacion = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    duracion_publicacion_dias = models.IntegerField(default=30)

    def __str__(self):
        return f"Configuración de Servicio"

    @classmethod
    def get_solo_instance(cls):
        # Obtener o crear la única instancia de ConfiguracionServicio
        instance, created = cls.objects.get_or_create(pk=1)
        return instance


class Tarjeta(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_apellido = models.CharField(max_length=100)
    numero = models.CharField(max_length=19)
    mes_vencimiento = models.IntegerField(null=True, blank=True)
    año_vencimiento = models.IntegerField(null=True, blank=True)
    cvv = models.CharField(max_length=3)
    saldo = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return str(self.id)
    

class PagoServicio(models.Model):
    id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=20, decimal_places=2) 
    fecha = models.DateField(null=True, blank=True)
    tarjeta = models.ForeignKey(Tarjeta, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.id) 
    
class Servicio(models.Model):
    ESTADOS = (
        ('pendiente', 'Pendiente'),   
        ('aceptado', 'Aceptado'),
        ('rechazado', 'Rechazado'),
        ('publicado', 'Publicado'),
    )
    id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='pendiente')
    ciudad = models.CharField(max_length=50, null=True, blank=True)
    imagen = models.ImageField(upload_to='imagenes/')
    descripcion = models.TextField(null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)    
    pago = models.ForeignKey(PagoServicio, on_delete=models.CASCADE, null=True, blank=True)
    fechaFin = models.DateField(null=True, blank=True)
    visible = models.BooleanField(default=True)  

    def save(self, *args, **kwargs):
        self.fechaFin = timezone.now().date() + timedelta(days=30)
        self.slug = slugify(str(self.id) + "-" + str(self.imagen))
        return super().save(*args , **kwargs)

    def __str__(self):
        return str(self.id) 
    
    @property
    def puede_eliminar(self):
        if self.fechaFin:
            return self.fechaFin <= timezone.now().date()
        return False
    
