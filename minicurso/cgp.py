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
    return np.sum(i_out!=np.array(t_out))

def count_dist(individual, table):
    dist = 0
##    for inp,outp in table:
##        i_out = individual.eval(inp)
    evals = map(individual.eval,[i[0] for i in table])
    dist = np.sum(list(map(compare_out,evals,[i[1] for i in table])))
    return dist
    #pass
        

def design(individual, table, budget, lbd = 4):
    parent = individual
    b_dist = count_dist(parent, table)
    while b_dist > 0 and budget > 0:
        pop = [individual.copy() for i in range(lbd)]
        [i.mutate_sam() for i in pop]
        dist = [count_dist(i,table) for i in pop]
        if np.min(dist) <= b_dist:
            b_dist = np.min(dist)
            parent = pop[dist.index(np.min(dist))]
        budget-=1
    return parent.copy(),b_dist

table_xor = [
    [[0,0],[0]],
    [[0,1],[1]],
    [[1,0],[1]],
    [[1,1],[0]]]

A = individual(2,1,1,25,12,3)
B,erro = design(A, table_xor, 10000)
        
        
        
    
