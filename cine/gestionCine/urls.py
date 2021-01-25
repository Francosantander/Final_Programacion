from django.conf.urls import url
from gestionCine import views

urlpatterns = [
    # url(r'^principal$', views.principal),
    # Actualizacion BD
    # url(r'^actualizacion$', views.actualizacion),
    # Endpoint Peliucla
    url(r'^peliculas$', views.pelis),
    url(r'^peliFecha/(\d{4}[-/]\d{2}[-/]\d{2})/(\d{4}[-/]\d{2}[-/]\d{2})$', views.peli_date_detail),
    url(r'^peliEspecifica/([a-zA-Z0-9 ]+)/(\d{4}[-/]\d{2}[-/]\d{2})/(\d{4}[-/]\d{2}[-/]\d{2})$', views.peli_detail),
    # Endpoint Sala
    url(r'^salas$', views.salas_list),
    url(r'^salasEspecifica/(?P<pk>[0-9]+)$', views.sala_detail),
    # Endpoint Butacas
    url(r'^butacas$', views.butacas_list),
    url(r'^ButacaEspecifica/(?P<pk>[0-9]+)$', views.butacasEspecifica),
    # Endpoint Proyecciones
    url(r'^proye$', views.proyecciones_list),
    url(r'^proyeRango/(?P<inicio>\d{4}[-/]\d{2}[-/]\d{2})/(?P<fin>\d{4}[-/]\d{2}[-/]\d{2})$', views.proyeccionesRango),
    url(r'^proyeEspecifica/(?P<pk>[0-9]+)$', views.modificarProyeccion),
    url(r'^proyePeliRango/(?P<pk>[0-9]+)/(?P<fecha>\d{4}[-/]\d{2}[-/]\d{2})$', views.proyePeliRango),

    # Reportes
    url(r'^reporte/butacasRango/(\d{4}[-/]\d{2}[-/]\d{2})/(\d{4}[-/]\d{2}[-/]\d{2})$', views.reporteButacasRango),
    url(r'^reporte/butacasProyeccion/(?P<pk>[0-9]+)/(?P<inicio>\d{4}[-/]\d{2}[-/]\d{2})/(?P<fin>\d{4}[-/]\d{2}[-/]\d{2})$', views.reporteButacasProyeccionRango),
    url(r'^reporte/Ranking/(?P<inicio>\d{4}[-/]\d{2}[-/]\d{2})/(?P<fin>\d{4}[-/]\d{2}[-/]\d{2})$', views.reporteRanking),
    url(r'^reporte/activeMovies$', views.reportePeliculasActivas),
]
