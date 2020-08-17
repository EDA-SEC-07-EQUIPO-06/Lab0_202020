"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad de Los Andes
 * 
 * Contribución de:
 *
 * Cristian Camilo Castellanos
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
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

"""
  Este módulo es una aplicación básica con un menú de opciones para cargar datos, contar elementos, y hacer búsquedas sobre una lista.
"""

import config as cf
import sys
import csv
from time import process_time 

def loadCSVFile (file, lst, sep=";"):
    """
    Carga un archivo csv a una lista
    Args:
        file 
            Archivo de texto del cual se cargaran los datos requeridos.
        lst :: []
            Lista a la cual quedaran cargados los elementos despues de la lectura del archivo.
        sep :: str
            Separador escodigo para diferenciar a los distintos elementos dentro del archivo.
    Try:
        Intenta cargar el archivo CSV a la lista que se le pasa por parametro, si encuentra algun error
        Borra la lista e informa al usuario
    Returns: None   
    """
    del lst[:]
    print("Cargando archivo ....")
    t1_start = process_time() #tiempo inicial
    dialect = csv.excel()
    dialect.delimiter=sep
    try:
        with open(file, encoding="utf-8") as csvfile:
            spamreader = csv.DictReader(csvfile, dialect=dialect)
            for row in spamreader: 
                lst.append(row)
    except:
        del lst[:]
        print("Se presento un error en la carga del archivo")
    
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución ",t1_stop-t1_start," segundos")

def printMenu():
    """
    Imprime el menu de opciones
    """
    print("\nBienvenido")
    print("1- Cargar Datos")
    print("2- Contar los elementos de la Lista")
    print("3- Contar elementos filtrados por palabra clave")
    print("4- Consultar elementos a partir de dos listas")
    print("0- Salir")

def countElementsFilteredByColumn(criteria, column, lst):
    """
    Retorna cuantos elementos coinciden con un criterio para una columna dada  
    Args:
        criteria:: str
            Critero sobre el cual se va a contar la cantidad de apariciones
        column
            Columna del arreglo sobre la cual se debe realizar el conteo
        list
            Lista en la cual se realizará el conteo, debe estar inicializada
    Return:
        counter :: int
            la cantidad de veces ue aparece un elemento con el criterio definido
    """
    if len(lst)==0:
        print("La lista esta vacía")  
        return 0
    else:
        t1_start = process_time() #tiempo inicial
        counter=0 #Cantidad de repeticiones
        for element in lst:
            if criteria.lower() in element[column].lower(): #filtrar por palabra clave 
                counter+=1
        t1_stop = process_time() #tiempo final
        print("Tiempo de ejecución ",t1_stop-t1_start," segundos")
    return counter

def countElementsByCriteria(director, lst, otra):
    """
    Retorna la cantidad de elementos que cumplen con un criterio para una columna dada
    """
    if len(lst)!= len(otra):
        print("listas incongruentes")
        return 0
    else:
        t1_start = process_time() #tiempo inicial
        counter= 0
        puntaje_total=0
        referencia=""
        respuesta= (0,0)
        for element in otra: #recorre elementos en lista 2
            if director.lower() in element["director_name"].lower(): #filtra por director
                referencia= (element["id"]) #recupera id de pelicula
                for element2 in lst: #recorre elementos en lista 1
                    if referencia in element2["id"]: #filtra por id de pelicula
                        puntaje= float(element2["vote_average"])
                        if puntaje >= 6.0:
                            counter+= 1
                            puntaje_total+= puntaje
        respuesta= (counter, puntaje_total/counter)
        t1_stop= process_time()
        print("Tiempo de ejecución ",t1_stop-t1_start," segundos")
    return respuesta

            

def main():
    """
    Método principal del programa, se encarga de manejar todos los metodos adicionales creados

    Instancia una lista vacia en la cual se guardarán los datos cargados desde el archivo
    Args: None
    Return: None 
    """
    lista1 = [] #instanciar una lista vacia
    lista2 = [] #instancia otra lista vacia
    while True:
        printMenu() #imprimir el menu de opciones en consola
        inputs =input('Seleccione una opción para continuar\n') #leer opción ingresada
        if len(inputs)>0:
            if int(inputs[0])==1: #opcion 1
                loadCSVFile("Data/SmallMoviesDetailsCleaned.csv", lista1) #llamar funcion cargar datos
                print("Datos cargados, "+str(len(lista1))+" elementos cargados")
                loadCSVFile("Data/MoviesCastingRaw-small.csv",lista2) #carga datos lista 2
                print("Datos cargados, "+str(len(lista2))+" elementos cargados")
            elif int(inputs[0])==2: #opcion 2
                if len(lista1)==0: #obtener la longitud de la lista
                    print("La lista 1 esta vacía")    
                else: print("La lista 1 tiene "+str(len(lista1))+" elementos")
                if len(lista2)==0: #longitud lista 2 (deberia ser igual a la 1 para funionar)
                    print("La lista 2 esta vacía")
                else: print("La lista 2 tiene "+str(len(lista2))+" elementos")
            elif int(inputs[0])==3: #opcion 3
                criteria =input('Ingrese el genero de búsqueda\n')
                counter=countElementsFilteredByColumn(criteria, "genres", lista1) #filtrar una columna por criterio  
                print("Coinciden ",counter," elementos con el crtierio: ", criteria  )
            elif int(inputs[0])==4: #option 4
                director =input('Ingrese el director de búsqueda\n')
                respuesta=countElementsByCriteria(director, lista1, lista2)
                counter=respuesta[0]
                promedio=respuesta[1]
                print("Coinciden ",counter," elementos del director: ", director ," con puntaje igual o mayor a 6 puntos. El promedio de puntaje es ", promedio)
            elif int(inputs[0])==0: #opcion 0, salir
                sys.exit(0)

if __name__ == "__main__":
    main()

def encontrar_buenas_peliculas(peliculas:dict):
    
    buenasPeli =[]
    if i in peliculas :

       if ( (pelicula["vote_average"] >= 6)) and peliculas[i]== pelicula["director_name"]:

           buenasPeli.append(peliculas[i])

return buenasPeli