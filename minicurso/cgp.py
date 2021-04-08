"""
Cartesian Genetic Programming 
"""

__version__ = "1.0"
__author__ = "Frederico Moeller"
__copyright__ = "Copyright 2021, Frederico Moeller"
__license__ = "MIT"

import numpy as np
from cgp_classes import *

def compare_out(i_out,t_out):
    return np.sum(i_out!=t_out)

def count_dist(individual, table):
    dist = 0
##    for inp,outp in table:
##        i_out = individual.eval(inp)
    evals = map(individual.eval,[i[0] for i in table])
    dist = np.sum(list(map(compate_out,evals,[i[1] for i in table])))
    return dist
    #pass
        

def design(individual, table, budget):
    pass
    
