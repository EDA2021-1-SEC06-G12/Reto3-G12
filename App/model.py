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
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newCatalog():
    """ Inicializa el analizador

    Crea una lista vacia para guardar todos los crimenes
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas

    Retorna el analizador inicializado.
    """
    catalog = {'events': None,
            'eventos':None}

    catalog['events'] = om.newMap(omaptype='RBT',
                                      comparefunction=comparetupla)
    catalog['eventos']=lt.newList()
    
    return catalog

def addevent(catalog,event):
    """
    """
    lista=catalog['eventos']
    lt.addLast(lista,event)
    updateevents(catalog['events'], event)

def addevent2(catalog,event):
    updatehtevent(catalog['events'],event)
    return catalog


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


    
def newcontextentry(event,content):
    entry={'valor':float(event[content]),'artists':None,'events':1}
    entry['artists']=lt.newList()
    lt.addLast(entry['artists'],event['artist_id'])
    return entry


def updateevents(mapa,event):
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
    entry={'tupla':None,'hashtag':None,'events':event}
    entry['tuple']=user,track,date
    entry['events']=lt.newList()
    return entry




# Funciones para agregar informacion al catalogo

# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
def comparetupla(tupla1, tupla2):
    """
    Compara dos fechas
    """
    if (tupla1 == tupla2):
        return 0
    elif (tupla1 > tupla2):
        return 1
    else:
        return -1