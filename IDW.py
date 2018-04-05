# -*- coding: Latin-1 -*-
"""
Created on Sun Mar 25 17:58:36 2018

@author: solis
"""

import numpy as np
import pyodbc


def rellenar_huecos():
    """
    1. hago una conexión a la BD
    2. busco los puntos sin dato, ordenados por fechas
    3. para cada fecha busco todas las estaciones sin dato en esa fecha y
       cojo su codigo y coordenadas
    4. cuando cambia la fecha llamo a la función data_in_fecha
    ________________________________
    cod. lista de códigos de estaciones sin dato en fecha
    xy. lista de coordenadas de cada estación sin dato
    len(cod)=len(xy)
    xy.shape=[len(cod), 2]
    """

    import db_con_str
    import IDW_parameters as par

    a = db_con_str.con_str(par.DB)
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
            xy.append([[row.X, row.Y]])
        else:
            data_in_fecha(con, fecha, cod, np.array(xy, dtype=np.float32)
            cod = [row.ID]
            xy = [[row.X, row.Y]]

    cur.close()
    con.close()


def data_in_fecha(con, fecha, codv, xyv):
    """
    para la fecha hay len(codv) puntos de coordenadas xyv = [[x1, y1], ...]
    sin datos
    1. se ejecuta un select que devuelve los puntos con datos para fecha
    2. se forma un kdtree con los puntos con datos
    3. se ejecuta un kdtree query pata ordenar a distancias dist crecientes 
       cada punto sin datos con respecto a los puntos con datos,también 
       devuelve la lista de los índices ii, de modo que se puede identificar
       cada punto con datos
    4. se llama a la función data_in_quadrant
    """
    from scipy import spatial
    import IDW_parameters as par
    cur = con.cursor()
    cur.execute(par.select_d)
    rows = [row for row in cur]
    cur.close()
    xyd = np.array([[row.X, row.Y] for row in rows], dtype=np.float32)
    # the name of the 3rd element varies in each select
    z = np.array([row[2] for row in rows], dtype=np.float32)
    tree = spatial.cKDTree(xyd)
    n = len(xyv)
    dist, ii = tree.query(xyv, k=n)
    data_in_quadrant(xyv, xyd, z, dist, ii)


def data_in_quadrant(xyv, xyd, data, d, ii):
    """
    para cada punto sin dato de coordenadas xyv1 selecciona los 4 puntos más
    próximos en cada cuadrante
    1. Para cada xyv1 hace una traslación de coordenadas de modo que xyv1
       se quede en el centro de coornadas -> xt, yt
    2. Calcula el cuadrante de los puntos con datos llamando a la función
       get_quadrant
    """
    dist_selected = []
    data_selected = []
    q1p = np.zeros((4), dtype=np.int32)
    for xyv1 in xyv:
        xt = xyd[:,0] - xyv1[:,0]
        yt = xyd[:,1] - xyv1[:,1]
        iq = get_quadrant(xt, yt)
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
    
        
    
    
        
        
