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

from datetime import datetime
import config as cf
import model
import csv
from DISClib.DataStructures import listiterator as it
from DISClib.ADT import orderedmap as om
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import list as lt
from DISClib.Algorithms.Sorting import mergesort as mrge
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
    
    file3=cf.data_dir+'sentiment_values.csv'
    input_file3=csv.DictReader(open(file3, encoding="utf-8"),delimiter=",")
    for hashtag in input_file3:
        if hashtag['vader_avg']!='':
            model.addhashtag(catalog,hashtag['hashtag'],hashtag['vader_avg'])

    file1=cf.data_dir+'user_track_hashtag_timestamp-small.csv'
    input_file1 = csv.DictReader(open(file1, encoding="utf-8"),delimiter=",")
    for event in input_file1:
        model.addpromtrack(catalog,event)

    file2=cf.data_dir + 'context_content_features-small.csv'
    input_file2 = csv.DictReader(open(file2, encoding="utf-8"),delimiter=",")
    
    for event in input_file2:
        model.addevent(catalog,event)

    return catalog

def req1(menor,mayor,feature,catalog):
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    events = om.values(catalog[feature],menor,mayor)
    num_events = model.numevents(events)
    lista_artistas = model.list_art(events)
    mapa = mp.newMap(maptype="PROBING",loadfactor=0.5)

    i = it.newIterator(lista_artistas)
    while it.hasNext(i):
        artist = it.next(i)
        mp.put(mapa, artist, None)
    artists = mp.size(mapa)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    print('\n'+(feature.capitalize())+' is between '+str(menor)+' and '+str(mayor)+'\nTotal of reproduction: '+str(num_events)+'\nTotal of unique artists: '+str(artists)+'\n')

    return delta_time, delta_memory

def req2(catalog,min_en,max_en,min_dan,max_dan):
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    keys1 = om.values(catalog["energy"],min_en,max_en)
    lista1 = model.listaeventos(catalog["energy"],keys1)
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

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    n = 1
    listakeys = mp.keySet(mapafin)
    while n<=5:
        llave = lt.getElement(listakeys, n)
        event = mp.get(mapafin,llave)["value"]

        print('Track '+str(n)+': '+ event["track_id"]+' with energy of '+str(event["energy"])+' and danceability of '+str(event["danceability"]))
        n +=1
    print('\n')

    return delta_time, delta_memory

def req3(catalog,min_inst,max_inst,min_temp,max_temp):
    keys1 = om.values(catalog["tempo"],min_temp,max_temp)
    lista1 = model.listaeventos(catalog["tempo"],keys1)
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

    mapa = catalog["tempo"]
    if minimo==None and maximo==None:
        if genre=='reggae':
            menor=60.0
            mayor=90.0
        elif genre=='down-tempo':
            menor=70.0
            mayor=100.0
        elif genre=='chill-out':
            menor=90.0
            mayor=120.0
        elif genre=='hip-hop':
            menor=85.0
            mayor=115.0
        elif genre=='jazz and funk':
            menor=120.0
            mayor=125.0
        elif genre=='pop':
            menor=100.0
            mayor=130.0
        elif genre=='r&b':
            menor=60.0
            mayor=80.0
        elif genre=='rock':
            menor=110.0
            mayor=140.0
        elif genre=='metal':
            menor=100.0
            mayor=160.0
    else:
        menor=minimo
        mayor=maximo

    events = om.values(mapa,menor,mayor)
    num_events = model.numevents(events)
    lista_artistas = model.list_art(events)
    mapa = mp.newMap(maptype="PROBING",loadfactor=0.5)

    i = it.newIterator(lista_artistas)
    while it.hasNext(i):
        artist = it.next(i)
        mp.put(mapa, artist, None)
    artists = mp.size(mapa)

    listartists=mp.keySet(mapa)

    print('\n======= '+genre.upper()+' ========'+'\nFor '+genre+' the tempo is between '+str(menor)+' and '+str(mayor)+'\n'+genre+' reproductions: '+str(num_events)+' with '+str(artists)+' different artists'+'\n\n---- Some artists for '+genre+' -----\n')
    i=it.newIterator(listartists)
    n=1
    while it.hasNext(i) and n<=5:
        artist=it.next(i)
        print('Artist '+str(n)+': '+artist)
        n+=1



def req5(catalog,minim,maxim):
    mapa=mp.newMap()
    total=0
    mayor=None
    uniques=[]
    tuplas=[]
    lista=om.values(catalog['time'],minim,maxim)
    mapa=model.genresandtracks(lista)
    keys=mp.keySet(mapa)
    i=it.newIterator(keys)
    while it.hasNext(i):
        key=it.next(i)
        x=mp.get(mapa,key)
        entry=me.getValue(x)
        unique=mp.size(entry['unique'])
        uniques.append(unique)
        total+=unique
        tupla=unique,key
        tuplas.append(tupla)
    x=sorted(uniques,reverse=True)
    print('\nThere is a total of '+str(total)+' reproductions between '+str(minim)+' and '+str(maxim))
    print('========== GENRES SORTED REPRODUCTIONS ==========')
    i=1
    for num in x:
        for tupla in tuplas:
            if tupla[0]==num:
                print('TOP '+str(i)+': '+tupla[1].capitalize()+' with '+str(num)+' reps')
                if i==1:
                    mayor=tupla
                i+=1
    pareja=mp.get(mapa,mayor[1])
    entry=me.getValue(pareja)
    tracks=mp.keySet(entry['tracks'])
    print('\nThe TOP GENRE is '+mayor[1].capitalize()+' with '+str(mayor[0])+' reproductions')
    print('========== '+mayor[1].upper()+' SENTIMENT ANALYSIS ==========')
    print(mayor[1].capitalize()+' has '+str(lt.size(tracks))+' unique tracks')
    mapafinal=model.numhts(tracks,catalog)
    llavesnumhts=(om.keySet(mapafinal))
    n=it.newIterator(llavesnumhts)
    listanum=[]
    m=1
    while it.hasNext(n):
        numht=it.next(n)
        listanum.append(numht)
    orderedlistanum=sorted(listanum,reverse=True)
    for num in orderedlistanum:
        while m<=10:
            partuplas=om.get(mapafinal,num)
            listatuplas=me.getValue(partuplas)
            t=it.newIterator(listatuplas)
            while it.hasNext(t) and m<=10:
                tupla=it.next(t)
                print('TOP '+str(m)+' track: '+tupla[0]+' with '+str(num)+' hashtags and VADER = '+str(tupla[1]))
                m+=1
    print('\n')


"""    mapa=catalog['hashtagsportrack']
    m=1
    print('10 of these tracks are...')
    while it.hasNext(d) and m<=10:
        track=it.next(d)
        par=mp.get(mapa,track)
        hts=me.getValue(par)
        nums=model.promedio(catalog,hts)
        if nums!=None:
            print('Track '+str(m)+': '+track+' with '+str(nums[1])+' hashtags and VADER = '+str(nums[0]/nums[1]))
            m+=1
    print('\n')"""



"""
def req5prueba(catalog,minim,maxim):
   lista=om.values(catalog['time'],minim,maxim)
   mapa_tempo = om.newMap(omaptype="RBT")
   i1 = it.newIterator(lista)
   reproducciones = 0
   while it.hasNext(i1):
    entrada = it.next(i1)
    events = entrada["events"]

    i2 = it.newIterator(events)
    while it.hasNext(i2):
        event = it.next(i2)
        model.addtomap2(mapa_tempo,event,"tempo")
        reproducciones += 1
   
   lista_a_sortear = lt.newList("ARRAY_LIST")
   lista=("reggae, down-tempo, chill-out, hip-hop, jazz and funk, pop, r&b, rock, metal".lower()).split(', ')
   for genre in lista:
       lt.addLast(lista_a_sortear, auxiliar(catalog,genre,None,None,"req5",mapa_tempo))

   mrge.sort(lista_a_sortear, cmpgenres)
   m = 1
   suma = 0
   while m<=9:
       ele = lt.getElement(lista_a_sortear, m)
       suma += ele[1]
       m+=1

   print("There is a total of " + str(suma) + +" reproductions between"+ str(minim) +" and "+ str(maxim))

   n = 1
   while n<=9:
       ele = lt.getElement(lista_a_sortear, n)
       print("TOP " + str(n) + ": " + str(ele[0]) + " with " + str(ele[1]) + " reps")
       n+=1
   genre = lt.getElement(lista_a_sortear, 1) 
   if genre=='reggae':
        menor=60.0
        mayor=90.0
   elif genre=='down-tempo':
        menor=70.0
        mayor=100.0
   elif genre=='chill-out':
        menor=90.0
        mayor=120.0
   elif genre=='hip-hop':
        menor=85.0
        mayor=115.0
   elif genre=='jazz and funk':
        menor=120.0
        mayor=125.0
   elif genre=='pop':
        menor=100.0
        mayor=130.0
   elif genre=='r&b':
        menor=60.0
        mayor=80.0
   elif genre=='rock':
        menor=110.0
        mayor=140.0
   elif genre=='metal':
        menor=100.0
        mayor=160.0
  
   lista_mayor = om.values(mapa_tempo,menor,mayor)
   lista_eventos = model.listaeventos(mapa_tempo, lista_mayor)

   mapa_trac = mp.newMap(maptype="PROBING",loadfactor=0.5)
   i3 = it.newIterator(lista_eventos)
   while it.hasNext(i3):
       evento = it.next(i3)
       mp.put(mapa_trac,evento["track_id"],None)
   
   tracks_unicos = mp.keySet(mapa_trac)



    


def auxiliar(catalog,genre,minimo,maximo,req,mapa):
    if req == "req5":
        mapa = mapa
    else: 
        mapa = catalog["tempo"]
    menor = None
    mayor = None
    if minimo==None and maximo==None:
        if genre=='reggae':
            menor=60.0
            mayor=90.0
        elif genre=='down-tempo':
            menor=70.0
            mayor=100.0
        elif genre=='chill-out':
            menor=90.0
            mayor=120.0
        elif genre=='hip-hop':
            menor=85.0
            mayor=115.0
        elif genre=='jazz and funk':
            menor=120.0
            mayor=125.0
        elif genre=='pop':
            menor=100.0
            mayor=130.0
        elif genre=='r&b':
            menor=60.0
            mayor=80.0
        elif genre=='rock':
            menor=110.0
            mayor=140.0
        elif genre=='metal':
            menor=100.0
            mayor=160.0
    else:
        menor=minimo
        mayor=maximo

    events = om.values(mapa,menor,mayor)
    num_events = model.numevents(events)
    return (genre,num_events)


    
    
#    print(mp.size(m))

"""
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

def comparedates(date1,date2):
    if date1==date2:
        return 0
    elif date1>date2:
        return 1
    else:
        return -1

def cmpgenres(genre1,genre2):
    return (genre1[1])>=(genre2[1])