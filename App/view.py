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
import datetime
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.ADT import map as mp
assert cf
import model
from DISClib.DataStructures import mapentry as me
from DISClib.DataStructures import listiterator as it


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
        catalog=controller.loadData(cont)
        time=catalog['time']
        x='7:15:03'
        info=datetime.datetime.strptime(x,'%H:%M:%S')
        t=info.time()
        x=om.get(time,t)
        value=me.getValue(x)
        print(value)
        
    elif int(inputs[0])==3:
        minimo=float(input('Ingrese el valor mínimo del rango: '))
        maximo=float(input('Ingrese el valor máximo del rango: '))
        feature=input('Ingrese la característica de contenido: ')
        print(controller.req1(minimo,maximo,feature.lower(),catalog))

    elif int(inputs[0])==4:
        minenergy=float(input('Valor inferior energy: '))
        maxenergy=float(input('Valor superior energy: '))
        mindance=float(input('Valor inferior danceability: '))
        maxdance=float(input('Valor superior danceability: '))
        controller.req2(catalog,minenergy,maxenergy,mindance,maxdance)

    elif int(inputs[0])==5:
        mininstrum=float(input('Valor inferior instrumentalness: '))
        maxinstrum=float(input('Valor superior instrumentalness: '))
        mintempo=float(input('Valor inferior tempo: '))
        maxtempo=float(input('Valor superior tempo: '))
        controller.req3(catalog,mininstrum,maxinstrum,mintempo,maxtempo)
    
    elif int(inputs[0])==6:
        x=int(input('¿Desea conocer información sobre géneros ya existentes? [0: sí // 1: no]: '))
        if x==0:
            genres=input('¿Cuáles? [escríbalos separados por una coma y espacio. Ej: reggae, hip-hop]: ')
            lista=(genres.lower()).split(', ')
            for genre in lista:
                controller.req4(catalog,genre,None,None)
            print('\n')
        y=int(input('¿Desea conocer información sobre un género no existente? [0: sí // 1: no]: '))
        if y==0:
            name=input('Ingrese el nombre del nuevo género: ')
            minim=float(input('Ingrese el valor mínimo de tempo: '))
            maxim=float(input('Ingrese el valor máximo de tempo: '))
            controller.req4(catalog,name,minim,maxim)
            print('\n')
        
    elif int(inputs[0])==9:
        x='7:15:00'
        info=datetime.datetime.strptime(x,'%H:%M:%S')
        time=info.time()
        y='7:25:00'
        info1=datetime.datetime.strptime(y,'%H:%M:%S')
        time1=info1.time()
        controller.req5(catalog,time,time1)



    else:
        sys.exit(0)
sys.exit(0)
