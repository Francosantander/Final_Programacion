from rest_framework import serializers
from reservations.models import Pelicula, Proyeccion, Butaca, Sala


class PeliculaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pelicula
        fields = ('id', 'nombre', 'duracion', 'descripcion', 'detalle', 'genero', 'clasificacion',
                  'estado', 'fechaComienzo', 'fechaFinalizacion')


class ProyeccionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Proyeccion
        fields = ['id', 'sala', 'pelicula', 'fecha_inicio', 'fecha_fin', 'hora', 'estado']


class SalaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sala
        fields = ('id', 'nombre', 'estado', 'fila', 'asientos')


class ButacaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Butaca
        fields = ('id', 'proyeccion', 'fecha', 'fila', 'asiento')
