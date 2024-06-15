from django.db import models
from django.contrib.auth.models import User

class PerfilCliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ciudad = models.CharField(max_length=100)
    edad = models.IntegerField()
    monto_disponible = models.IntegerField(default=3000)

    def __str__(self):
        return self.user.username
