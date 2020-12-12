from django.conf.urls import url
from gestionCine import views

urlpatterns = [
    # url(r'^principal$', views.principal),
    # url(r'^butacas$', views.butacas),
    # url(r'^busqueda_pelis$', views.busqueda_pelis),
    # Endpoint Peliucla
    url(r'^peliculas$', views.pelis),
    url(r'^peliEspecifica/([a-zA-Z0-9 ]+)/(\d{4}[-/]\d{2}[-/]\d{2})/(\d{4}[-/]\d{2}[-/]\d{2})$', views.peli_detail),
    url(r'^peliFecha/(\d{4}[-/]\d{2}[-/]\d{2})/(\d{4}[-/]\d{2}[-/]\d{2})$', views.peli_date_detail),
    # Endpoint Sala
    url(r'^salas$', views.salas_list),
    url(r'^salasEspecifica/(?P<pk>[0-9]+)$', views.sala_detail),
]
