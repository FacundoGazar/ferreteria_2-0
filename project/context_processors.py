from gestion_de_sucursales.models import Sucursal


def agregar_datos_a_contexto(request):
    sucursales = Sucursal.objects.all()
    estados_list = ["Nuevo - Sin uso", "Usado", "Restaurado", "Para reparar", "Para piezas", "Con defectos leves"]
    categorias_list = ["Herramientas", "Construcción", "Ferretería general", "Electricidad", "Fontanería", "Jardín"]
    return {
        'sucursales': sucursales,
        'estados_list': estados_list,
        'categorias_list': categorias_list,
    }
