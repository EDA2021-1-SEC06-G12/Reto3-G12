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
from DISClib.DataStructures import listiterator as it
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import list as lt


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

    events2file=cf.data_dir+'user_track_hashtag_timestamp-small.csv'
    input2_file = csv.DictReader(open(events2file, encoding="utf-8"),delimiter=",")
    for evento in input2_file:
        model.addevent2(catalog,evento)

    return catalog
    
def req1(mayor,menor,content,catalog):
    mapa=model.req1(content,catalog)
    llaves=om.keys(mapa,mayor,menor)
    i=it.newIterator(llaves)
    artists=0
    events=0
    altura=om.height(mapa)
    num=om.size(mapa)
    while it.hasNext(i):
        entry=om.get(mapa,it.next(i))
        valor=me.getValue(entry)
        art=lt.size(valor['artists'])
        artists+=art
        events+=valor['events']
    return artists,events,altura,num


# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
