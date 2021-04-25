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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import orderedmap as om
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.DataStructures import listiterator as it
import datetime
assert cf

"""

"""

# Construccion de modelos
def newCatalog():
    """ 
    """
    catalog = {'events': None,
               'eventos':None,
               "artistas":None,
               "pistas": None}

    catalog['events'] = om.newMap(omaptype='RBT',
                                      comparefunction=comparetupla)
    catalog['eventos']=lt.newList(datastructure="ARRAY_LIST")

    catalog["artistas"] = mp.newMap(maptype="PROBING",loadfactor=0.5)

    catalog["pistas"] = mp.newMap(maptype="PROBING",loadfactor=0.5)
    
    return catalog

def addevent(catalog,event):
    """
    """
    lista=catalog['eventos']
    lt.addLast(lista,event)
    updateArtistas(catalog['artistas'], event)
    updatePistas(catalog["pistas"], event)

def addevent2(catalog,event):
    updatehtevent(catalog['events'],event)
    return catalog

    
def newcontextentry(event,content):
    entry={'valor':float(event[content]),'artists':None,'events':1}
    entry['artists']=lt.newList(datastructure="ARRAY_LIST")
    lt.addLast(entry['artists'],event['artist_id'])
    return entry

def newArtist(artist_id):
    entry = {"artist_id":None,"num_eventos":1}
    entry["artist_id"] = artist_id
    return entry

def newPista(track_id):
    entry = {"track_id":None,"apariciones":1}
    entry["track_id"] = track_id
    return entry

def updateArtistas(mapa,event):
    """
    """
    artist_id = event["artist_id"]

    if mp.contains(mapa, artist_id):
        entry = mp.get(mapa,artist_id)
        entry = me.getValue(entry)
        entry["num_eventos"] += 1
    
    else: 
        entry = newArtist(artist_id)
        mp.put(mapa,artist_id,entry)



def updatePistas(mapa,event):
    """
    """
    track_id = event["track_id"]

    if mp.contains(mapa,track_id):
        entry = mp.get(mapa, track_id)
        entry = me.getValue(entry)
        entry["apariciones"] += 1
    else:
        entry = newPista(track_id)
        mp.put(mapa,track_id,entry)
    
    

def updateevent(mapa,event):
    user=event['user_id']
    track=event['track_id']
    date=event['created_at']
    tupla=user,track,date
    entry=om.get(mapa,tupla)
    if entry is None:
        evententry=newevententry(event,user,track,date)
        om.put(mapa,tupla,evententry)
    else:
        evententry=me.getValue(entry)
    lt.addLast(evententry['events'],event)

def updatehtevent(mapa,event):  
    user=event['user_id']
    track=event['track_id']
    date=event['created_at']
    tupla=user,track,date
    entry=om.get(mapa,tupla)
    
        
def newevententry(event,user,track,date):
    entry={'tupla':None,'hashtag':None,'events':None}
    entry['tuple']=user,track,date
    entry['events']=lt.newList(datastructure="ARRAY_LIST")
    return entry




# Funciones para agregar informacion al catalogo

# Funciones para creacion de datos
def ListaPorContenido_TablaHashPorArtistas(mayor,menor,content,catalog):
    """
    Retorna una lista filtrada por eventos en los cuales menor<=event[content]<=mayor
    """
    mapa = mp.newMap(maptype="PROBING",loadfactor=0.5)
    lista = lt.newList(datastructure="ARRAY_LIST")
    listaevents = catalog['eventos']
    x = it.newIterator(listaevents)

    while it.hasNext(x):
        event = it.next(x)
        valor = float(event[content])

        if float(menor)<=valor<=float(mayor):
            lt.addLast(lista, event)
            artista = event["artist_id"]
            mp.put(mapa,artista,None)

    return lista,mapa

def TablaHashPorArtistas(lista):
    mapa = mp.newMap(maptype="PROBING",loadfactor=0.5)
    x = it.newIterator(lista)
    while it.hasNext(x):
        event = it.next(x)
        artista = event["artist_id"]
        mp.put(mapa,artista,None)
    
    return mapa


def RBTporContenido(mayor,menor,content,catalog):
    """
    Retorna un RBT cuyas llaves son el valor[content] (el valor del contenido especificado) y el valor respectivo es una entrada de newcontextentry que tiene valor, lista de artistas y número de eventos
    """
    mapa=om.newMap(omaptype="RBT",comparefunction=comparetupla)
    listaevents=catalog['eventos']
    x=it.newIterator(listaevents)
    while it.hasNext(x):
        event=it.next(x)
        valor=float(event[content])
        if float(menor)<=valor<=float(mayor):
            if om.contains(mapa,valor):
                entrada=om.get(mapa,valor)
                val=me.getValue(entrada)
                if lt.isPresent(val['artists'],event['artist_id'])==0:
                    lt.addLast(val['artists'], event['artist_id'])
                val['events']+=1
            else:
                entrada=newcontextentry(event,content)
                om.put(mapa,valor,entrada)
    return mapa

def req1(content,catalog):
    mapa=om.newMap(catalog['events'])
    listaevents=catalog['eventos']
    x=it.newIterator(listaevents)
    while it.hasNext(x):
        event=it.next(x)
        valor=float(event[content])
        if om.contains(mapa,valor):
            entrada=om.get(mapa,valor)
            val=me.getValue(entrada)
            if lt.isPresent(val['artists'],event['artist_id'])==0:
                lt.addLast(val['artists'], event['artist_id'])
            val['events']+=1
        else:
            entrada=newcontextentry(event,content)
            om.put(mapa,valor,entrada)
    return mapa
# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
def comparetupla(tupla1, tupla2):
    """
    Compara dos valores numericos
    """
    if (tupla1 == tupla2):
        return 0
    elif (tupla1 > tupla2):
        return 1
    else:
        return -1