from django.db import models


class Pelicula(models.Model):
    ID_Peli = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    duracion = models.DurationField()
    descripcion = models.TextField()
    detalle = models.TextField()
    genero = models.CharField(max_length=50)
    clasificacion = models.CharField(max_length=50)
    estado = models.BooleanField()  # True = activo / False = inactivo
    fechaComienzo = models.DateField()  # format YYYY-MM-DD
    fechaFinalizacion = models.DateField()  # format YYYY-MM-DD


class Salas(models.Model):
    ID_Sala = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    estado = models.CharField(max_length=20)
    fila = models.IntegerField()
    asientos = models.IntegerField()


class Proyeccion(models.Model):
    ID_Proye = models.IntegerField(primary_key=True)
    sala = models.OneToOneField(Salas, null=True, blank=True,
                                on_delete=models.CASCADE)
    pelicula = models.OneToOneField(Pelicula, null=True, blank=True,
                                    on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    hora = models.TimeField()
    estado = models.BooleanField()  # True = activo / False = inactivo


class Butacas(models.Model):
    ID_butacas = models.IntegerField(primary_key=True)
    proyeccion = models.OneToOneField(Proyeccion, null=True, blank=True,
                                      on_delete=models.CASCADE)
    fecha = models.DateField()  # format YYYY-MM-DD
    fila = models.CharField(max_length=50)
    asiento = models.IntegerField()
