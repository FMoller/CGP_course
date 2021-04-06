"""
Cartesian Genetic Programming Classes
"""

__version__ = "1.0"
__author__ = "Frederico Moeller"
__copyright__ = "Copyright 2021, Frederico Moeller"
__license__ = "MIT"

import numpy as np

class node():
    """ A cgp node """

    def __init__(self, pos, levels_back, lines, n_gates, inputs):

        self.values = (list(range(max(0,pos-levels_back),pos)) +
                       list(range(-inputs,0)))
        
        self.gate = np.random.randint(n_gates)
        self.i_add = ([np.random.randint(lines),
                       self.values[np.random.randint(len(self.values))]],
                      [np.random.randint(lines),
                       self.values[np.random.randint(len(self.values))]],)
        self.active = False
        self.output = -1

    def get_node(self):
        """ print the node"""
        return "{"+str(self.i_add)+" , "+str(self.gate)+"}"

class individual():
    """ A cgp individual """

    def __init__(self, inputs, outputs, lines, cols, levels_back, n_gates):

        self.nodes = []
        for i in range(lines):
            self.nodes.append([])
            for j in range(cols):
                self.nodes[i].append(node(j, levels_back, lines, n_gates, inputs))
        self.cols = cols
        self.lines = lines

    def print(self):
        """ print the individual"""
        for j in range(self.cols):
            expr = "col "+str(j)+": "
            for i in range(self.lines):
                expr += self.nodes[i][j].get_node()+"\t"
            print(expr)
            
        
    

        
        
                       
    
