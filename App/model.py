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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import orderedmap as om
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.DataStructures import listiterator as it
import datetime

"""
@@ -38,6 +41,92 @@
"""

# Construccion de modelos
def newCatalog():
    """ Inicializa el analizador
    Crea una lista vacia para guardar todos los crimenes
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas
    Retorna el analizador inicializado.
    """
    catalog = {'eventos':None,'energy':None,'instrumentalness':None,'danceability':None,'tempo':None,'acousticness':None}
    catalog['eventos']=lt.newList()
    catalog['energy']=om.newMap()
    catalog['instrumentalness']=om.newMap()
    catalog['danceability']=om.newMap()
    catalog['tempo']=om.newMap()
    catalog['acousticness']=om.newMap()
    catalog['liveness']=om.newMap()
    catalog['speechiness']=om.newMap()
    catalog['valence']=om.newMap()

    return catalog

def addevent(catalog,event):
    lt.addLast(catalog['eventos'],event)
    addtomap(catalog['energy'],event['track_id'],event['artist_id'],float(event['energy']),1)
    addtomap(catalog['instrumentalness'],event['track_id'],event['artist_id'],float(event['instrumentalness']),1)
    addtomap(catalog['danceability'],event['track_id'],event['artist_id'],float(event['danceability']),1)
    addtomap(catalog['tempo'],event['track_id'],event['artist_id'],float(event['tempo']),1)
    addtomap(catalog['acousticness'],None,event['artist_id'],float(event['acousticness']),0)
    addtomap(catalog['liveness'],None,event['artist_id'],float(event['liveness']),0)
    addtomap(catalog['speechiness'],None,event['artist_id'],float(event['speechiness']),0)
    addtomap(catalog['valence'],None,event['artist_id'],float(event['valence']),0)

    
def addtomap(mapa,track,artist,llave,x):
    if om.contains(mapa,llave):
        pareja=om.get(mapa,llave)
        value=me.getValue(pareja)
        value['events']+=1
        artists=value['artists']
        if lt.isPresent(artists,artist)==0:
            lt.addLast(artists,artist)
        if x==1:
            tracks=value['tracks']
            if lt.isPresent(tracks,track)==0:
                lt.addLast(tracks,track)
    else:
        if x==1:
            entrada=newentry1(llave,track,artist)
        else:
            entrada=newentry2(llave,artist)
        om.put(mapa,llave,entrada)
        

def newentry1(llave,track,artist):
    entry={'llave':llave,'tracks':None,'events':1,'artists':None}
    entry['tracks']=lt.newList(datastructure='ARRAY_LIST')
    lt.addLast(entry['tracks'],track)
    entry['artists']=lt.newList(datastructure='ARRAY_LIST')
    lt.addLast(entry['artists'],artist)
    return entry

def newentry2(llave,artist):
    entry={'llave':llave,'events':1,'artists':None}
    entry['artists']=lt.newList(datastructure='ARRAY_LIST')
    lt.addLast(entry['artists'],artist)
    return entry


def listaconlistas(lista):
    uno=lt.firstElement(lista)
    final=uno['tracks']
    lt.deleteElement(lista,1)
    i=it.newIterator(lista)
    while it.hasNext(i):
        entry=it.next(i)
        tracks=entry['tracks']
        ite=it.newIterator(tracks)
        while it.hasNext(ite):
            lt.addLast(final,it.next(ite))
    return final

def dosfeatures(lista,lista2):
    final=0
    i=it.newIterator(lista)
    while it.hasNext(i):
        entry=it.next(i)
        tracks=entry['tracks']
        ite=it.newIterator(tracks)
        while it.hasNext(ite):
            track=it.next(ite)
            if lt.isPresent(lista2,track):
                final+=1
    return final


def random5(catalog,feat1,feat2,min1,max1,min2,max2):
    i=it.newIterator(catalog['eventos'])
    final=lt.newList(datastructure='ARRAY_LIST')
    c=0
    while it.hasNext(i) and c<5:
        evento=it.next(i)
        if float(evento[feat1])>=min1 and float(evento[feat1])<=max1 and float(evento[feat2])>=min2 and float(evento[feat2])<=max2:
            c+=1
            tupla=(evento['track_id'],evento[feat1],evento[feat2])
            lt.addLast(final,tupla)
    return final

def numevents(lista):
    final=0
    i=it.newIterator(lista)
    while it.hasNext(i):
        entry=it.next(i)
        num=entry['events']
        final+=num
    return final

def artists(lista):
    entry1=lt.firstElement(lista)
    final=entry1['artists']
    lt.deleteElement(lista,1)
    i=it.newIterator(lista)
    while it.hasNext(i):
        entry=it.next(i)
        artists=entry['artists']
        ite=it.newIterator(artists)
        while it.hasNext(ite):
            artist=it.next(ite)
            if lt.isPresent(final,artist)==0:
                lt.addLast(final,artist)
    return lt.size(final)


# Funciones para agregar informacion al catalogo
# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento