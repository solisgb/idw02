# -*- coding: Latin-1 -*-
"""
Created on Sun Mar 25 14:23:56 2018

@author: solis

El script realiza una interpolación por el método IDW, bien en una series de
    datos con huecos (1), bien en una series de puntos suministrada por el
    usuario (2)
"""
import traceback
import logging

OPTION = 2

if __name__ == "__main__":

    try:
        import time
        startTime = time.time()
        if OPTION == 1:
            from IDW_parameters import DIR_OUT
            from IDW import fill_voids_idw_quadrants

            print('IDW: Interpolate voids in a temporal serie')
            fill_voids_idw_quadrants()

        elif OPTION == 2:
            from IDW_SCATTER_parameters import DIR_OUT
            from IDW import fill_scatter_idw_quadrants

            print('IDW: Interpolate scatter points')
            fill_scatter_idw_quadrants()

        xtime = time.time()-startTime
        if xtime < 60.0:
            units = 'seconds'
        else:
            units = 'minutes'
            xtime = xtime / 60.0
        print('The script took {0} {1}'.format(xtime, units))
        print('Results in {}'.format(DIR_OUT))
    except Exception as e:
        logging.error(traceback.format_exc())
    finally:
        print('fin')
