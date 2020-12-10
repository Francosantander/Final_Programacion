from rest_framework import serializers
from .models import Pelicula, Proyeccion, Butacas, Salas


class PeliculaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pelicula
        fields = ('ID_Peli', 'nombre', 'duracion', 'descripcion', 'detalle', 'genero', 'clasificacion',
                  'estado', 'fechaComienzo', 'fechaFinalizacion')


class ProyeccionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Proyeccion
        fields = ['ID_Proye', 'sala', 'pelicula', 'fecha_inicio', 'fecha_fin', 'hora', 'estado']


class SalaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Salas
        fields = ('ID_Sala', 'nombre', 'estado', 'fila', 'asientos')


class ButacaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Butacas
        fields = ('ID_butacas', 'proyeccion', 'fecha', 'fila', 'asiento')
