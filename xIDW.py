# -*- coding: Latin-1 -*-
"""
Created on Sun Mar 25 14:23:56 2018

@author: solis
"""

import traceback
import logging

if __name__ == "__main__":

    try:
        from IDW import fill_voids_idw_quadrants

        fill_voids_idw_quadrants()

        print('proceso terminado', end=' ')
    except Exception as e:
        logging.error(traceback.format_exc())
    finally:
        print('fin')
