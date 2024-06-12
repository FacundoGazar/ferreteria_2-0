from django.db import models
from django.contrib.auth.models import User 

class PagoServicio(models.Model):
    id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=20, decimal_places=2) 
    fecha = models.DateField(null=True, blank=True)


    def __str__(self):
        return str(self.id) 