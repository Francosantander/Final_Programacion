from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.shortcuts import render
from .models import Pelicula, Salas, Proyeccion, Butacas
from .serializers import PeliculaSerializer, SalaSerializer, ButacaSerializer
from .serializers import ProyeccionSerializer
from rest_framework.decorators import api_view
import datetime as dt


def principal(request):
    return render(request, "principal.html")


# Endpoint Peliculas
# Listado de peliculas en un rando de +- 15 dias
@api_view(['GET'])
def pelis(request):
    now = dt.datetime.now()
    rango = dt.timedelta(days=15)
    peliculas = Pelicula.objects.filter(fechaFinalizacion__gte=(now - rango),
                                        fechaComienzo__lte=(now + rango))
    peliculas_serializer = PeliculaSerializer(peliculas, many=True)
    return JsonResponse(peliculas_serializer.data, safe=False,
                        status=status.HTTP_200_OK)


# Arreglar
# Endpoint pelicula especifica + rango de fecha
@api_view(['GET'])
def peli_detail(request, nombre, inicio, fin):
    try:
        peli = Pelicula.objects.get(nombre=nombre, fechaComienzo=inicio,
                                    fechaFinalizacion=fin)
        pelicula_serializer = PeliculaSerializer(peli)
        return JsonResponse(pelicula_serializer.data,
                            status=status.HTTP_200_OK)
    except Pelicula.DoesNotExist:
        return JsonResponse({'Mensaje': 'La pelicula especificada no existe o los rangos de fechas ingresados son incorrecto'},
                            status=status.HTTP_404_NOT_FOUND)


# Lista de peliculas especificando un rango de fechas
@api_view(['GET'])
def peli_date_detail(request, inicio, fin):
    try:
        peli = Pelicula.objects.get(fechaComienzo__gte=inicio,
                                    fechaFinalizacion__lte=fin)
        pelicula_serializer = PeliculaSerializer(peli, many=True)
        return JsonResponse(pelicula_serializer.data,
                            status=status.HTTP_200_OK)
    except Pelicula.DoesNotExist:
        return JsonResponse({'Mensaje': 'Los rangos de fechas ingresados son incorrecto'},
                            status=status.HTTP_404_NOT_FOUND)


# Endpoint de las Salas
# Endpoint para obetener la lista de salas o crear una
@api_view(['GET', 'POST'])
def salas_list(request):
    if request.method == 'GET':
        salas = Salas.objects.all()
        salas_serializer = SalaSerializer(salas, many=True)
        return JsonResponse(salas_serializer.data, safe=False,
                            status=status.HTTP_200_OK)

    elif request.method == 'POST':
        salas_data = JSONParser().parse(request)
        salas_serializer = SalaSerializer(data=salas_data)
        if salas_serializer.is_valid():
            salas_serializer.save()
            return JsonResponse(salas_serializer.data,
                                status=status.HTTP_201_CREATED)
        return JsonResponse(salas_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


# Endpoint de obtencion, modificacion o eliminacion de una sala
@api_view(['GET', 'PUT', 'DELETE'])
def sala_detail(request, pk):
    try:
        sala = Salas.objects.get(pk=pk)

        if request.method == 'GET':
            sala_serializer = SalaSerializer(sala)
            return JsonResponse(sala_serializer.data,
                                status=status.HTTP_200_OK)

        elif request.method == 'PUT':
            sala_data = JSONParser().parse(request)
            sala_serializer = SalaSerializer(sala, data=sala_data)
            if sala_serializer.is_valid():
                sala_serializer.save()
                return JsonResponse(sala_serializer.data)
            return JsonResponse(sala_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            sala.delete()
            return JsonResponse({'Mensaje': 'La sala se elimino correctamente'},
                                status=status.HTTP_204_NO_CONTENT)

    except Salas.DoesNotExist:
        return JsonResponse({'Mensaje': 'La sala especificada no existe'},
                            status=status.HTTP_404_NOT_FOUND)


# Valido los datos de la sala
def validar_sala(sala_serializer, sala_data):
    pass


# Endpoint Proyecciones
# Endpoint Proyecciones activas
@api_view(['GET'])
def proyecciones_list(request):
    if request.method == 'GET':
        proye = Proyeccion.objects.get(estado=True)
        proye_serializer = ProyeccionSerializer(proye, many=True)
        return JsonResponse(proye_serializer.data, safe=False,
                            status=status.HTTP_200_OK)
    elif request.method == 'POST':
        proye_data = JSONParser().parse(request)
        proye_serializer = ProyeccionSerializer(data=proye_data)
        if proye_serializer.is_valid():
            proye_serializer.save()
            return validar_proyeccion(proye_data, proye_serializer)
        return JsonResponse(proye_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


# Endpoint GET + Rango de fechas
# Arreglar
@api_view(['GET'])
def proyeccionesRango(request, inicio, fin):
    try:
        # Ver si poner filter o get
        proye = Proyeccion.objects.get(fecha_inicio__gte=inicio,
                                       fecha_fin__lte=fin, estado=True)
        proye_serializer = ProyeccionSerializer(proye, many=True)
        return JsonResponse(proye_serializer.data,
                            status=status.HTTP_200_OK)
    except Proyeccion.DoesNotExist:
        return JsonResponse({'Mensaje': 'Los rangos de fechas ingresados son incorrecto'},
                            status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def modificarProyeccion(request, pk):
    try:
        proye = Proyeccion.objects.get(pk=pk)
        # Traigo una proyeccion en particular
        if request.method == 'GET':
            proyecciones = Proyeccion.objects.all(pk=pk)
            proye_serializer = ProyeccionSerializer(proyecciones, many=True)
            return JsonResponse(proye_serializer.data, safe=False,
                                status=status.HTTP_200_OK)
        elif request.method == 'PUT':
            proye_data = JSONParser().parse(request)
            proye_serializer = ProyeccionSerializer(proye, data=proye_data)
            if proye_serializer.is_valid():
                proye_serializer.save()
                return validar_proyeccion(proye_data, proye_serializer)
            return JsonResponse(proye_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
    except Butacas.DoesNotExist:
        return JsonResponse({'Mensaje': 'La butaca especificada no existe'},
                            status=status.HTTP_404_NOT_FOUND)


# Get + proyeccion + fecha
@api_view(['GET'])
def proyePeliRango(request, pelicula, fecha):
    pass


# Terminar de hacer la validacion
def validar_proyeccion(proye_data, proye_serializer):
    pass


# Endpoint Butacas reservadas
@api_view(['GET'])
def butacas_list(request):
    if request.method == 'GET':
        butacas = Butacas.objects.all()
        butacas_serializer = ButacaSerializer(butacas, many=True)
        return JsonResponse(butacas_serializer.data, safe=False,
                            status=status.HTTP_200_OK)
    elif request.method == 'POST':
        butaca_data = JSONParser().parse(request)
        butaca_serializer = SalaSerializer(data=butaca_data)
        if butaca_serializer.is_valid():
            butaca_serializer.save()
            return validar_butaca(butaca_data, butaca_serializer)
        return JsonResponse(butaca_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


# Endpoint get + butaca
# Endpoint Butacas reservadas
@api_view(['GET'])
def butacasEspecifica(request, pk):
    try:
        butaca = Butacas.objects.get(pk=pk)
        if request.method == 'GET':
            butacas = Butacas.objects.all(pk=pk)
            butacas_serializer = ButacaSerializer(butacas, many=True)
            return JsonResponse(butacas_serializer.data, safe=False,
                                status=status.HTTP_200_OK)
        elif request.method == 'PUT':
            butaca_data = JSONParser().parse(request)
            butaca_serializer = ButacaSerializer(butaca, data=butaca_data)
            if butaca_serializer.is_valid():
                butaca_serializer.save()
                return validar_butaca(butaca_data, butaca_serializer)
            return JsonResponse(butaca_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
    except Butacas.DoesNotExist:
        return JsonResponse({'Mensaje': 'La butaca especificada no existe'},
                            status=status.HTTP_404_NOT_FOUND)


def validar_butaca(butaca_data, butaca_serializer):
    # obtengo la proyeccion
    proyeccion = Proyeccion.objects.get(pk=butaca_data['proyeccion'])
    # Obtengo la fecha de la proyeccion
    fecha = dt.datetime.strptime(butaca_data['fecha'],'%Y-%m-%d').date()
    # Veo que la proyeccion este activa
    if proyeccion.estado:
        sala = proyeccion.sala
        # Verifico que la fecha de la proyeccio este disponible
        if(fecha <= proyeccion.fechaFin and fecha >= proyeccion.fechaInicio):
            # Verifico que haya ingresado una fila y una butaca valida
            if butaca_data['fila'] <= sala.fila and butaca_data['asiento'] <= sala.asientos:
                # Obtengo todas las butacas de la proyeccion en la fecha ingresada
                butacas = Butacas.objects.filter(proyeccion=butaca_data['proyeccion'],
                                                 fecha=dt.datetime.strptime(butaca_data['fecha'], '%Y-%m-%d').date())
                for butaca in butacas:
                    # Verifico que la butaca no este reservada
                    if butaca.fila == butaca_data['fila'] and butaca.asiento == butaca_data['asiento']:
                        return JsonResponse({'Mensaje': 'La butaca deseada ya esta reservada'},
                                            status=status.HTTP_400_BAD_REQUEST)
                # Reservo la butaca
                butaca_serializer.save()
                return JsonResponse(butaca_serializer.data, status=status.HTTP_201_CREATED)
            return JsonResponse({'Mensaje': 'El numero de butaca es invalido para la sala seleccionada'},
                                status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'Mensaje': 'La fecha seleccionada es invalida para la proyeccion'},
                            status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({'Mensaje': 'La proyeccion especificada esta inhabilitada para reservas'},
                        status=status.HTTP_400_BAD_REQUEST)


# Reportes
# Reporte Butacas -> Rango de tiempo
@api_view(['GET'])
def reporteButacasRango(request, inicio, fin):
    pass


# Reporte Butacas -> Proyeccion + Rango de tiempo
@api_view(['GET'])
def reporteButacasProyeccionRango(request, proyeccion, inicio, fin):
    pass


# Reporte Ranking 5 peliculas mas vendidas -> Rango de tiempo
@api_view(['GET'])
def reporteRanking(request, inicio, fin):
    pass


# Reporte butacas vendidas en las peliculas activas -> Rango de tiempo
@api_view(['GET'])
def reportePeliculasActivas(request, inicio, fin):
    pass
