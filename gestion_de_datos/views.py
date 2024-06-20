import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from gestion_de_servicios.models import PagoServicio
from intercambiar_producto.models import Intercambio
import pandas as pd
from iniciar_sesion import *

# Create your views here.
@super_user
def gestion_de_datos_view(request):
    return render(request, "gestion_de_datos/gestion_datos.html")
    
@super_user
def estadisticas_intercambios_view(request):
    fecha_inicio_str = request.GET.get('fecha_inicio', '01-01-2024')
    fecha_fin_str = request.GET.get('fecha_fin', '31-12-2024')

    # Convertir a objetos de fecha
    fecha_inicio = datetime.strptime(fecha_inicio_str, '%d-%m-%Y').date()
    fecha_fin = datetime.strptime(fecha_fin_str, '%d-%m-%Y').date()

    # Obtener intercambios en el rango de fechas
    intercambios = Intercambio.objects.filter(fecha__range=(fecha_inicio, fecha_fin))

    if intercambios.exists():
        # Crear un DataFrame con los datos
        data = {
            'Sucursal': [intercambio.producto_receptor.sucursal.nombre for intercambio in intercambios],
            'Cantidad': [1 for _ in intercambios]  # Cada intercambio cuenta como uno
        }
        df = pd.DataFrame(data)

        # Agrupar por sucursal y contar los intercambios
        df = df.groupby('Sucursal').sum().reset_index()

        # Generar el gráfico de torta
        fig, ax = plt.subplots()
        pie = ax.pie(df['Cantidad'], labels=df['Sucursal'], autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax.set_title('Proporción de Intercambios por Sucursal')

        # Agregar la cantidad de intercambios al lado del gráfico
        total_intercambios = sum(df['Cantidad'])
        legend_labels = [f'{sucursal}: {cantidad} intercambios' for sucursal, cantidad in zip(df['Sucursal'], df['Cantidad'])]
        ax.legend(pie[0], legend_labels, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

        # Convertir el gráfico a una imagen en formato base64
        buffer = io.BytesIO()
        plt.tight_layout()
        fig.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        graphic = base64.b64encode(image_png).decode('utf-8')
    else:
        graphic = None  # No hay datos para mostrar

    context = {
        'graphic': graphic,
        'fecha_inicio': fecha_inicio_str,
        'fecha_fin': fecha_fin_str
    }
    return render(request, "gestion_de_datos/estadisticas_intercambios.html", context)

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
