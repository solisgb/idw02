# -*- coding: Latin-1 -*-
"""
Created on Sun Mar 18 12:53:24 2018
@author: solis

DRIVERS
Primero hay que instalar los drivers corrspondientes a la DB que se quiere
utilizar
1.- Para access y otros https://github.com/mkleehammer/pyodbc/wiki
2.- Para sqlite http://www.ch-werner.de/sqliteodbc/
"""


def conexion_str_get(dbname):
    from os.path import exists, splitext

    if not exists(dbname):
        raise ValueError('no existe\n{}'.format(dbname))

    ext = splitext(dbname)[1]

    if ext == '.mdb' or ext == '.accdb':
        a = 'DBQ={0};'.format(dbname)
        conn_str = (r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)}; ' + a)
    elif ext == '.db':
        a = 'DATABASE={0};'.format(dbname)
        conn_str = "DRIVER={SQLite3 ODBC Driver};SERVER=localhost;{0}Trusted_connection=yes".format(a)
    else:
        raise ValueError('Cadena de conexión no implementada: {}'.format(ext))
    return conn_str
