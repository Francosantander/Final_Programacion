from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.shortcuts import render
from .models import Pelicula, Salas, Proyeccion, Butacas
from .serializers import PeliculaSerializer, SalaSerializer, ButacaSerializer, ProyeccionSerializer
from rest_framework.decorators import api_view
import datetime as dt


def principal(request):
    return render(request, "principal.html")


def butacas(request):
    return render(request, "butacas.html")


def busqueda_pelis(request):
    return render(request, "busqueda_pelis.html")

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


# Ver si anda
# Endpoint pelicula especifica + rango de fecha
@api_view(['GET'])
def peli_detail(request, nombre, inicio, fin):
    try:
        peli = Pelicula.objects.get(nombre=nombre, fechaComienzo=inicio, fechaFinalizacion=fin)
        pelicula_serializer = PeliculaSerializer(peli)
        return JsonResponse(pelicula_serializer.data,
                            status=status.HTTP_200_OK)
    except Pelicula.DoesNotExist:
        return JsonResponse({'Mensaje': 'La pelicula especificada no existe o los rangos de fechas ingresados son incorrecto'},
                            status=status.HTTP_404_NOT_FOUND)


# Ver si anda
# Lista de peliculas especificando un rango de fechas
@api_view(['GET'])
def peli_date_detail(request, inicio, fin):
    try:
        peli = Pelicula.objects.get(fechaComienzo__gte=inicio, fechaFinalizacion__lte=fin)
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


# Endpoint Proyecciones
# Endpoint Proyecciones activas
@api_view(['GET'])
def proyecciones_list(request):
    if request.method == 'GET':
        proye = Proyeccion.objects.get(estado=True)
        proye_serializer = ProyeccionSerializer(proye, many=True)
        return JsonResponse(proye_serializer.data, safe=False,
                            status=status.HTTP_200_OK)


# Endpoint GET + Rango de fechas
@api_view(['GET'])
def proyeccionesRango(request, pelicula, fecha):
    try:
        proye = Proyeccion.objects.filter(pelicula=pelicula)
        proye_serializer = ProyeccionSerializer(proye, many=True)
        return JsonResponse(proye_serializer.data,
                            status=status.HTTP_200_OK)
    except Proyeccion.DoesNotExist:
        return JsonResponse({'Mensaje': 'Los rangos de fechas ingresados son incorrecto'},
                            status=status.HTTP_404_NOT_FOUND)
