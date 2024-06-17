import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from gestion_de_servicios.models import PagoServicio
import pandas as pd
from iniciar_sesion import *


# Create your views here.
@super_user
def gestion_de_datos_view(request):
    return render(request, "gestion_de_datos/gestion_datos.html")
def estadisticas_intercambios_view(request):    
    return render(request, "gestion_de_datos/estadisticas_intercambios.html")

@super_user
def estadisticas_servicios_view(request):    
    # Rango de fechas - ejemplo: del 1 de enero de 2023 al 31 de diciembre de 2023
    fecha_inicio = request.GET.get('fecha_inicio', '01-01-2024')
    fecha_fin = request.GET.get('fecha_fin', '31-12-2024')

    # Convertir a objetos de fecha
    fecha_inicio = datetime.strptime(fecha_inicio, '%d-%m-%Y').date()
    fecha_fin = datetime.strptime(fecha_fin, '%d-%m-%Y').date()

    # Obtener pagos en el rango de fechas
    pagos = PagoServicio.objects.filter(fecha__range=(fecha_inicio, fecha_fin))

    # Crear un DataFrame con los datos
    data = {
        'Fecha': [pago.fecha.strftime('%d-%m-%Y') for pago in pagos],
        'Monto': [pago.monto for pago in pagos]
    }
    df = pd.DataFrame(data)
    
    # Agrupar por fecha y sumar los montos
    df = df.groupby('Fecha').sum().reset_index()

    # Generar el gráfico
    fig, ax = plt.subplots()
    ax.bar(df['Fecha'], df['Monto'])
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Monto acumulado')
    ax.set_title('Monto acumulado por fecha')

    # Convertir el gráfico a una imagen en formato base64
    buffer = io.BytesIO()
    plt.xticks(rotation=45)
    plt.tight_layout()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    context = {
        'graphic': graphic,
        'fecha_inicio': fecha_inicio.strftime('%d-%m-%Y'),
        'fecha_fin': fecha_fin.strftime('%d-%m-%Y')
    }
    return render(request, "gestion_de_datos/estadisticas_servicios.html", context)

@super_user
def estadisticas_generales_view(request):
    return render(request, "gestion_de_datos/estadisticas_generales.html")