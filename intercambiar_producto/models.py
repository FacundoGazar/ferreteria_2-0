from django.db import models
from django.contrib.auth.models import User
from mis_productos.models import Producto

class Intercambio(models.Model):
    ESTADOS = (
        ('pendiente', 'Pendiente'),
        ('aceptado', 'Aceptado'),
        ('rechazado', 'Rechazado'),
        ('realizado', 'Realizado'),
        ('cancelado', 'Cancelado'),
        ('ausente', 'Ausente'),
    )


    producto_solicitante = models.ForeignKey(Producto, related_name='intercambios_solicitados', on_delete=models.CASCADE)
    producto_receptor = models.ForeignKey(Producto, related_name='intercambios_recibidos', on_delete=models.CASCADE)
    cliente_solicitante = models.ForeignKey(User, related_name='solicitudes_realizadas', on_delete=models.CASCADE)
    cliente_receptor = models.ForeignKey(User, related_name='solicitudes_recibidas', on_delete=models.CASCADE)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='pendiente')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    dia = models.CharField(max_length=20, blank=True)
    fecha = models.DateField(null=True, blank=True)
    horario = models.IntegerField()
    def save(self, *args, **kwargs):
        if not self.dia:  
            self.dia = self.producto_receptor.dias  
        super().save(*args, **kwargs) 
    def __str__(self):
        return f"{self.producto_solicitante} <-> {self.producto_receptor} ({self.dia}) ({self.fecha}) ({self.horario}) ({self.estado})"