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
            import IDW_parameters as par
            from IDW import fill_voids_idw_quadrants

            print('IDW: Interpolate voids in a temporal serie')
            fill_voids_idw_quadrants()

        elif OPTION == 2:
            import IDW_SCATTER_parameters as par
            from IDW import fill_scatter_idw_quadrants

            print('IDW: Interpolate scatter points')
            fill_scatter_idw_quadrants()

        print('The script took {0} seconds'.format(time.time()-startTime))
        print('Results in {}'.format(par.DIR_OUT))
    except Exception as e:
        logging.error(traceback.format_exc())
    finally:
        print('fin')
