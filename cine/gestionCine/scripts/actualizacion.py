from gestionCine.models import Pelicula
import requests
import datetime as dt


def run():
    update()


def update():
    # Obtengo el catalogo del servicio
    r = requests.get('http://localhost:5000/api/pelicula/')
    peliculas_servicio = r.json()
    # Obtengo las peliculas de la BD del cine
    peliculas_db = list(Pelicula.objects.all().values())
    # Adapto los datos del servicio a los de la BD del cine
    peliculas_servicio = adaptar_datos(peliculas_servicio)
    peliculas_db = eliminar_id(peliculas_db)
    # Actualizo la BD del cine
    for pelicula in peliculas_servicio:
        if pelicula not in peliculas_db:
            Pelicula.objects.update_or_create(nombre=pelicula['nombre'],
                                              defaults={
                                                  'duracion': pelicula['duracion'],
                                                  'descripcion': pelicula['descripcion'],
                                                  'detalle': pelicula['detalle'],
                                                  'genero': pelicula['genero'],
                                                  'clasificacion': pelicula['clasificacion'],
                                                  'estado': pelicula['estado'],
                                                  'fechaComienzo': pelicula['fechaComienzo'],
                                                  'fechaFinalizacion': pelicula['fechaFinalizacion']
                                              })
    # Dejo inactivas las peliculas que no esten en el servicio
    # Obtengo de nuevo las peliculas pero esta vez con la BD actualizada
    peliculas_db = list(Pelicula.objects.all().values())
    peliculas_db = eliminar_id(peliculas_db)
    for pelicula in peliculas_db:
        if pelicula not in peliculas_servicio:
            Pelicula.objects.filter(nombre=pelicula['nombre']).update(estado='Inactiva')


def adaptar_datos(peliculas):
    for pelicula in peliculas:
        # Elimino el ID ya que no siempre coincide con el ID de la BD del cine
        del pelicula['id']
        # Adapto la fecha
        pelicula['fechaComienzo'] = dt.datetime.strptime(pelicula['fechaComienzo'], '%Y-%m-%dT%H:%M:%S+%f').date()
        pelicula['fechaFinalizacion'] = dt.datetime.strptime(pelicula['fechaFinalizacion'], '%Y-%m-%dT%H:%M:%S+%f').date()
    return peliculas


def eliminar_id(peliculas):
    for pelicula in peliculas:
        # Elimino el ID ya que no siempre coincide con el ID de la BD del servicio
        del pelicula['ID_Peli']
    return peliculas
