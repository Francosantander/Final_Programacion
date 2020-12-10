from django.conf.urls import url
from gestionCine import views

urlpatterns = [
    url(r'^principal$', views.principal),
    url(r'^butacas$', views.butacas),
    url(r'^busqueda_pelis$', views.busqueda_pelis),
    url(r'^salas$', views.salas_list),
]
