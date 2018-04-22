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
    NUM = 100

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
    for i, row in enumerate(cur):
        if fecha == row.FECHA:
            codv.append(row.ID)
            xyv.append([row.X, row.Y])
        else:
            xyd, z = select_data(con, fecha)
            if len(z) != 0:
                fill_fecha(fo, fecha, codv, xyv, xyd, z)
                if fmod(i, NUM) == 0.0:
                    print('{}'.format(fecha.strftime('%d/%m/%Y')))
            else:
                a = 'El {} no hay datos'.format(fecha.strftime('%d/%m/%Y'))
                print(a)
                foi.write('{}\n'.format(a))
            fecha = row.FECHA
            codv = [row.ID]
            xyv = [[row.X, row.Y]]

    xyd, z = select_data(con, fecha)
    if len(z) != 0:
        fill_fecha(fo, fecha, codv, xyv, xyd, z)
        print('{}'.format(fecha.strftime('%d/%m/%Y')))
    else:
        a = 'El {} no hay datos'.format(fecha.strftime('%d/%m/%Y'))
        print(a)
        foi.write('{}\n'.format(a))

    cur.close()
    con.close()

    fo.flush()
    fo.close()
    foi.flush()
    foi.close()


def select_data(con, fecha):
    """
    argumentos
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
    xyd = np.array([[row.X, row.Y] for row in rows], dtype='float64')
    z = np.array([row.VALUE for row in rows], dtype='float64')
    cur.close()
    return xyd, z


def fill_fecha(fo, fecha, codv, xyv, xyd, z):
    """
    argumentos
    fecha: un type(date) en la que hay puntos sin datos
    codv: lista de str con los id de los puntos sin datos
    xyv: lista de coordenadas [[x1, y1]...] de los puntos sin datos en fecha
    xyd: array 2D de las coordenadas de los puntos con dato
    z: array 1D con los valores de la variable en cada xyd
    """
    xyva = np.array(xyv, dtype=np.float64)
    tree = spatial.cKDTree(xyd)
    dist, ii = tree.query(xyva, k=xyd.shape[0])
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
    Para cada punto sin dato de coordenadas xyv1 selecciona los 4 puntos más
    próximos en cada cuadrante.
    argumentos
    dist: array 2D de distancias (n, m) n número de puntos sin datos, m núm de
        puntos con datos
    ii: lista 2D (n, m) en que cada elemento es una lista al con las posiciones
        de z
    z: array 1D (m) con los valores de la variable en cada punto con datos
    iqp: array 2D (n, m) con el cuadrante de cada punto con datos respecto a
        cada punto sin datos
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
    Calcula el valor en cada punto sin datos
    d array 2D (n, m) distancias del punto sin datos a los puntos con datos
    z array 2D (n, m) valores de la variable en cada d
    power: potencia
    dist_min distncia mínima. Si d[i][0] <= dist_min
      el valor interpolado es igual a z[i][0]
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


def rango_fechas(start, stop, step = 1):
    """
    generador de fechas entre start y stop con un paso de tiempo de un día
    """
    from datetime import datetime, timedelta
    start = datetime.strptime(start, '%d/%m/%Y')
    stop = datetime.strptime(stop, '%d/%m/%Y')

    if stop <= start:
        raise ValueError("start must be smaller than stop")

    step = timedelta(days = step)
    fecha = start
    while fecha < stop:
        yield fecha
        fecha += step


def fill_scatter_idw_quadrants():
    """operaciones generales para rellenado de una series de puntos
           distribuidos en el interior del espacio de un conjunto de
           puntos con datos"""
    from math import fmod
    from os.path import join
    import db_con_str
    import IDW_SCATTER_parameters as par

    FILE_INCIDENCIAS = 'idw_scatter_indicencias.txt'
    NUM = 100

    fo = open(join(par.DIR_OUT, par.F_OUT), 'w', par.BUFSIZE)
    foi = open(join(par.DIR_OUT, FILE_INCIDENCIAS), 'w', par.BUFSIZE)

    xyp = np.loadtxt(par.FILE_POINTS, delimiter='\t', usecols=[1,2],
                     dtype='float64')
    codp = np.loadtxt(par.FILE_POINTS, delimiter='\t', usecols=[0],
                     dtype='int32')
    codp = codp.tolist()

    con = pyodbc.connect(db_con_str.con_str(par.DB))

    for i, fecha in enumerate(rango_fechas(par.FECHA_INICIAL,
                                           par.FECHA_FINAL)):
        xyd, z = select_data(con, fecha)
        if z.size == 0:
            a = 'El {} no hay datos'.format(fecha.strftime('%d/%m/%Y'))
            print(a)
            foi.write('{}\n'.format(a))
            continue
        tree = spatial.cKDTree(xyd)
        dist, ii = tree.query(xyp, k=z.size)
        iqp = quadrants(xyp, xyd)
        selected_dist, selected_z = select_points_2_idw(dist, ii, z, iqp)
        values = idw(selected_dist, selected_z, par.POWER, par.DIST_MIN)
        write_2_file(fo, codp, fecha, values)
        if fmod(i, NUM) == 0.0:
            print('{}'.format(fecha.strftime('%d/%m/%Y')))

    con.close()

    fo.flush()
    fo.close()
    foi.flush()
    foi.close()
