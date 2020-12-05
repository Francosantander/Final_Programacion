from django.shortcuts import render
# from django.template import Template, Context
from django.template.loader import get_template
from django.http import HttpResponse
from gestionCine.models import Pelicula


def principal(request):
    return render(request, "principal.html")


def butacas(request):
    return render(request, "butacas.html")


def busqueda_pelis(request):
    return render(request, "busqueda_pelis.html")


def buscar(request):
    if request.GET["peli"]:
        # mensaje = "Pelicula buscada: {}" .format(request.GET["peli"])
        peli = request.GET["peli"]
        if len(peli) > 20:
            mensaje = "Texto de busqueda demasiado largo"
            return HttpResponse(mensaje) 
        else:
            peliculas = Pelicula.objects.filter(nombre__icontains=peli)
            return render(request, "resultados_busqueda.html", {"peliculas":peliculas, "query":peli})
    else:
        mensaje = "No se ha ingresado nada para la busqueda"
        return HttpResponse(mensaje)
