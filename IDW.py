# -*- coding: Latin-1 -*-
"""
Created on Sun Mar 25 17:58:36 2018

@author: solis
"""

import numpy as np
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
            xy.append([[row.C_X, row.C_Y]])
        else:
            data_in_fecha(con, fecha, cod, xy)
            cod = [row.ID]
            xy = [[row.C_X, row.C_Y]]

    cur.close()
    con.close()


def data_in_fecha(con, fecha, codv, xyv):
    """
    para la fecha hay len(cod) puntos de coordenadas xv = [x1, x2...]
    yv = [y1, y2...] sin datos
    se seleccionan en con los puntos con datos para fecha
    se forma un kdtree con los puntos con datos
    se llama a idw para calcular los valores de los puntos sin datos
    """
    from scipy import spatial
    import IDW_parameters as par
    cur = con.cursor()
    cur.execute(par.select_d)
    rows = [row for row in cur]
    cur.close()
    xd = np.array([row.C_X for row in rows], dtype=np.float32)
    yd = np.array([row.C_Y for row in rows], dtype=np.float32)
    # the name of the 3rd element varies in each select
    data = np.array([row[2] for row in rows], dtype=np.float32)
    tree = spatial.cKDTree(xd, yd)
    n = len(xyv)
    d, ii = tree.query(xyv, k=n)
    data_in_quadrant(xyv, xd, yd, data, d, ii)


def data_in_quadrant(xyv, xd, yd, data, d, ii):
    """
    para cada punto sin dato de coordenadas xyv1
    selecciona los 4 puntos más próximos en cada cuadrante
    """
    d_selected = []
    q_data_selected = []
    q1p = np.array([0, 0, 0, 0], dtype=np.int32)
    for xyv1 in xyv:
        xc = xd - xyv1[0]
        yc = yd - xyv1[1]
        iq = get_quadrant(xc, yc)
        d1p = []
        for i in range(len(iq)):
            if q1p[iq[i]-1] == 0:
                q1p[iq[i]-1] = 1
                d1p.append() = d[0]
                if np.sum(q1p) == 4:
                    d_selected.append(d1p)
                    q_data_selected.append(q1p)
                    break
        if np.sum(q1p) < 4:
            d_selected.append(d1p)
            q_data.append(q1p)
    return 
            
            
            


def get_quadrant(xs, ys):
    """
    dados dos np.array xs ys con igual numero de elementos
    xs contiene las coordenadas x de una serie de puntos
    ys contiene las coordenadas y de la misma serie de puntos
    devuelve el cuadrante de capa punto
    """
    bxs = xs >= 0
    bys = ys >= 0
    ixs = bxs.astype(np.int32)
    iys = bys.astype(np.int32)
    return 3 + ixs - iys - 2 * ixs * iys


def idw(d, ii, power):
    """
    realiza la interpolación
    """
    pass
    
        
    
    
        
        
