# -*- coding: Latin-1 -*-
"""
Created on Sun Mar 25 17:58:36 2018

@author: solis
"""

import pyodbc


def rellenar_huecos():
    """
    hago una conexión a la BD
    busco los puntos sin dato, ordenados por fechas
    para cada fecha paso a interpola la fecha, los codigos de los puntos
    sin datos cod y sus coordenadas
    len(cod)=len(xy)
    len(xy[0])=2
    """

    import connexion_str as cstr
    import IDW_parameters as par

    a = cstr.conexion_str_get(par.DB)
    con = pyodbc.connect(a)
    cur = con.cursor()
    cur.execute(par.select_v)
    N = 0
    flag = 0
    for row in cur:
        if flag == N:
            flag = 1
            fecha = row.FECHA
            cod = []
            xy = []

        if fecha == row.FECHA:
            cod.append(row.ID)
            xy.append([row.C_X, row.C_Y])
        else:
            interpola(fecha, cod, xy)
            cod = [row.ID]
            xy = [[row.C_X, row.C_Y]]

    cur.close()
    con.close()


def interpola(con, fecha, cod, xy):
    """
    para la fecha hay len(cod) puntos de coordenadas xy = [[x1, y1]...]
    sin datos
    se seleccionan en con los puntos con datos para fecha
    se forma un kdtree con los puntos con datos
    se llama a idw para calcular los valores de los puntos sin datos
    """
    import numpy as np
    from scipy import spatial
    import IDW_parameters as par
    cur = con.cursor()
    cur.execute(par.select_d)
    rows = [row for row in cur]
    cur.close()
    xd = np.array([row[0] for row in rows], dtype=np.float32)
    yd = np.array([row[1] for row in rows], dtype=np.float32)
    tree = spatial.KDTree(xd, yd)
    n = len(xy)
    d, ii = tree.query(xy, k=n)
    v_interpolated = idw(d, ii, par.power)

    def getQuadrant(xs, ys):
        """
        dados dos np.array xs ys con igual numero de elementos
        xs contiene las coordenadas x de una serie de puntos
        ys contiene las coordenadas y de la misma serie de puntos
        devuelve el cuadrante de capa punto
        """
        assert xs.size==ys.size, 'xy ys must have equal size'
        bxs=xs>=0
        bys=ys>=0
        ixs=np.zeros(len(bxs), np.int32)
        iys=np.zeros(len(bys), np.int32)
        ixs[:]=bxs[:]
        iys[:]=bys[:]
        return 3 + ixs - iys - 2 * ixs * iys


def idw(d, ii, power):
    """
    realiza la interpolación
    """
    pass
    
        
    
    
        
        
