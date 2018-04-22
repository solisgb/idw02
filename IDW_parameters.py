# -*- coding: Latin-1 -*-
"""
Created on Sun Mar 25 17:52:37 2018

@author: solis
parámetros del script
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

"""base de dato con las estaciones con datos y huecos"""
DB = r'C:\Users\solis\Documents\aemet\DB\AEMET_CHS.accdb'
# DB = r'C:\Users\solil\Documents\BBDD\AEMET_CHS\AEMET_CHS.accdb'

"""voids in P series: select que busca en DB las estaciones y fechas sin datos
   este select es especifico de la serie que se quiere rellenar y debe estar
   ordenado por fecha. El formato de fecha de Access es '#mm/dd/aaaa#'"""
SELECT_V = """SELECT Estaciones.X, Estaciones.Y, P_voids.ID, P_voids.FECHA
             FROM Estaciones INNER JOIN P_voids ON Estaciones.ID = P_voids.ID
             WHERE P_voids.FECHA>=#1/1/1965#
             ORDER BY P_voids.FECHA, P_voids.ID;"""

"""data in P series: select to retrieve data for each fecha
   Al igual que el anterior es específico de la serie que se quiere rellenar"""
SELECT_D = """SELECT Estaciones.X, Estaciones.Y, PD.VALUE
    FROM Estaciones INNER JOIN PD ON Estaciones.ID = PD.ID
    WHERE FECHA=?"""

"""Tamaño del bufer para escribir el fichero de resultados"""
BUFSIZE = 1024000

"""directorio de resultados"""
DIR_OUT = r'C:\Users\solis\Documents\aemet\DB\out'

"""Nombre delfichero de resultados"""
F_OUT = 'p_idw.txt'
