﻿"""
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

from datetime import datetime
import config as cf
import model
import csv
from DISClib.DataStructures import listiterator as it
from DISClib.ADT import orderedmap as om
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import list as lt
import tracemalloc
import time


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
    file1=cf.data_dir+'user_track_hashtag_timestamp-small.csv'
    input_file1 = csv.DictReader(open(file1, encoding="utf-8"),delimiter=",")
    mapa=mp.newMap()
    for event in input_file1:
        llave=(event['track_id'],event['user_id'],event['created_at'])
        if mp.contains(mapa,llave):
            pareja=mp.get(mapa,llave)
            lista=me.getValue(pareja)
            lt.addLast(lista,event['hashtag'])
        else:
            lista=lt.newList()
            lt.addLast(lista,event['hashtag'])
            mp.put(mapa,llave,lista)

    file2=cf.data_dir + 'context_content_features-small.csv'
    input_file2 = csv.DictReader(open(file2, encoding="utf-8"),delimiter=",")
    for event in input_file2:
        llave=(event['track_id'],event['user_id'],event['created_at'])
        if mp.contains(mapa,llave):
            pareja=mp.get(mapa,llave)
            hashtags=me.getValue(pareja)
            event['hashtags']=hashtags
        else:
            event['hashtags']=None
        model.addevent(catalog,event)


    file3=cf.data_dir+'sentiment_values.csv'
    input_file3=csv.DictReader(open(file3, encoding="utf-8"),delimiter=",")
    for hashtag in input_file3:
        print(hashtag)

    return catalog

def req1(menor,mayor,feature,catalog):
    events=model.numevents(om.values(catalog[feature],menor,mayor))
    artists=(model.artists(om.values(catalog[feature],menor,mayor)))[0]
    print('\n'+feature+' is between '+str(menor)+' and '+str(mayor)+'\nTotal of reproduction: '+str(events)+'\nTotal of unique artists: '+str(artists))

def req2_3(catalog,min_en,max_en,min_dan,max_dan):
    keys1 = om.values(catalog["energy2"],min_en,max_en)
    lista1 = model.listaeventos(catalog["energy2"],keys1)
    mapa = om.newMap(omaptype="RBT")

    i1 = it.newIterator(lista1)
    while it.hasNext(i1):
        event = it.next(i1)
        model.addtomap2(mapa, event,"danceability")

    keys2 = om.values(mapa,min_dan,max_dan)
    lista2 = model.listaeventos(mapa,keys2)

    mapafin = mp.newMap(maptype="PROBING",loadfactor=0.5)
    i2 = it.newIterator(lista2)
    while it.hasNext(i2):
        event = it.next(i2)
        mp.put(mapafin, event["track_id"],event)
    
    print('\Energy is between '+str(min_en)+' and '+str(max_en)+'\Danceability is between '+str(min_dan)+' and '+str(max_dan)+'\nTotal of unique tracks in events: '+str(mp.size(mapafin))+'\n')

    n = 1
    listakeys = mp.keySet(mapafin)
    while n<=5:
        llave = lt.getElement(listakeys, n)
        event = mp.get(mapafin,llave)["value"]

        print('Track '+str(n)+': '+ event["track_id"]+' with energy of '+str(event["energy"])+' and danceability of '+str(event["danceability"]))
        n +=1
    print('\n')

def req2(catalog,min1,max1,min2,max2):
    keys1=om.values(catalog['energy'],min1,max1)
    keys2=om.values(catalog['danceability'],min2,max2)
    lista1=model.listaconlistas(keys1)
    final=model.dosfeatures(keys2,lista1)
    print('\nEnergy is between '+str(min1)+' and '+str(max1)+'\nDanceability is between '+str(min2)+' and '+str(max2)+'\nTotal of unique tracks in events: '+str(final)+'\n')
    random=model.random5(catalog,'energy','danceability',min1,max1,min2,max2)
    i=it.newIterator(random)
    n=0
    print('--- Unique track_id ---')
    while it.hasNext(i):
        event=it.next(i)
        n+=1
        print('Track '+str(n)+': '+ event[0]+' with energy of '+str(event[1])+' and danceability of '+str(event[2]))
    print('\n')

def req3(catalog,min_inst,max_inst,min_temp,max_temp):
    keys1 = om.values(catalog["tempo2"],min_temp,max_temp)
    lista1 = model.listaeventos(catalog["tempo2"],keys1)
    mapa = om.newMap(omaptype="RBT")

    i1 = it.newIterator(lista1)
    while it.hasNext(i1):
        event = it.next(i1)
        model.addtomap2(mapa, event,"instrumentalness")

    keys2 = om.values(mapa,min_inst,max_inst)
    lista2 = model.listaeventos(mapa,keys2)

    mapafin = mp.newMap(maptype="PROBING",loadfactor=0.5)
    i2 = it.newIterator(lista2)
    while it.hasNext(i2):
        event = it.next(i2)
        mp.put(mapafin, event["track_id"],event)
    
    print('\Instrumentalness is between '+str(min_inst)+' and '+str(max_inst)+'\nTempo is between '+str(min_temp)+' and '+str(max_temp)+'\nTotal of unique tracks in events: '+str(mp.size(mapafin))+'\n')

    n = 1
    listakeys = mp.keySet(mapafin)
    while n<=5:
        llave = lt.getElement(listakeys, n)
        event = mp.get(mapafin,llave)["value"]

        print('Track '+str(n)+': '+ event["track_id"]+' with instrumentalness of '+str(event["instrumentalness"])+' and tempo of '+str(event["tempo"]))
        n +=1
    print('\n')



def req4(catalog,genre,minimo,maximo):
    if minimo==None:
        if genre=='reggae':
            menor=60
            mayor=90
        elif genre=='down-tempo':
            menor=70
            mayor=100
        elif genre=='chill-out':
            menor=90
            mayor=120
        elif genre=='hip-hop':
            menor=85
            mayor=112
        elif genre=='jazz and funk':
            menor=120
            mayor=125
        elif genre=='pop':
            menor=100
            mayor=130
        elif genre=='r&b':
            menor=60
            mayor=80
        elif genre=='rock':
            menor=100
            mayor=140
        elif genre=='metal':
            menor=100
            mayor=160
    else:
        menor=minimo
        mayor=maximo

    eventos=model.numevents(om.values(catalog['tempo'],menor,mayor))
    y=model.artists(om.values(catalog['tempo'],menor,mayor))
    numartists=y[0]
    listartists=y[1]
    print('\n======= '+genre.upper()+' ========'+'\nFor '+genre+' the tempo is between '+str(menor)+' and '+str(mayor)+'\n'+genre+' reproductions: '+str(eventos)+' with '+str(numartists)+' different artists'+'\n\n---- Some artists for '+genre+' -----\n')
    i=it.newIterator(listartists)
    n=1
    while it.hasNext(i):
        artist=it.next(i)
        print('Artist '+str(n)+': '+artist)
        n+=1

def getTime():
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