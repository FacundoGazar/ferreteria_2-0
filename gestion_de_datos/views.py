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
from django.contrib import messages

# Create your views here.
@super_user
def gestion_de_datos_view(request):
    return render(request, "gestion_de_datos/gestion_datos.html")
    
@super_user
def estadisticas_intercambios_view(request):
    fecha_inicio_str = request.GET.get('fecha_inicio')
    fecha_fin_str = request.GET.get('fecha_fin')

    graphic = None

    if fecha_inicio_str and fecha_fin_str:
        try:
            # Convertir a objetos de fecha
            fecha_inicio = datetime.strptime(fecha_inicio_str, '%d-%m-%Y').date()
            fecha_fin = datetime.strptime(fecha_fin_str, '%d-%m-%Y').date()

            # Obtener intercambios en el rango de fechas
            intercambios = Intercambio.objects.filter(estado="realizado", fecha__range=(fecha_inicio, fecha_fin))

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
        except ValueError:
            messages.error(request, 'Formato de fecha incorrecto. Use DD-MM-YYYY.')
    else:
        if not fecha_inicio_str:
            messages.error(request, 'Por favor, complete la fecha de inicio.')
        if not fecha_fin_str:
            messages.error(request, 'Por favor, complete la fecha de fin.')

    context = {
        'graphic': graphic,
        'fecha_inicio': fecha_inicio_str or '',
        'fecha_fin': fecha_fin_str or ''
    }
    return render(request, "gestion_de_datos/intercambios_por_sucursal.html", context)

@super_user
def estadisticas_intercambios_por_fecha_view(request):
    fecha_inicio_str = request.GET.get('fecha_inicio')
    fecha_fin_str = request.GET.get('fecha_fin')

    graphic = None

    if fecha_inicio_str and fecha_fin_str:
        try:
            # Convertir a objetos de fecha
            fecha_inicio = datetime.strptime(fecha_inicio_str, '%d-%m-%Y').date()
            fecha_fin = datetime.strptime(fecha_fin_str, '%d-%m-%Y').date()

            # Obtener intercambios en el rango de fechas
            intercambios = Intercambio.objects.filter(estado="realizado", fecha__range=(fecha_inicio, fecha_fin))

            if intercambios.exists():
                # Crear un DataFrame con los datos
                data = {
                    'Fecha': [intercambio.fecha for intercambio in intercambios]
                }
                df = pd.DataFrame(data)

                # Convertir la columna 'Fecha' a tipo datetime si no lo está
                df['Fecha'] = pd.to_datetime(df['Fecha'])

                # Contar intercambios por fecha y redondear a enteros
                intercambios_por_fecha = df['Fecha'].value_counts().sort_index().astype(int)

                 # Generar el gráfico de barras
                plt.figure(figsize=(12, 6))
                plt.bar(intercambios_por_fecha.index.strftime('%Y-%m-%d'), intercambios_por_fecha.values, color=['skyblue', 'orange', 'green', 'red'])
                plt.xlabel('Fecha', fontsize=12)
                plt.ylabel('Cantidad de Intercambios', fontsize=12)
                plt.title('Cantidad de Intercambios por Fecha', fontsize=14)
                plt.xticks(rotation=45, fontsize=10)
                plt.yticks(fontsize=10)
                plt.grid(True, axis='y', linestyle='--', linewidth=0.5, alpha=0.7)  # Añadir rejilla horizontal
                plt.tight_layout()

                # Convertir el gráfico a una imagen en formato base64
                buffer = io.BytesIO()
                plt.savefig(buffer, format='png')
                buffer.seek(0)
                image_png = buffer.getvalue()
                buffer.close()

                graphic = base64.b64encode(image_png).decode('utf-8')
        except ValueError:
            messages.error(request, 'Formato de fecha incorrecto. Use DD-MM-YYYY.')
    else:
        if not fecha_inicio_str:
            messages.error(request, 'Por favor, complete la fecha de inicio.')
        if not fecha_fin_str:
            messages.error(request, 'Por favor, complete la fecha de fin.')

    context = {
        'graphic': graphic,
        'fecha_inicio': fecha_inicio_str or '',
        'fecha_fin': fecha_fin_str or ''
    }
    return render(request, "gestion_de_datos/intercambios_por_fecha.html", context)

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

# Vista para estadísticas de intercambios por sucursal y fecha
@super_user
def estadisticas_intercambios_sucursal_fecha_view(request):
    # Obtener la sucursal seleccionada del formulario (si se envía)
    sucursal_seleccionada = request.GET.get('sucursal', None)

    fecha_inicio_str = request.GET.get('fecha_inicio')
    fecha_fin_str = request.GET.get('fecha_fin')

    graphic = None

    if sucursal_seleccionada and fecha_inicio_str and fecha_fin_str:
        try:
            # Convertir a objetos de fecha
            fecha_inicio = datetime.strptime(fecha_inicio_str, '%d-%m-%Y').date()
            fecha_fin = datetime.strptime(fecha_fin_str, '%d-%m-%Y').date()

            # Filtrar intercambios por sucursal y rango de fechas
            intercambios = Intercambio.objects.filter(
                producto_receptor__sucursal=sucursal_seleccionada,
                fecha__range=(fecha_inicio, fecha_fin),
                estado="realizado"
            )
   
            if intercambios.exists():
                # Crear un DataFrame con los datos
                data = {
                    'Fecha': [intercambio.fecha.strftime('%d-%m-%Y') for intercambio in intercambios],
                    'Cantidad': [1 for _ in intercambios]  # Cada intercambio cuenta como uno
                }
                df = pd.DataFrame(data)
    
                # Agrupar por fecha y sumar las cantidades
                df = df.groupby('Fecha').sum().reset_index()

                # Generar el gráfico
                fig, ax = plt.subplots()
                ax.bar(df['Fecha'], df['Cantidad'], color=['skyblue', 'orange', 'green', 'red'])
                ax.set_xlabel('Fecha')
                ax.set_ylabel('Cantidad de Intercambios')
                ax.set_title(f'Cantidad de Intercambios para {sucursal_seleccionada} por fecha')

                # Convertir el gráfico a una imagen en formato base64
                buffer = io.BytesIO()
                plt.xticks(rotation=45)
                plt.tight_layout()
                fig.savefig(buffer, format='png')
                buffer.seek(0)
                image_png = buffer.getvalue()
                buffer.close()

                graphic = base64.b64encode(image_png).decode('utf-8')
        except ValueError:
            messages.error(request, 'Formato de fecha incorrecto. Use DD-MM-YYYY.')
    else:
        if not sucursal_seleccionada:
            messages.error(request, 'Por favor, seleccione una sucursal.')
        if not fecha_inicio_str:
            messages.error(request, 'Por favor, complete la fecha de inicio.')
        if not fecha_fin_str:
            messages.error(request, 'Por favor, complete la fecha de fin.')

    context = {
        'graphic': graphic,
        'fecha_inicio': fecha_inicio_str or '',
        'fecha_fin': fecha_fin_str or '',
        'sucursal_seleccionada': sucursal_seleccionada,
    }
    return render(request, "gestion_de_datos/intercambios_sucursal_fecha.html", context)
    
@super_user
def estadisticas_generales_view(request):
    return render(request, "gestion_de_datos/estadisticas_generales.html")
