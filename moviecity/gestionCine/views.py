from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.shortcuts import render
from gestionCine.models import Pelicula, Salas, Proyeccion, Butacas
from .serializers import PeliculaSerializer, SalaSerializer, ButacaSerializer, ProyeccionSerializer
from rest_framework.decorators import api_view


def principal(request):
    return render(request, "principal.html")


def butacas(request):
    return render(request, "butacas.html")


def busqueda_pelis(request):
    return render(request, "busqueda_pelis.html")


# Salas
@api_view(['GET', 'POST'])
def salas_list(request):
    if request.method == 'GET':
        salas = Salas.objects.all()
        salas_serializer = SalaSerializer(salas, many=True)
        return JsonResponse(salas_serializer.data, safe=False, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        salas_data = JSONParser().parse(request)
        salas_serializer = SalaSerializer(data=salas_data)
        if salas_serializer.is_valid():
            salas_serializer.save()
            return JsonResponse(salas_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(salas_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def sala_detail(request, pk):
    try:
        sala = Salas.objects.get(pk=pk)

        if request.method == 'GET':
            sala_serializer = SalaSerializer(sala)
            return JsonResponse(sala_serializer.data, status=status.HTTP_200_OK)

        elif request.method == 'PUT':
            sala_data = JSONParser().parse(request)
            sala_serializer = SalaSerializer(sala, data=sala_data)
            if sala_serializer.is_valid():
                sala_serializer.save()
                return JsonResponse(sala_serializer.data)
            return JsonResponse(sala_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            sala.delete()
            return JsonResponse({'Mensaje': 'La sala se elimino correctamente'}, status=status.HTTP_204_NO_CONTENT)

    except Salas.DoesNotExist:
        return JsonResponse({'Mensaje': 'La sala especificada no existe'}, status=status.HTTP_404_NOT_FOUND)
