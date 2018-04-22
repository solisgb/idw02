# -*- coding: Latin-1 -*-
"""
Created on Sun Apr 22 10:45:42 2018

@author: solis
"""

"""potencia a la que se eleva la función de interpolación
   (valor fuertemente recomendado 2)"""
POWER = 2

"""distancia máxima hasta la cual el valor interpolado es igual a la de la
   estación con dato"""
DIST_MIN = 1.

"""Número mínimo de puntos con datos en todo el dominio en una fecha para
interpolar (no confundir con el número mínimo de datos para interpolar una
estación sin dato en una determinada fecha"""
NUM_MIN_DATA_POINTS = 2

"""fecha inicial de la interpolación formato dd/mm/aaaa"""
FECHA_INICIAL = '01/01/1985'

"""fecha final de la interpolación formato dd/mm/aaaa"""
FECHA_FINAL = '01/12/2017'

"""base de dato con las estaciones con datos. Las series de datos en la
   DB puede tener huecos"""
DB = r'C:\Users\solis\Documents\aemet\DB\AEMET_CHS.accdb'

"""select to retrieve data for each fecha de DB"""
SELECT_D = """SELECT Estaciones.X, Estaciones.Y, PD.VALUE
    FROM Estaciones INNER JOIN PD ON Estaciones.ID = PD.ID
    WHERE FECHA=?"""

"""fichero de texto con las coordenadas de los puntos en los que se desea
       hacer la interpolación"""
FILE_POINTS = r'C:\Users\solis\Documents\GIS\meteoro_points.txt'

"""Tamaño del bufer para escribir el fichero de resultados"""
BUFSIZE = 1024000

"""directorio de resultados"""
DIR_OUT = r'C:\Users\solis\Documents\aemet\DB\out'

"""Nombre delfichero de resultados"""
F_OUT = 'p_scatter_idw.txt'
