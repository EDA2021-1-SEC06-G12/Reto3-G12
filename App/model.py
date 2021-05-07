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
    catalog = {'eventos':None,'energy':None,'instrumentalness':None}
    catalog['eventos']=lt.newList()
    catalog['energy']=om.newMap()
    catalog['instrumentalness']=om.newMap()

    return catalog

def addevent(catalog,event):
    """
    """
    lista=catalog['eventos']
    lt.addLast(lista,event)
    addtomap(catalog,event,'energy','danceability')
    addtomap(catalog,event,'instrumentalness','tempo')
    
    
def addtomap(catalog,event,feature,feature2):
    mapa=catalog[feature]
    llave=float(event[feature])
    feat2=float(event[feature2])
    ide=event['track_id']
    if om.contains(mapa,llave):
        pareja=om.get(mapa,llave)
        value=me.getValue(pareja)
        tracks=value['tracks']
        if lt.isPresent(tracks,ide)==0:
            lt.addLast(tracks,ide)
            lt.addLast(value['f2'],feat2)
    else:
        entrada=newentry(llave,feat2,ide)
        om.put(mapa,llave,entrada)

def newentry(llave,f2,ide):
    entry={'llave':llave,'tracks':None,'f2':None}
    entry['tracks']=lt.newList(datastructure='ARRAY_LIST')
    lt.addLast(entry['tracks'],ide)
    entry['f2']=lt.newList(datastructure='ARRAY_LIST')
    lt.addLast(entry['f2'],f2)
    return entry

def req1(content,catalog):
    mapa=om.newMap()
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


def requ2(catalog,feature1,feature2,min1,max1,min2,max2):
    mapa=catalog[feature1]
    tracks=om.values(mapa,min1,max1)
    final=0
    i=it.newIterator(tracks)
    while it.hasNext(i):
        entrada=it.next(i)
        f2=entrada['f2']
        ite=1
        while ite<=lt.size(f2):
            feat=lt.getElement(f2,ite)
            if feat<=max2 and feat>=min2:
                final+=1
    return final


def newcontextentry(event,content):
    entry={'valor':float(event[content]),'artists':None,'events':1}
    entry['artists']=lt.newList()
    lt.addLast(entry['artists'],event['artist_id'])
    return entry



    


# Funciones para agregar informacion al catalogo
# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento