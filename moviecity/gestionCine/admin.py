from django.contrib import admin
from .models import Pelicula, Salas, Butacas, Proyeccion


admin.site.register(Pelicula)
admin.site.register(Salas)
admin.site.register(Butacas)
admin.site.register(Proyeccion)
