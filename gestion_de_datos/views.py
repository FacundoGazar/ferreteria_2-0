import matplotlib.pyplot as plt
import io
import base64
import json

from datetime import datetime,date
from django.shortcuts import render
from django.http import HttpResponse
from gestion_de_servicios.models import *
from intercambiar_producto.models import Intercambio,Venta
from intercambiar_producto.models import Venta
import pandas as pd
from iniciar_sesion import *
from django.contrib import messages
from django.db.models import Sum
from django.db.models import Count
from django.http import JsonResponse


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
def servicios_tiempo_view(request):    
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    graphic = None
    if fecha_inicio and fecha_fin:
        try:
            fecha_inicio = datetime.strptime(fecha_inicio, '%d-%m-%Y').date()
            fecha_fin = datetime.strptime(fecha_fin, '%d-%m-%Y').date()

            pagos = PagoServicio.objects.filter(fecha__range=(fecha_inicio, fecha_fin))

            data = {
                'Fecha': [pago.fecha.strftime('%d-%m-%Y') for pago in pagos],
                'Monto': [pago.monto for pago in pagos]
            }
            df = pd.DataFrame(data)
            
            df = df.groupby('Fecha').sum().reset_index()

            fig, ax = plt.subplots()
            ax.bar(df['Fecha'], df['Monto'])
            ax.set_xlabel('Fecha')
            ax.set_ylabel('Monto acumulado')
            ax.set_title('Monto acumulado por fecha')

            buffer = io.BytesIO()
            plt.xticks(rotation=45)
            plt.tight_layout()
            fig.savefig(buffer, format='png')
            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()

            graphic = base64.b64encode(image_png)
            graphic = graphic.decode('utf-8')
        except ValueError:
            messages.error(request, 'Formato de fecha incorrecto. Use DD-MM-YYYY.')
    else:
        if not fecha_inicio:
            messages.error(request, 'Por favor, complete la fecha de inicio.')
        if not fecha_fin:
            messages.error(request, 'Por favor, complete la fecha de fin.')

    context = {
        'graphic': graphic,
        'fecha_inicio': fecha_inicio or '',
        'fecha_fin': fecha_fin or ''
    }
    return render(request, "gestion_de_datos/servicios_tiempo.html", context)


@super_user
def servicios_ciudad_view(request):
    sucursales = Sucursal.objects.all()
    servicios = Servicio.objects.filter(estado="publicado")
    graphic = None

    if servicios.exists():
        try:            
                data = {
                    'Ciudad': [servicio.ciudad for servicio in servicios],
                    'Monto': [servicio.pago.monto for servicio in servicios]
                }
                df = pd.DataFrame(data)
            
                df = df.groupby('Ciudad').sum().reset_index()

                fig, ax = plt.subplots()
                ax.bar(df['Ciudad'], df['Monto'])
                ax.set_xlabel('Ciudad')
                ax.set_ylabel('Monto acumulado')
                ax.set_title('Monto acumulado por ciudad')

                buffer = io.BytesIO()
                plt.xticks(rotation=45)
                plt.tight_layout()
                fig.savefig(buffer, format='png')
                buffer.seek(0)
                image_png = buffer.getvalue()
                buffer.close()

                graphic = base64.b64encode(image_png)
                graphic = graphic.decode('utf-8')
        except ValueError:
            messages.error(request, 'Hubo un error procesando los datos.')
    else:
        messages.error(request, 'No hay servicios.')

    context = {
        'graphic': graphic,
        "servicios": servicios,
        "sucursales": sucursales
    }
    return render(request, "gestion_de_datos/servicios_ciudad.html", context)

@super_user
def servicios_ciudad_tiempo_view(request):        
    ciudad_seleccionada = request.GET.get('ciudad', None)    
    sucursales = Sucursal.objects.all()
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    graphic = None
    if fecha_inicio and fecha_fin and ciudad_seleccionada:
        try:
            fecha_inicio = datetime.strptime(fecha_inicio, '%d-%m-%Y').date()
            fecha_fin = datetime.strptime(fecha_fin, '%d-%m-%Y').date()

            servicios = Servicio.objects.filter(ciudad=ciudad_seleccionada,estado="publicado", pago__fecha__range=(fecha_inicio, fecha_fin))
            
            if servicios.exists():
                data = {
                    'Fecha': [servicio.pago.fecha.strftime('%d-%m-%Y') for servicio in servicios],
                    'Ciudad': [servicio.ciudad for servicio in servicios],
                    'Monto': [servicio.pago.monto for servicio in servicios]
                }
                df = pd.DataFrame(data)
                
                df = df.groupby('Fecha').sum().reset_index()

                fig, ax = plt.subplots()
                ax.bar(df['Fecha'], df['Monto'])
                ax.set_xlabel('Fecha')
                ax.set_ylabel('Monto acumulado')
                ax.set_title(f'Monto acumulado por fecha para la ciudad {ciudad_seleccionada}')

                buffer = io.BytesIO()
                plt.xticks(rotation=45)
                plt.tight_layout()
                fig.savefig(buffer, format='png')
                buffer.seek(0)
                image_png = buffer.getvalue()
                buffer.close()

                graphic = base64.b64encode(image_png)
                graphic = graphic.decode('utf-8')
        except ValueError:
            messages.error(request, 'Formato de fecha incorrecto. Use DD-MM-YYYY.')
    else:
        if not fecha_inicio:
            messages.error(request, 'Por favor, complete la fecha de inicio.')
        if not fecha_fin:
            messages.error(request, 'Por favor, complete la fecha de fin.')
        if not ciudad_seleccionada:
            messages.error(request, 'Por favor, complete la ciudad.')

    context = {
        'graphic': graphic,
        'fecha_inicio': fecha_inicio or '',
        'fecha_fin': fecha_fin or '',        
        'ciudad_seleccionada': ciudad_seleccionada,
        "sucursales": sucursales
    }
    return render(request, "gestion_de_datos/servicios_ciudad_tiempo.html", context)

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
def estadisticas_intercambios_por_categoria_view(request):
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
                    'Categoria': [intercambio.producto_solicitante.categoria for intercambio in intercambios]
                }
                df = pd.DataFrame(data)

                # Contar intercambios por categoría
                intercambios_por_categoria = df['Categoria'].value_counts().sort_index()

                # Calcular el porcentaje de intercambios por categoría
                total_intercambios = intercambios_por_categoria.sum()
                porcentajes = (intercambios_por_categoria / total_intercambios) * 100

                # Crear etiquetas con el nombre de la categoría y el porcentaje
                etiquetas = [f'{categoria} ({porcentaje:.1f}%)' for categoria, porcentaje in zip(intercambios_por_categoria.index, porcentajes)]

                # Generar el gráfico de barras
                plt.figure(figsize=(12, 6))
                plt.bar(etiquetas, intercambios_por_categoria.values, color=['skyblue', 'orange', 'green', 'red', 'purple', 'brown'])

                plt.xlabel('Categoría', fontsize=12)
                plt.ylabel('Cantidad de Intercambios', fontsize=12)
                plt.title('Cantidad de Intercambios por Categoría', fontsize=14)
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
    return render(request, "gestion_de_datos/intercambios_por_categoria.html", context)

@super_user
def estadisticas_intercambios_por_categoria_sucursal_view(request):
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

            # Obtener intercambios en el rango de fechas
            intercambios = Intercambio.objects.filter(producto_receptor__sucursal=sucursal_seleccionada,
                                                      estado="realizado", fecha__range=(fecha_inicio, fecha_fin))

            if intercambios.exists():
                # Crear un DataFrame con los datos
                data = {
                    'Categoria': [intercambio.producto_solicitante.categoria for intercambio in intercambios]
                }
                df = pd.DataFrame(data)

                # Contar intercambios por categoría
                intercambios_por_categoria = df['Categoria'].value_counts().sort_index()

                # Calcular el porcentaje de intercambios por categoría
                total_intercambios = intercambios_por_categoria.sum()
                porcentajes = (intercambios_por_categoria / total_intercambios) * 100

                # Crear etiquetas con el nombre de la categoría y el porcentaje
                etiquetas = [f'{categoria} ({porcentaje:.1f}%)' for categoria, porcentaje in zip(intercambios_por_categoria.index, porcentajes)]

                # Generar el gráfico de barras
                plt.figure(figsize=(12, 6))
                plt.bar(etiquetas, intercambios_por_categoria.values, color=['skyblue', 'orange', 'green', 'red', 'purple', 'brown'])

                plt.xlabel('Categoría', fontsize=12)
                plt.ylabel('Cantidad de Intercambios', fontsize=12)
                plt.title(f'Cantidad de Intercambios de la sucursal {sucursal_seleccionada} por Categoría', fontsize=14)
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
    return render(request, "gestion_de_datos/intercambios_por_categoria_sucursal.html", context)

@super_user
def estadisticas_generales_view(request):
    return render(request, "gestion_de_datos/estadisticas_generales.html")


# Tango
def ingresos_por_sucursal(request):
    if request.method == 'POST':
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')

        if fecha_inicio and fecha_fin:
            try:
                # Convertir fechas de string a objetos datetime
                fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
                fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')

                # Obtener todas las sucursales
                sucursales = Sucursal.objects.all()

                # Inicializar listas para almacenar los datos de ingresos por sucursal
                sucursales_nombres = []
                ingresos_por_sucursal = []

                # Si la fecha de fin es el día actual, ajustarla al día actual exacto
                if fecha_fin.date() == date.today():
                    fecha_fin = timezone.now()

                # Calcular ingresos por cada sucursal entre las fechas seleccionadas
                for sucursal in sucursales:
                    ingresos = Venta.objects.filter(sucursal=sucursal, fecha__range=[fecha_inicio, fecha_fin]).aggregate(Sum('monto_total'))['monto_total__sum']
                    ingresos = float(ingresos) if ingresos else 0.0
                    sucursales_nombres.append(sucursal.nombre)
                    ingresos_por_sucursal.append(ingresos)

                # Convertir listas a JSON para pasar a la plantilla
                data = {
                    'sucursales': sucursales_nombres,
                    'ingresos_por_sucursal': ingresos_por_sucursal,
                }
                return JsonResponse(data)

            except ValueError:
                messages.error(request, 'Formato de fecha incorrecto. Use el formato YYYY-MM-DD.')

        else:
            # Si no se seleccionaron fechas, mostrar mensaje de error
            messages.error(request, 'Por favor, seleccione un período de tiempo válido.')

    else:
        # Si la solicitud es GET, enviar mensaje informativo
        messages.info(request, 'Ingrese fecha de inicio y fin válidas para visualizar los ingresos por sucursal.')

    return render(request, 'gestion_de_datos/chart_ingresos_por_sucursal.html')

def ventas_por_sucursal(request):
    if request.method == 'POST':
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')

        if fecha_inicio and fecha_fin:
            try:
                # Convertir fechas de string a objetos datetime
                fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
                fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')

                # Obtener todas las sucursales
                sucursales = Sucursal.objects.all()

                # Inicializar listas para almacenar los datos de ventas por sucursal
                sucursales_nombres = []
                ventas_por_sucursal = []

                # Si la fecha de fin es el día actual, ajustarla al día actual exacto
                if fecha_fin.date() == date.today():
                    fecha_fin = timezone.now()

                # Calcular cantidad de ventas por cada sucursal entre las fechas seleccionadas
                for sucursal in sucursales:
                    ventas = Venta.objects.filter(sucursal=sucursal, fecha__range=[fecha_inicio, fecha_fin]).count()
                    sucursales_nombres.append(sucursal.nombre)
                    ventas_por_sucursal.append(ventas)

                # Convertir listas a JSON para pasar a la plantilla
                data = {
                    'sucursales': sucursales_nombres,
                    'ventas_por_sucursal': ventas_por_sucursal,
                }
                return JsonResponse(data)

            except ValueError:
                messages.error(request, 'Formato de fecha incorrecto. Use el formato YYYY-MM-DD.')

        else:
            # Si no se seleccionaron fechas, mostrar mensaje de error
            messages.error(request, 'Por favor, seleccione un período de tiempo válido.')

    else:
        # Si la solicitud es GET, enviar mensaje informativo
        messages.info(request, 'Ingrese fecha de inicio y fin válidas para visualizar las ventas por sucursal.')

    return render(request, 'gestion_de_datos/chart_ventas_por_sucursal.html')
    
def ingresos_por_mes(request):
    if request.method == 'POST':
        anio_seleccionado = request.POST.get('anio')

        if anio_seleccionado:
            try:
                # Convertir el año seleccionado a entero
                anio_seleccionado = int(anio_seleccionado)

                # Obtener los ingresos por mes para el año seleccionado
                ingresos_por_mes = Venta.objects.filter(fecha__year=anio_seleccionado) \
                                                .values('fecha__month') \
                                                .annotate(ingresos=Sum('monto_total')) \
                                                .order_by('fecha__month')

                meses = []
                ingresos_mensuales = [0] * 12  # Inicializar un array de 12 posiciones para cada mes

                # Mapear el número de mes a su nombre (opcional, depende de tus necesidades)
                nombres_meses = {
                    1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
                    5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
                    9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
                }

                # Sumar los ingresos por mes
                for ingreso in ingresos_por_mes:
                    mes = ingreso['fecha__month']
                    ingresos = ingreso['ingresos'] if ingreso['ingresos'] else 0
                    ingresos_mensuales[mes - 1] = float(ingresos)

                    # Guardar el nombre del mes para mostrar en el gráfico
                    meses.append(nombres_meses[mes])

                # Preparar datos para enviar como respuesta JSON
                data = {
                    'meses': meses,
                    'ingresos_mensuales': ingresos_mensuales,
                }

                # Renderizar la plantilla con los datos actuales
                print("Meses:", meses)
                print("Ingresos mensuales:", ingresos_mensuales)
                return JsonResponse(data)

            except ValueError:
                return JsonResponse({'error': 'El año seleccionado no es válido.'}, status=400)

        else:
            return JsonResponse({'error': 'Por favor, seleccione un año válido.'}, status=400)

    # Si la solicitud es GET, renderizar la plantilla con un rango predeterminado de años
    today = datetime.today()
    current_year = today.year
    return render(request, 'gestion_de_datos/chart_ingresos_por_tiempo.html', {'years': range(current_year, current_year - 11, -1)})

def ventas_por_mes(request):
    if request.method == 'POST':
        anio_seleccionado = request.POST.get('anio')

        if anio_seleccionado:
            try:
                # Convertir el año seleccionado a entero
                anio_seleccionado = int(anio_seleccionado)

                # Obtener las ventas por mes para el año seleccionado
                ventas_por_mes = Venta.objects.filter(fecha__year=anio_seleccionado) \
                                              .values('fecha__month') \
                                              .annotate(cantidad_ventas=Count('id')) \
                                              .order_by('fecha__month')

                meses = []
                ventas_mensuales = [0] * 12  # Inicializar un array de 12 posiciones para cada mes

                # Mapear el número de mes a su nombre (opcional, depende de tus necesidades)
                nombres_meses = {
                    1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
                    5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
                    9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
                }

                # Sumar las ventas por mes
                for venta in ventas_por_mes:
                    mes = venta['fecha__month']
                    cantidad_ventas = venta['cantidad_ventas'] if venta['cantidad_ventas'] else 0
                    ventas_mensuales[mes - 1] = cantidad_ventas

                    # Guardar el nombre del mes para mostrar en el gráfico
                    meses.append(nombres_meses[mes])

                # Preparar datos para enviar como respuesta JSON
                data = {
                    'meses': meses,
                    'ventas_mensuales': ventas_mensuales,
                }

                # Renderizar la plantilla con los datos actuales
                print("Meses:", meses)
                print("Ventas mensuales:", ventas_mensuales)
                return JsonResponse(data)

            except ValueError:
                return JsonResponse({'error': 'El año seleccionado no es válido.'}, status=400)

        else:
            return JsonResponse({'error': 'Por favor, seleccione un año válido.'}, status=400)

    # Si la solicitud es GET, renderizar la plantilla con un rango predeterminado de años
    today = datetime.today()
    current_year = today.year
    return render(request, 'gestion_de_datos/chart_ventas_por_tiempo.html', {'years': range(current_year, current_year - 11, -1)})


def ingresos_por_sucursal_tiempo(request):
    if request.method == 'POST':
        sucursal_id = request.POST.get('sucursal')
        anio_seleccionado = request.POST.get('anio')
        if sucursal_id and anio_seleccionado:
            try:
                # Convertir el año seleccionado a entero
                anio_seleccionado = int(anio_seleccionado)

                # Obtener las ventas por mes para la sucursal y el año seleccionados
                ingresos_por_mes_sucursal = Venta.objects.filter(fecha__year=anio_seleccionado, sucursal_id=sucursal_id) \
                                                        .values('fecha__month') \
                                                        .annotate(ingresos=Sum('monto_total')) \
                                                        .order_by('fecha__month')

                meses = []
                ingresos_mensuales = [0] * 12  # Inicializar un array de 12 posiciones para cada mes

                # Mapear el número de mes a su nombre
                nombres_meses = {
                    1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
                    5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
                    9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
                }

                # Sumar los ingresos por mes
                for ingreso in ingresos_por_mes_sucursal:
                    mes = ingreso['fecha__month']
                    ingresos = ingreso['ingresos'] if ingreso['ingresos'] else 0
                    ingresos_mensuales[mes - 1] = float(ingresos)

                    # Guardar el nombre del mes para mostrar en el gráfico
                    meses.append(nombres_meses[mes])

                # Preparar datos para enviar como respuesta JSON
                data = {
                    'meses': meses,
                    'ingresos_mensuales': ingresos_mensuales,
                }

                # Renderizar la plantilla con los datos actuales
                print("Meses:", meses)
                print("Ingresos mensuales:", ingresos_mensuales)
                return JsonResponse(data)

            except ValueError:
                return JsonResponse({'error': 'El año seleccionado no es válido.'}, status=400)

        else:
            return JsonResponse({'error': 'Por favor, seleccione una sucursal y un año válidos.'}, status=400)

    # Si la solicitud es GET, renderizar la plantilla con las sucursales y un rango predeterminado de años
    sucursales = Sucursal.objects.all()
    today = datetime.today()
    current_year = today.year
    return render(request, 'gestion_de_datos/chart_ingresos_sucursales_tiempo.html', {'sucursales': sucursales, 'years': range(current_year, current_year - 11, -1)})

def productos_mas_vendidos(request):
    if request.method == 'POST':
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')

        if fecha_inicio and fecha_fin:
            try:
                # Convertir fechas de string a objetos datetime
                fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
                fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')

                # Obtener los productos más vendidos en el rango de fechas
                productos_mas_vendidos = Venta.objects.filter(fecha__range=[fecha_inicio, fecha_fin]) \
                                                     .values('productos__nombre') \
                                                     .annotate(cantidad_vendida=Count('productos')) \
                                                     .order_by('-cantidad_vendida')[:5]

                productos = []
                for producto in productos_mas_vendidos:
                    productos.append({
                        'nombre': producto['productos__nombre'],
                        'cantidad_vendida': producto['cantidad_vendida']
                    })

                data = {
                    'productos': productos
                }

                return JsonResponse(data)

            except ValueError:
                return JsonResponse({'error': 'Las fechas ingresadas no son válidas.'}, status=400)
        else:
            return JsonResponse({'error': 'Por favor, seleccione un rango de fechas válido.'}, status=400)

    # Si la solicitud es GET, renderizar la plantilla
    return render(request, 'gestion_de_datos/chart_productos_mas_vendidos.html')

def relacion_intercambio_venta(request):
    # Obtener el total de intercambios en la base de datos
    total_intercambios = Intercambio.objects.count()

    # Obtener el total de ventas en la base de datos
    total_ventas_asociadas = Venta.objects.count()

    if total_intercambios == 0:
        ratio = 0
    else:
        ratio = total_ventas_asociadas / total_intercambios

    context = {
        'total_intercambios': total_intercambios,
        'total_ventas_asociadas': total_ventas_asociadas,
        'ratio': ratio
    }

    return render(request, 'gestion_de_datos/chart_intercambio_venta.html', context)