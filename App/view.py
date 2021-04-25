"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.ADT import map as mp
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Cargar información de eventos")
    print("3- Consultar número de eventos en un rango para una característica de contenido")
    print("4- Consultar canciones de fiesta")
    print("5 - Consultar canciones para estudiar")
    print("6 - Consultar número de canciones para un género")
    print("0- Salir")

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("")
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:
        catalog = controller.loadData(cont)
        print("")
        print("Total de registros de eventos de escucha cargados: " + str(lt.size(catalog["eventos"])))
        print("Total de artistas unicos cargados: " + str(mp.size(catalog["artistas"])))
        print("Total de pistas de audio únicas guardadas: " + str(mp.size(catalog["pistas"])))
        print("Primeros 5 eventos de escucha cargados: ")
        i = 1
        while i <= 5:
            elem = lt.getElement(catalog["eventos"], i)
            print("|" + str(i) + "|" + " instrumentalness: " + str(elem["instrumentalness"]) + " liveness: " + str(elem["liveness"])+ " speechiness: " + str(elem["speechiness"]) + " danceability: " + str(elem["danceability"])+ " valence: " + str(elem["valence"]) + " loudness: " + str(elem["loudness"])+ " tempo: " + str(elem["tempo"]) + " acousticness: " + str(elem["acousticness"])+ " energy: " + str(elem["energy"]) + " mode: " + str(elem["mode"])+ " key: " + str(elem["key"]) + " artist_id: " + str(elem["artist_id"]) + " tweet_lang: " + str(elem["tweet_lang"]) + " track_id: " + str(elem["track_id"]) + " created_at: " + str(elem["created_at"]) + " lang: " + str(elem["lang"]) + " time_zone: " + str(elem["time_zone"]) + " user_id: " + str(elem["user_id"]) + " id: " + str(elem["id"]))
            i += 1

        print("")
        print("Últimos 5 eventos de escucha cargados: " )

        num = 1
        ii = lt.size(catalog["eventos"])
        while ii >=(lt.size(catalog["eventos"])-4):
            elem = lt.getElement(catalog["eventos"], i)
            print("|" + str(num) + "|" + " instrumentalness: " + str(elem["instrumentalness"]) + " liveness: " + str(elem["liveness"])+ " speechiness: " + str(elem["speechiness"]) + " danceability: " + str(elem["danceability"])+ " valence: " + str(elem["valence"]) + " loudness: " + str(elem["loudness"])+ " tempo: " + str(elem["tempo"]) + " acousticness: " + str(elem["acousticness"])+ " energy: " + str(elem["energy"]) + " mode: " + str(elem["mode"])+ " key: " + str(elem["key"]) + " artist_id: " + str(elem["artist_id"]) + " tweet_lang: " + str(elem["tweet_lang"]) + " track_id: " + str(elem["track_id"]) + " created_at: " + str(elem["created_at"]) + " lang: " + str(elem["lang"]) + " time_zone: " + str(elem["time_zone"]) + " user_id: " + str(elem["user_id"]) + " id: " + str(elem["id"]))
            num += 1
            ii -= 1

        #arbol=catalog['events']
        #print('Altura del árbol: '+str(om.height(arbol)))
        #print('Elementos del árbol: '+str(om.size(arbol)))
        #print(om.maxKey(arbol))
        #print(om.minKey(arbol))
        
    elif int(inputs[0])==3:
        minimo=float(input('Ingrese el valor mínimo del rango: '))
        maximo=float(input('Ingrese el valor máximo del rango: '))
        contenido=input('Ingrese la característica de contenido: ')
        x=controller.req1(maximo,minimo,contenido.lower(),catalog)
        print("Tiempo [ms]: "+f"{x[2]:.3f}"+" ||  "+"Memoria [kB]: "+f"{x[3]:.3f}")
        print('Total de eventos de escuchados: '+str(x[1])+' || Número de artistas escuchados: '+str(x[0])+'\n')
        input('Presione enter para continuar')
    
    elif int(inputs[0]) == 4:
        minimoEnergy=float(input('Ingrese el valor mínimo de Energy: '))
        maximoEnergy=float(input('Ingrese el valor máximo de Energy: '))
        minimoDanceability=float(input('Ingrese el valor mínimo de Danceability: '))
        maximoDanceability=float(input('Ingrese el valor máximo de Danceability: '))
        x = controller.req2(minimoEnergy,maximoEnergy,minimoDanceability,maximoDanceability,catalog)
        print("Tiempo [ms]: "+f"{x[2]:.3f}"+" ||  "+"Memoria [kB]: "+f"{x[3]:.3f}")
        print("Total de pistas únicas en eventos: " + str(x[0]))
        print("")
        print("Pistas aleatorias: ")
        i = 1
        while i <= lt.size(x[1]):
            elem = lt.getElement(x[1], i)
            print("Pista " + str(i) + " " + str(elem["track_id"]) + " con energy de " + str(elem["energy"]) + " y danceability de " + str(elem["danceability"]))
            i +=1
        print("")



    else:
        sys.exit(0)
sys.exit(0)
