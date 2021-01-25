from django.db import models
from django.core.validators import MinValueValidator


class Pelicula(models.Model):
    ID_Peli = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    duracion = models.IntegerField()
    descripcion = models.TextField()
    detalle = models.TextField()
    genero = models.CharField(max_length=50)
    clasificacion = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)  # activo / inactivo
    fechaComienzo = models.DateField(verbose_name="Fecha de comienzo")  # format YYYY-MM-DD
    fechaFinalizacion = models.DateField(verbose_name="Fecha de Finalizacion")  # format YYYY-MM-DD

    def __str__(self):
        return self.nombre


class Salas(models.Model):
    ID_Sala = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    estado = models.CharField(max_length=20)
    fila = models.IntegerField()
    asientos = models.IntegerField()

    def __str__(self):
        return self.nombre


class Proyeccion(models.Model):
    ID_Proye = models.AutoField(primary_key=True)
    sala = models.ForeignKey(Salas, null=True, blank=True,
                             on_delete=models.CASCADE)
    pelicula = models.ForeignKey(Pelicula, null=True, blank=True,
                                 on_delete=models.CASCADE)
    fecha_inicio = models.DateField(verbose_name="Fecha de inicio")
    fecha_fin = models.DateField(verbose_name="Fecha de finalizacion")
    hora = models.TimeField()
    estado = models.BooleanField(default=False)  # True = activo / False = inactivo

    def __str__(self):
        text = "Proyeccion: " + str(self.pelicula.nombre) + " / Sala: "
        text += str(self.sala.nombre)
        return text


class Butacas(models.Model):
    ID_butacas = models.AutoField(primary_key=True)
    proyeccion = models.ForeignKey(Proyeccion, null=True, blank=True,
                                   on_delete=models.CASCADE)
    fecha = models.DateField()  # format YYYY-MM-DD
    fila = models.IntegerField()
    asiento = models.IntegerField()

    def __str__(self):
        text = str(self.proyeccion.pelicula.nombre) + " el dia "
        text += str(self.fecha) + " / Butaca Fila: " + str(self.fila)
        text += " Asiento: " + str(self.asiento)
        return text
