# -*- coding: Latin-1 -*-
"""
Created on Sun Mar 25 17:52:37 2018

@author: solis
parámetros del script
"""

# potencia a la que se eleva el método idw
power = 2

# bases de datos de datos y huecos
# DB = r'E:\WORK\CHS\aemet\out\AEMET_CHS.accdb'
DB = r'C:\Users\solis\Documents\aemet\DB\AEMET_CHS.accdb'

# voids in P series: select que busca en DB las estaciones y fechas sin datos
select_v = """SELECT Estaciones.C_X, Estaciones.C_Y, P_voids.ID, P_voids.FECHA
    FROM Estaciones INNER JOIN P_voids ON Estaciones.ID = P_voids.ID
    WHERE P_voids.FECHA=#1/1/1965#
    ORDER BY P_voids.FECHA"""

# data in P series: select to retrieve data for each fecha
select_d = """SELECT Estaciones.C_X, Estaciones.C_Y, P.P
    FROM Estaciones INNER JOIN P ON Estaciones.ID = P.ID
    WHERE FECHA=?"""

# directorio de resultados
dir_out = r'E:\WORK\CHS\aemet\out'

# P results: name file
fpout = 'p_idw.txt'
