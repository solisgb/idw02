# -*- coding: Latin-1 -*-
"""
Created on Sun Mar 25 17:58:36 2018

@author: solis

We use the inverse distance wheigthed to interpolate precipitacion and
temperature data.
We use a variant of Shepards method
https://en.wikipedia.org/wiki/Inverse_distance_weighting
We use the nearest data point in each quadrant nearest to a point without data,
    so we have a maximun of 4 points to do the interpolation
The parameters of the script are accesible importing de module IDW_parameters
    and they are not passed as variables in the functions -they work as
    constants
"""

import numpy as np
from scipy import spatial
import pyodbc
import IDW_parameters as par


def fill_voids_idw_quadrants():
    """
    Se utiliza para rellener huecos de una serie de estacines con huecos
       almacenadso en una BDD
    1. hago una conexión a la BD
    2. ejecuto una select que me devuelve las fechas de los id de los puntos
       sin datos y sus coordenadas xyv, ordenadas por fechas
    3. Para cada fecha formo una lista codv de las estaciones sin datos
       y otro lista xyv de las coornadas de los puntos sin datos xyv
    4. cuando cambia la fecha llamo a la función data_in_fecha
    """
    import db_con_str
    from os.path import join
    from math import fmod

    FILE_INCIDENCIAS = 'idw_indicencias.txt'
    NCICLOS = 365

    fo = open(join(par.DIR_OUT, par.F_OUT), 'w', par.BUFSIZE)
    foi = open(join(par.DIR_OUT, FILE_INCIDENCIAS), 'w', par.BUFSIZE)

    a = db_con_str.con_str(par.DB)
    con = pyodbc.connect(a)
    cur = con.cursor()
    cur.execute(par.SELECT_V)
    row = cur.fetchone()
    if row is None:
        raise ValueError('La consulta {} no devuelve filas'.
                         format(par.SELECT_V))
    fecha = row.FECHA
    codv = [row.ID]
    xyv = [[row.X, row.Y]]
    for row in cur:
        if fecha.year == 1966:
            break
        if fecha == row.FECHA:
            codv.append(row.ID)
            xyv.append([row.X, row.Y])
        else:
            if len(codv) == 0:
                a = 'El {} no hay huecos'.format(fecha.strftime('%d/%m/%Y'))
                print(a)
                foi.write('{}\n'.format(a))
                continue
            elif len(codv) == 1:
                xyv = xyv[0]

            xyd, z = select_data(con, fecha)
            if len(z) == 0:
                a = 'El {} no hay datos'.format(fecha.strftime('%d/%m/%Y'))
                print(a)
                foi.write('{}\n'.format(a))
                continue
            fill_fecha(fo, fecha, codv, xyv, xyd, z)
            print('{}'.format(fecha.strftime('%d/%m/%Y')))
            fecha = row.FECHA
            codv = [row.ID]
            xyv = [[row.X, row.Y]]

    flag = True
    if len(codv) == 0:
        a = 'El {} no hay huecos'.format(fecha.strftime('%d/%m/%Y'))
        print(a)
        foi.write('{}\n'.format(a))
        flag = False
    elif len(codv) == 1:
        xyv = xyv[0]

    if flag:
        xyd, z = select_data(con, fecha)
        if len(z) == 0:
            a = 'El {} no hay datos'.format(fecha.strftime('%d/%m/%Y'))
            print(a)
            foi.write('{}\n'.format(a))
            flag = False

    if flag:
        fill_fecha(fo, fecha, codv, xyv, xyd, z)
        print('{}'.format(fecha.strftime('%d/%m/%Y')))

    cur.close()
    con.close()

    fo.flush()
    fo.close()
    foi.flush()
    foi.close()


def select_data(con, fecha):
    """
    con: conexión a la DB abierta en fill_voids_idw_quadrants
    fecha: en la que se seleccionan los datos. SELECT_D debe tener un
        where CAMPO_FECHA=?
    return
    xyd: array 2D con las coordenadas de los puntos con datos
    z: array 1D con el valor de la variable en cada punto con dato
    """
    cur = con.cursor()
    cur.execute(par.SELECT_D, fecha)
    rows = [row for row in cur]
    cur.close()

    if len(rows) < par.NUM_MIN_DATA_POINTS:
        raise ValueError('No hay suficientes datos en la fecha {}'.
                         format(fecha.strftime('%d/%m/%Y')))

    xyd = np.array([[row.X, row.Y] for row in rows], dtype=np.float64)
    z = np.array([row.VALUE for row in rows], dtype=np.float64)
    return xyd, z


def fill_fecha(fo, fecha, codv, xyv, xyd, z):
    """
    fecha: un type(date) en la que hay puntos sin datos
    codv: lista de str con los id de los puntos sin datos
    xyv: lista lista con una coordenada [x1, y1] lista de coordenadas
    [[x1, y1]...] de los puntos sin datos
    xyd: array 2D de las coordenadas de los puntos con dato
    z: array 1D con los valores de la variable en cada xyd
    """
    xyva = np.array(xyv, dtype=np.float64)
    tree = spatial.cKDTree(xyd)
    dist, ii = tree.query(xyva, k=xyva.shape[0])
    iqp = quadrants(xyva, xyd)
    selected_dist, selected_z = select_points_2_idw(dist, ii, z, iqp)
    values = idw(selected_dist, selected_z, par.POWER, par.DIST_MIN)
    write_2_file(fo, codv, fecha, values)


def quadrants(xyv, xyd):
    """calcula la situación de cada xyd en un sistema de coordenadas
       cartesiano centrado en cada elemento de xyv
       devuelve un array entero [N, M], siendo N = xyv.shape[0] y
       M = xyd.shape[0]
    """
    iqp = []
    for xyv1 in xyv:
        xt = xyd[:, 0] - xyv1[0]
        yt = xyd[:, 1] - xyv1[1]
        iq = get_quadrant(xt, yt)
        iqp.append(iq)
    return np.array(iqp, dtype=np.int32)


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


def select_points_2_idw(dist, ii, z, iqp):
    """
    para cada punto sin dato de coordenadas xyv1 selecciona los 4 puntos más
    próximos en cada cuadrante
    """
    selected_dist = []
    selected_z = []
    for i in range(dist.shape[0]):
        iq = np.zeros((4), dtype=np.int32)
        s1_dist = []
        s1_z = []
        for j in range(dist.shape[1]):
            n = iqp[i, j] - 1
            if iq[n] == 0:
                iq[n] = 1
                s1_dist.append(dist[i, j])
                m = ii[i, j]
                s1_z.append(z[m])
                if iq.sum() == 0:
                    selected_dist.append(np.array(s1_dist, np.float32))
                    selected_z.append(np.array(s1_z, np.float32))
                    break
            selected_dist.append(np.array(s1_dist, np.float32))
            selected_z.append(np.array(s1_z, np.float32))

    return selected_dist, selected_z


def idw(d, z, power, dist_min):
    """
    d list each element type array 1D. It have lengths from point
      without value to points with data
    z equal type that d, fill with the values of the variable to
      interpolate
    power used set array w
    dist_min a minimum distance. If d[i][0] <= dist_min
      interpolated value = z[i][0]
    """
    if len(d) != len(z):
        raise ValueError('d and z have different elements number')
    values = np.empty([len(d)], dtype=np.float32)
    for i in range(len(d)):
        if d[i][0] <= dist_min:
            values[i] = z[i][0]
            continue
        w = 1./np.power(d[i], power)
        values[i] = np.sum(w * z[i])/np.sum(w)
    return values


def write_2_file(fo, codv, fecha, values):
    """
    print codv, values to file
    """
    for i in range(len(codv)):
        fo.write('{0}\t{1}\t{2:.0f}\n'.format(codv[i],
                 fecha.strftime('%d/%m/%Y'), values[i]))
