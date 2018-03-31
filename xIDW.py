# -*- coding: Latin-1 -*-
"""
Created on Sun Mar 25 14:23:56 2018

@author: solis
"""

import traceback
import logging

if __name__ == "__main__":

    try:
        from IDW import rellenar_huecos

        rellenar_huecos()

        print('fin ok', end=' ')
    except Exception as e:
        logging.error(traceback.format_exc())
    finally:
        print('fin')
