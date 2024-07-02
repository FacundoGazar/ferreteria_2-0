from django.contrib import admin
from .models import PagoServicio, Servicio, Tarjeta,ConfiguracionServicio

# Register your models here.
admin.site.register(PagoServicio)
admin.site.register(Servicio)
admin.site.register(Tarjeta)
admin.site.register(ConfiguracionServicio)