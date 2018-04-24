# -*- coding: Latin-1 -*-
"""
Created on Sun Apr 22 10:45:42 2018

@author: solis
"""

"""potencia a la que se eleva la funci�n de interpolaci�n
   (valor fuertemente recomendado 2)"""
POWER = 2

"""distancia m�xima hasta la cual el valor interpolado es igual a la de la
   estaci�n con dato"""
DIST_MIN = 1.

"""N�mero m�nimo de puntos con datos en todo el dominio en una fecha para
interpolar (no confundir con el n�mero m�nimo de datos para interpolar una
estaci�n sin dato en una determinada fecha"""
NUM_MIN_DATA_POINTS = 2

"""fecha inicial de la interpolaci�n formato dd/mm/aaaa"""
FECHA_INICIAL = '01/10/1985'

"""fecha final de la interpolaci�n formato dd/mm/aaaa"""
FECHA_FINAL = '01/10/2017'

"""base de dato con las estaciones con datos. Las series de datos en la
   DB puede tener huecos"""
# DB = r'C:\Users\solis\Documents\aemet\DB\AEMET_CHS.accdb'
DB = r'C:\Users\solil\Documents\BBDD\AEMET_CHS\AEMET_CHS.accdb'

"""select to retrieve data for each fecha de DB"""
SELECT_D = """SELECT Estaciones.X, Estaciones.Y, PD.VALUE
    FROM Estaciones INNER JOIN PD ON Estaciones.ID = PD.ID
    WHERE FECHA=?"""

"""fichero de texto con las coordenadas de los puntos en los que se desea
       hacer la interpolaci�n. El formato del fichero es:
           # ID\tX\tY (C�digo del punto coordenada X coordenada Y) y
           continuaci�n tantos puntos como se desee, con formato 
           entero, real-entero, real-entero"""
FILE_POINTS = r'\\intsrv1008\SGD\00_Proyectos\42142\100_TRABAJO\100_10_DOC_COMUN\MARIA\RECARGA\meteoro_points.txt'

"""Tama�o del bufer para escribir el fichero de resultados"""
BUFSIZE = 1024000

"""directorio de resultados"""
DIR_OUT = r'C:\Users\solil\Documents\TMP'

"""Nombre delfichero de resultados"""
F_OUT = 'PD_scatter_idw.txt'
