from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.shortcuts import render
from .models import Pelicula, Salas, Proyeccion, Butacas
from .serializers import PeliculaSerializer, SalaSerializer, ButacaSerializer
from .serializers import ProyeccionSerializer
from rest_framework.decorators import api_view
import datetime as dt
import operator


def principal(request):
    return render(request, "principal.html")


# Endpoint Peliculas
# Listado de peliculas en un rando de +- 15 dias
@api_view(['GET', 'POST'])
def pelis(request):
    if request.method == 'GET':
        now = dt.datetime.now()
        rango = dt.timedelta(days=15)
        peliculas = Pelicula.objects.filter(fechaFinalizacion__gte=(now - rango),
                                            fechaComienzo__lte=(now + rango))
        peliculas_serializer = PeliculaSerializer(peliculas, many=True)
        return JsonResponse(peliculas_serializer.data, safe=False,
                            status=status.HTTP_200_OK)
    elif request.method == 'POST':
        pelicula_data = JSONParser().parse(request)
        pelicula_serializer = PeliculaSerializer(data=pelicula_data)
        if pelicula_serializer.is_valid():
            pelicula_serializer.save()
            return JsonResponse(pelicula_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(pelicula_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)



# Ver que hacer con la respuesta de la pelicula
# Endpoint pelicula especifica + rango de fecha
@api_view(['GET'])
def peli_detail(request, pk, inicio, fin):
    try:
        # Convierto las fechas ingresadas a formato date
        fechaInicio = dt.datetime.strptime(inicio, '%Y-%m-%d').date()
        fechaFin = dt.datetime.strptime(fin, '%Y-%m-%d').date()
        # Obtengo los datos de la pelicula ingresada
        peli = Pelicula.objects.get(pk=pk)
        fechas = []
        proye = Proyeccion.objects.filter(pelicula=peli,
                                          fecha_inicio__lte=fechaInicio,
                                          fecha_fin__gte=fechaFin)
        respuesta = []
        salas = []
        # Me fijo que la fecha de la proyeccion se encuentre en el rango ingresado
        if proye.count() != 0:
            # Obtengo las proyecciones de las fechas de las butacas
            for proyeccion in proye:
                butacas = Butacas.objects.all().filter(proyeccion=proyeccion)
                if salas == []:
                    salas.append(proyeccion.sala.nombre)
                else:
                    for j in range(len(salas)):
                        if salas[j] != str(proyeccion.sala.nombre):
                            salas.append(str(proyeccion.sala.nombre))
                for butaca in butacas:
                    fechas.append(str(butaca.fecha))
            fechas.sort()
            # Elimino las fechas que se repiten y ordenos las fechas
            fecha = list(set(fechas))
            fecha.sort()
            now = str(dt.datetime.now())
            now = now.split()
            now = now[0]
            fechas = []
            # Obtengo las fechas que sean mayor a la fecha del dia
            for i in range(len(fecha)):
                if fecha[i] >= now:
                    fechas.append(fecha[i])
            if fechas == []:
                # En caso de que no haya fechas disponibles ya que se vencio su proyeccion
                fechas = "No hay proyecciones disponibles"
            respuesta.append({
                'Pelicula': peli.nombre,
                'Descripcion': peli.descripcion,
                'Genero': peli.genero,
                'Sala': salas[0],
                'Rango de fecha activa de la pelicula': '{} al {}'.format(peli.fechaComienzo, peli.fechaFinalizacion),
                'Fechas Disponibles': fechas,
                })
            return JsonResponse(respuesta, safe=False, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'Mensaje': 'No existen proyecciones de la pelicula en las fechas deseadas'},
                                status=status.HTTP_204_NO_CONTENT)
    except Pelicula.DoesNotExist:
        return JsonResponse({'Mensaje': 'La pelicula especificada no existe o los rangos de fechas ingresados son incorrecto'},
                            status=status.HTTP_404_NOT_FOUND)


# Lista de peliculas especificando un rango de fechas
@api_view(['GET'])
def peli_date_detail(request, inicio, fin):
    try:
        fechaInicio = dt.datetime.strptime(inicio, '%Y-%m-%d').date()
        fechaFin = dt.datetime.strptime(fin, '%Y-%m-%d').date()
        # Proyeccion.objects.filter(fecha_inicio__lte=fechaFin, fecha_fin__gte=fechaInicio)
        peliculas = Pelicula.objects.filter(fechaComienzo__lte=fechaFin,
                                            fechaFinalizacion__gte=fechaInicio)
        # pelicula_serializer = PeliculaSerializer(peli, many=True)
        listado = []
        for pelicula in peliculas:
            listado.append(pelicula.nombre)
        respuesta = {
            'peliculas': listado
        }
        return JsonResponse(respuesta,
                            status=status.HTTP_200_OK)
    except Pelicula.DoesNotExist:
        return JsonResponse({'Mensaje': 'Los rangos de fechas ingresados son incorrecto'},
                            status=status.HTTP_404_NOT_FOUND)


# Endpoint de las Salas
# Endpoint para obetener la lista de salas o crear una
@api_view(['GET', 'POST'])
def salas_list(request):
    if request.method == 'GET':
        salas = Salas.objects.all()
        salas_serializer = SalaSerializer(salas, many=True)
        return JsonResponse(salas_serializer.data, safe=False,
                            status=status.HTTP_200_OK)
    # Verificar la creacion de la sala
    elif request.method == 'POST':
        salas_data = JSONParser().parse(request)
        salas_serializer = SalaSerializer(data=salas_data)
        if salas_serializer.is_valid():
            return validar_sala_Creacion(salas_data, salas_serializer)
        return JsonResponse(salas_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


# Endpoint de obtencion, modificacion o eliminacion de una sala
@api_view(['GET', 'PUT', 'DELETE'])
def sala_detail(request, pk):
    try:
        sala = Salas.objects.get(pk=pk)

        if request.method == 'GET':
            sala_serializer = SalaSerializer(sala)
            return JsonResponse(sala_serializer.data,
                                status=status.HTTP_200_OK)

        elif request.method == 'PUT':
            sala_data = JSONParser().parse(request)
            sala_serializer = SalaSerializer(sala, data=sala_data)
            if sala_serializer.is_valid():
                return validar_sala(sala_data, sala_serializer)
            return JsonResponse(sala_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            sala.delete()
            return JsonResponse({'Mensaje': 'La sala se elimino correctamente'},
                                status=status.HTTP_204_NO_CONTENT)

    except Salas.DoesNotExist:
        return JsonResponse({'Mensaje': 'La sala especificada no existe'},
                            status=status.HTTP_404_NOT_FOUND)


def validar_sala_Creacion(sala_data, sala_serializer):
    # Veo que no se repita el nombre de la sala
    salas = Salas.objects.all()
    for sala in salas:
        if sala.nombre == sala_data['nombre']:
            return JsonResponse({'Mensaje': 'Nombre de la sala repetida'},
                                status=status.HTTP_400_BAD_REQUEST)
    # Verifico el estado de la sala
    if sala_data['estado'] == "Habilitada" or sala_data['estado'] == "habilitada" or sala_data['estado'] == "Deshabilitada" or sala_data['estado'] == "deshabilitada":
        # Verifico que haya ingresado una cantidad valida de filas y asientos
        if sala_data['fila'] >= 8 and sala_data['fila'] <= 15:
            if sala_data['asientos'] >= 8 and sala_data['asientos'] <= 15:
                sala_serializer.save()
                return JsonResponse(sala_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse({'Mensaje': 'Ingrese una cantidad de asientos validas (8-15)'},
                                    status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({'Mensaje': 'Ingrese una cantidad de filas validas (8-15)'},
                                status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({'Mensaje': 'Ingrese un estado valido para la sala'},
                            status=status.HTTP_400_BAD_REQUEST)


def validar_sala(sala_data, sala_serializer):
    # Verifico el estado de la sala
    if sala_data['estado'] == "Habilitada" or sala_data['estado'] == "habilitada" or sala_data['estado'] == "Deshabilitada" or sala_data['estado'] == "deshabilitada":
        # Verifico que haya ingresado una cantidad valida de filas y asientos
        if sala_data['fila'] >= 8 and sala_data['fila'] <= 15:
            if sala_data['asientos'] >= 8 and sala_data['asientos'] <= 15:
                sala_serializer.save()
                return JsonResponse(sala_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse({'Mensaje': 'Ingrese una cantidad de asientos validas (8-15)'},
                                    status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({'Mensaje': 'Ingrese una cantidad de filas validas (8-15)'},
                                status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({'Mensaje': 'Ingrese un estado valido para la sala'},
                            status=status.HTTP_400_BAD_REQUEST)


# Endpoint Proyecciones
# Endpoint Proyecciones activas
@api_view(['GET', 'POST'])
def proyecciones_list(request):
    if request.method == 'GET':
        proye = Proyeccion.objects.filter(estado=True)
        proye_serializer = ProyeccionSerializer(proye, many=True)
        return JsonResponse(proye_serializer.data, safe=False,
                            status=status.HTTP_200_OK)
    elif request.method == 'POST':
        proye_data = JSONParser().parse(request)
        proye_serializer = ProyeccionSerializer(data=proye_data)
        if proye_serializer.is_valid():
            return validar_proyeccion(proye_data, proye_serializer)
        return JsonResponse(proye_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


# Endpoint GET + Rango de fechas
@api_view(['GET'])
def proyeccionesRango(request, inicio, fin):
    try:
        # Si funciona con get, entonces se lo dejo
        proye = Proyeccion.objects.filter(fecha_inicio__lte=fin,
                                          fecha_fin__gte=inicio, estado=True)
        proye_serializer = ProyeccionSerializer(proye, many=True)
        return JsonResponse(proye_serializer.data, safe=False,
                            status=status.HTTP_200_OK)
    except Proyeccion.DoesNotExist:
        return JsonResponse({'Mensaje': 'Los rangos de fechas ingresados son incorrecto'},
                            status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'PUT'])
def modificarProyeccion(request, pk):
    try:
        proye = Proyeccion.objects.get(pk=pk)
        # Traigo una proyeccion en particular
        if request.method == 'GET':
            proye_serializer = ProyeccionSerializer(proye)
            return JsonResponse(proye_serializer.data, safe=False,
                                status=status.HTTP_200_OK)
        elif request.method == 'PUT':
            proye_data = JSONParser().parse(request)
            proye_serializer = ProyeccionSerializer(proye, data=proye_data)
            if proye_serializer.is_valid():
                return validar_proyeccion(proye_data, proye_serializer)
            return JsonResponse(proye_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
    except Proyeccion.DoesNotExist:
        return JsonResponse({'Mensaje': 'La proyeccion especificada no existe'},
                            status=status.HTTP_404_NOT_FOUND)


# Arreglar y colocar butacas libres
# Get + proyeccion + fecha
@api_view(['GET'])
def proyePeliRango(request, pk, fecha):
    # Convierto el formato de la fecha
    fecha = dt.datetime.strptime(fecha, '%Y-%m-%d').date()
    try:
        # Obtengo la informacion de la proyeccion, pelicula, sala y butacas
        # A partir del pk de la proyeccion
        proye = Proyeccion.objects.get(pk=pk)
        peli = PeliculaSerializer(proye.pelicula)
        sala = SalaSerializer(proye.sala)
        butacas = Butacas.objects.filter(proyeccion=proye, fecha=fecha)
        # Creo un diccionario donde se almacenara el estado de las butacas
        ubicacion = {}
        c = 0
        # Recorro las filas y los asientos y me fijo si coinciden con la informacion de la butaca
        for fila in range(proye.sala.fila):
            for asiento in range(proye.sala.asientos):
                for butaca in butacas:
                    if((butaca.fila-1) == fila):
                        if((butaca.asiento-1) == asiento):
                            # Si coinciden lo almaceno como reservada
                            ubicacion[c] = {
                                'fila': butaca.fila,
                                'asiento': butaca.asiento,
                                'estado': 'Reservada',
                            }
                try:
                    # Trato de ver si hay informacion en esa posicion
                    # En caso contrario es que esta libre la butaca
                    ubicacion[c]
                except KeyError:
                    ubicacion[c] = {
                        'fila': fila+1,
                        'asiento': asiento+1,
                        'estado': 'Libre',
                    }
                finally:
                    c += 1
        # Creo el json
        respuesta = {
            'Informacion de la pelicula': peli.data,
            'Informacion de la sala': sala.data,
            'Informacion de las butacas': ubicacion,
        }
        return JsonResponse(respuesta, safe=False, status=status.HTTP_200_OK)
    except Proyeccion.DoesNotExist:
        return JsonResponse({'Mensaje': 'La proyeccion ingresada no existe'},
                            status=status.HTTP_404_NOT_FOUND)


def validar_proyeccion(proye_data, proye_serializer):
    # Obtengo todas las proyecciones
    proyecciones = Proyeccion.objects.all()
    # Valido que no se repitan las salas y las peliculas
    for proyeccion in proyecciones:
        if proyeccion.sala != proye_data['sala']:
            if proyeccion.pelicula != proye_data['pelicula']:
                pass
            else:
                return JsonResponse({'Mensaje': 'La Pelicula especificada ya se esta proyectando'},
                                    status=status.HTTP_404_NOT_FOUND)
        else:
            return JsonResponse({'Mensaje': 'La sala especificada ya esta ocupada'},
                                 status=status.HTTP_404_NOT_FOUND)
    # Obtengo la fecha actual y genero un rango de 540 dias
    now = str(dt.datetime.now())
    now = now.split()
    now = now[0]
    rango = dt.timedelta(days=540)
    # Obtengo la hora de la proyeccion y genero un rango de validacion
    hora = str(proye_data['hora'])
    hora = dt.datetime.strptime(hora, '%H:%M')
    manana = '10:00'
    manana = dt.datetime.strptime(manana, '%H:%M')
    noche = '23:59'
    noche = dt.datetime.strptime(noche, '%H:%M')
    # Valido la fecha ingresada
    if proye_data['fecha_inicio'] >= now and proye_data['fecha_fin'] < str(rango):
        # Valido la hora ingresada
        if hora >= manana and hora <= noche:
            # Valido el estado de la pelicula
            if proye_data['estado'] == True or proye_data['estado'] == False:
                proye_serializer.save()
                return JsonResponse(proye_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse({'Mensaje': 'El estado ingresado no es correcto (True/False)'},
                                    status=status.HTTP_404_NOT_FOUND)
        else:
            return JsonResponse({'Mensaje': 'La hora ingresada es incorrecta (10:00 - 23:59)'},
                                status=status.HTTP_404_NOT_FOUND)
    else:
        return JsonResponse({'Mensaje': 'Las fechas ingresadas son incorrectas'},
                            status=status.HTTP_404_NOT_FOUND)


# Endpoint Butacas reservadas
@api_view(['GET', 'POST'])
def butacas_list(request):
    if request.method == 'GET':
        butacas = Butacas.objects.all()
        butacas_serializer = ButacaSerializer(butacas, many=True)
        return JsonResponse(butacas_serializer.data, safe=False,
                            status=status.HTTP_200_OK)
    elif request.method == 'POST':
        butaca_data = JSONParser().parse(request)
        butaca_serializer = ButacaSerializer(data=butaca_data)
        if butaca_serializer.is_valid():
            return validar_butaca(butaca_data, butaca_serializer)
        return JsonResponse(butaca_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


# Endpoint get + butaca
# Endpoint Butacas reservadas
@api_view(['GET', 'PUT'])
def butacasEspecifica(request, pk):
    try:
        # Lo hago con el pk ya que es unico
        # Si lo hiciera con la fila y la columna, habria que especificar la pelicula
        butaca = Butacas.objects.get(pk=pk)
        if request.method == 'GET':
            butacas_serializer = ButacaSerializer(butaca)
            return JsonResponse(butacas_serializer.data, safe=False,
                                status=status.HTTP_200_OK)
        elif request.method == 'PUT':
            butaca_data = JSONParser().parse(request)
            butaca_serializer = ButacaSerializer(butaca, data=butaca_data)
            if butaca_serializer.is_valid():
                return validar_butaca(butaca_data, butaca_serializer)
            return JsonResponse(butaca_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
    except Butacas.DoesNotExist:
        return JsonResponse({'Mensaje': 'La butaca especificada no existe'},
                            status=status.HTTP_404_NOT_FOUND)


def validar_butaca(butaca_data, butaca_serializer):
    # obtengo la proyeccion
    proye = Proyeccion.objects.get(pk=butaca_data['proyeccion'])
    # Obtengo la fecha de la proyeccion
    fecha = dt.datetime.strptime(butaca_data['fecha'],'%Y-%m-%d').date()
    # Veo que la proyeccion este activa
    if proye.estado:
        sala = proye.sala
        # Verifico que la fecha de la proyeccio este disponible
        if(fecha <= proye.fecha_fin and fecha >= proye.fecha_inicio):
            # Verifico que haya ingresado una fila y una butaca valida
            if butaca_data['fila'] <= sala.fila and butaca_data['asiento'] <= sala.asientos:
                # Obtengo todas las butacas de la proyeccion en la fecha ingresada
                butacas = Butacas.objects.filter(proyeccion=butaca_data['proyeccion'],
                                                 fecha=dt.datetime.strptime(butaca_data['fecha'], '%Y-%m-%d').date())
                for butaca in butacas:
                    # Verifico que la butaca no este reservada
                    if butaca.fila == butaca_data['fila'] and butaca.asiento == butaca_data['asiento']:
                        return JsonResponse({'Mensaje': 'La butaca deseada ya esta reservada'},
                                            status=status.HTTP_400_BAD_REQUEST)
                # Reservo la butaca
                butaca_serializer.save()
                return JsonResponse(butaca_serializer.data, status=status.HTTP_201_CREATED)
            return JsonResponse({'Mensaje': 'El numero de butaca es invalido para la sala seleccionada'},
                                status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'Mensaje': 'La fecha seleccionada es invalida para la proyeccion'},
                            status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({'Mensaje': 'La proyeccion especificada esta inhabilitada para reservas'},
                        status=status.HTTP_400_BAD_REQUEST)


# Reportes
# Reporte Butacas -> Rango de tiempo
@api_view(['GET'])
def reporteButacasRango(request, inicio, fin):
    # Obtenemos todas las butacas en ese rango de fecha -> Butacas
    # Creamos un contar
    # Con un for recorremos los registros almacenados en "Butacas"
    # Y vamos agregandole  unidad al contador por cada registro encontrado
    # Hacemos un json con la cantidad de butacas vendidas
    try:
        fechaInicio = dt.datetime.strptime(inicio, '%Y-%m-%d').date()
        fechaFin = dt.datetime.strptime(fin, '%Y-%m-%d').date()
        butacas = Butacas.objects.filter(fecha__gte=fechaInicio, fecha__lte=fechaFin)
    except TypeError:
        return JsonResponse({'Message': 'The query is wrong'}, status=status.HTTP_404_NOT_FOUND)
    c = 0
    for butaca in butacas:
        c += 1
    if c == 0:
        respuesta = ['No se realizaron venta de butacas en el rango de fechas:{} al {}'.format(inicio, fin)]
        return JsonResponse(respuesta, safe=False, status=status.HTTP_200_OK)
    else:
        respuesta = ['Rango de fecha: {} al {}'.format(inicio, fin), 'Cantidad de butacas vendidas en el rango de tiempo: ' + str(c)]
        return JsonResponse(respuesta, safe=False, status=status.HTTP_200_OK)


# Reporte Butacas -> Proyeccion + Rango de tiempo
@api_view(['GET'])
def reporteButacasProyeccionRango(request, pk, inicio, fin):
    # Obtengo las butacas de la proyeccion en particular
    # butacas = Butacas.objects.get(pk=proyeccion)
    # Creamos un contar
    # Con un for recorremos los registros almacenados en "Butacas"
    # Y vamos agregandole  unidad al contador por cada registro encontrado
    # Hacemos un json con la cantidad de butacas vendidas
    try:
        proyeccion = Proyeccion.objects.get(pk=pk)
        fechaInicio = dt.datetime.strptime(inicio, '%Y-%m-%d').date()
        fechaFin = dt.datetime.strptime(fin, '%Y-%m-%d').date()
        butacas = Butacas.objects.filter(fecha__gte=fechaInicio, fecha__lte=fechaFin, proyeccion=proyeccion)
        c = 0
        for butaca in butacas:
            c += 1
        if c == 0:
            respuesta = ['No se realizaron venta de butacas en el rango de fechas:{} al {}'.format(fechaInicio, fechaFin)]
            return JsonResponse(respuesta, safe=False, status=status.HTTP_200_OK)
        else:
            respuesta = {
                'Pelicula': proyeccion.pelicula.nombre,
                'Rango de fecha': '{} al {}'.format(fechaInicio, fechaFin),
                'Cantidad de butacas vendidas': str(c),
            }
            return JsonResponse(respuesta, safe=False, status=status.HTTP_200_OK)
    except Proyeccion.DoesNotExist:
        return JsonResponse({'Mensaje': 'La proyeccion especificada no existe'},
                             status=status.HTTP_404_NOT_FOUND)


# Reporte Ranking 5 peliculas mas vendidas -> Rango de tiempo
@api_view(['GET'])
def reporteRanking(request, inicio, fin):
    # Buscamos las proyecciones que se han hecho en ese rango de tiempo -> objeto con proyecciones
    # Hacemos un for para recorre las proyecciones
    # Hacemos otro for adentro de las proyecciones para ir contando las butacas vendidas
    # Creamos un diccionario con el clave = nombre y valor = butacas vendidas
    # Creamos un json con el ranking de las peliculas y su cantidad
    try:
        fechaInicio = dt.datetime.strptime(inicio, '%Y-%m-%d').date()
        fechaFin = dt.datetime.strptime(fin, '%Y-%m-%d').date()
        proyecciones = Proyeccion.objects.filter(fecha_inicio__lte=fechaFin, fecha_fin__gte=fechaInicio)
        peliculas = {}
        c = 0
        for proyeccion in proyecciones:
            butacas = Butacas.objects.filter(proyeccion=proyeccion)
            for butaca in butacas:
                c += 1
            peliculas[proyeccion.pelicula.nombre] = c
            c = 0
        lista_ordenada = dict(sorted(peliculas.items(), key=operator.itemgetter(1), reverse=True))
        ranking = {}
        total = 0
        for elemento in lista_ordenada.items():
            total += 1
            if total <= 5:
                ranking[elemento[0]] = elemento[1]
        top = []
        x = 1
        for elemento in ranking:
            top.append((str(x) + ") " + str(elemento) + ", Butacas vendidas: " + str(ranking[elemento])))
            x += 1
        respuesta = {
            'Ranking de proyecciones:': top,
        }
        return JsonResponse(respuesta, safe=False, status=status.HTTP_200_OK)
    except TypeError:
        return JsonResponse({'Message': 'The query is wrong'}, status=status.HTTP_404_NOT_FOUND)


# Reporte butacas vendidas en las peliculas activas -> Rango de tiempo
@api_view(['GET'])
def reportePeliculasActivas(request):
    # Obtengo las peliculas que esten activas
    # Obtengo las proyecciones de las peliculas y de ahi las butacas vendidas
    # Creamos un json con la informacion
    peliculas = Pelicula.objects.filter(estado=True)
    c = 0
    respuesta = []
    for pelicula in peliculas:
        proyeccion = Proyeccion.objects.get(pelicula=pelicula)
        butacas = Butacas.objects.filter(proyeccion=proyeccion)
        for butaca in butacas:
            c += 1
        respuesta.append({
            'Pelicula': pelicula.nombre,
            'Proyeccion': proyeccion.ID_Proye,
            'Sala': proyeccion.sala.nombre,
            'Butacas Vendidas': str(c),
            })
        c = 0
    return JsonResponse(respuesta, safe=False, status=status.HTTP_200_OK)
