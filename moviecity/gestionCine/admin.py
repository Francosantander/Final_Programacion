from django.contrib import admin
from .models import Pelicula, Salas, Butacas, Proyeccion


class PeliculasAdmin(admin.ModelAdmin):
    list_display = ("nombre", "fechaComienzo", "fechaFinalizacion", "estado")
    search_fields = ("nombre", "fechaComienzo", "fechaFinalizacion", "estado")
    list_filter = ("nombre", "estado", "clasificacion")


class SalasAdmin(admin.ModelAdmin):
    list_display = ("nombre", "estado")
    search_fields = ("nombre", "estado")
    list_filter = ("nombre", "estado")


class ProyeccionesAdmin(admin.ModelAdmin):
    list_display = ("pelicula", "sala", "estado")
    search_fields = ("pelicula", "sala", "estado")
    list_filter = ("pelicula", "sala", "estado")


class ButacasAdmin(admin.ModelAdmin):
    list_display = ("proyeccion", "fecha", "fila", "asiento")
    search_fields = ("proyeccion", "fecha", "fila", "asiento")
    list_filter = ("proyeccion", "fecha", "fila", "asiento")


admin.site.register(Pelicula, PeliculasAdmin)
admin.site.register(Salas, SalasAdmin)
admin.site.register(Butacas, ButacasAdmin)
admin.site.register(Proyeccion, ProyeccionesAdmin)
