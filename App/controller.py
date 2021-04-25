"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import model
import csv
import time
import tracemalloc
import random

from datetime import datetime

from DISClib.DataStructures import listiterator as it
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # catalog es utilizado para interactuar con el modelo
    catalog = model.newCatalog()
    return catalog


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento de datos en los modelos
# ___________________________________________________

def loadData(catalog):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    eventsfile=cf.data_dir + 'context_content_features-small.csv'
    input_file = csv.DictReader(open(eventsfile, encoding="utf-8"),delimiter=",")
    for evento in input_file:
        model.addevent(catalog,evento)

    lista = catalog["usertrackhashtagtimestamp"]
    userTHT_file=cf.data_dir+'user_track_hashtag_timestamp-small.csv'
    input2_file = csv.DictReader(open(userTHT_file, encoding="utf-8"),delimiter=",")
    for evento in input2_file:
        model.add_2(lista,evento)
    
    lista2 = catalog["sentiment_val"]
    sentimenalval_file = cf.data_dir+'user_track_hashtag_timestamp-small.csv'
    input3_file = csv.DictReader(open(sentimenalval_file, encoding="utf-8"),delimiter=",")
    for evento in input2_file:
        model.add_2(lista2,evento)

    return catalog

def req1(mayor,menor,content,catalog):
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    lista_mapa = model.ListaPorContenido_TablaHashPorArtistas(mayor, menor, content, catalog)
    #mapa_artistas = model.TablaHashPorArtistas(lista_filtrada)
    artists = mp.size(lista_mapa[1])
    events = lt.size(lista_mapa[0])

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return artists,events, delta_time, delta_memory

def req2(minimoEnergy,maximoEnergy,minimoDanceability,maximoDanceability,catalog):
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    lista = catalog["eventos"]
    filtro_En = model.FiltrarPorRango(minimoEnergy, maximoEnergy, "energy", lista)
    filtro_Da = model.FiltrarPorRango(minimoDanceability, maximoDanceability, "danceability", filtro_En)

    mapa = model.TablaHashPorTrack(filtro_Da)
    total = mp.size(mapa)

    mi = random.randint(1,lt.size(filtro_Da))

    aleatorios = lt.subList(filtro_Da, mi, 5)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return total,aleatorios,delta_time, delta_memory



"""
def req1(mayor,menor,content,catalog):
    mapa=model.RBTporContenido(mayor,menor,content,catalog)
    llaves=om.keys(mapa)
    i=it.newIterator(llaves)
    artists= om.newMap(omaptype="RBT")
    events=0
    altura=om.height(mapa)
    num=om.size(mapa)
    while it.hasNext(i):
        entry=om.get(mapa,it.next(i))
        valor=me.getValue(entry)
        art=valor["artists"]
        artists+=lt.size(art)
        events+=valor['events']
    return artists,events,altura,num
"""

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

# ======================================
# Funciones para medir tiempo y memoria
# ======================================


def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(start_memory, stop_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory
