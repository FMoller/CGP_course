"""
Cartesian Genetic Programming Classes
"""

__version__ = "1.0"
__author__ = "Frederico Moeller"
__copyright__ = "Copyright 2021, Frederico Moeller"
__license__ = "MIT"

import numpy as np

def And(a,b):
    return int(a and b)
def Or(a,b):
    return int(a or b)
def Not(a,b):
    return int(not a)
def Xor(a,b):
    return int((a or b) and not(a and b))
def Nand(a,b):
    return int(not(a and b))
def Nor(a,b):
    return int(not(a or b))
def Nxor(a,b):
    return int(not Xor(a,b))

gate_map = {0:Not,1:And,2:Or,3:Xor,4:Nand,5:Nor,6:Nxor}

class node():
    """ A cgp node """

    def __init__(self, pos, levels_back, lines, n_gates, inputs):
        self.pos = pos
        self.levels_back = levels_back
        self.lines = lines
        self.n_gates = n_gates
        self.inputs = inputs

        self.values = (list(range(max(0,pos-levels_back),pos)) +
                       list(range(-inputs,0)))
        
        self.gate = np.random.randint(n_gates)
        self.i_add = [[np.random.randint(lines),
                       self.values[np.random.randint(len(self.values))]],
                      [np.random.randint(lines),
                       self.values[np.random.randint(len(self.values))]],]
        self.active = False
        self.output = -1

    def get_node(self):
        """ print the node"""
        return "{"+str(self.i_add)+" , "+str(self.gate)+"}"

    def set_inactive(self):
        """ sets the node as inactive"""
        self.active = False
        self.outpur = -1

    def copy(self):
        """ make a copy of itself"""
        new = node(self.pos, self.levels_back, self.lines, self.n_gates, self.inputs)
        new.gate = self.gate
        new.i_add = [self.i_add[0].copy(),self.i_add[1].copy()]
        new.active = self.active
        return new

    def eval(self, a,b):
        """ Eval node inputs"""
        self.output = gate_map[self.gate](a,b)

    def mutate(self):
        """ Mutate the node"""
        element = np.random.randint(3)
        if element != 2:
            self.i_add[element] = [np.random.randint(self.lines),
                       self.values[np.random.randint(len(self.values))]]
        else:
            self.gate = np.random.randint(self.n_gates)
                             
        


class individual():
    """ A cgp individual """

    def __init__(self, inputs, outputs, lines, cols, levels_back, n_gates):

        self.inputs = inputs
        self.outputs = outputs
        self.lines = lines
        self.cols = cols
        self.levels_back = levels_back
        self.n_gates = n_gates
        
        self.values = (list(range(max(0,cols-levels_back),cols)) +
                       list(range(-inputs,0)))
        self.nodes = []
        for i in range(lines):
            self.nodes.append([])
            for j in range(cols):
                self.nodes[i].append(node(j, levels_back, lines, n_gates, inputs))
        self.o_add = []
        for i in range(outputs):
            self.o_add.append([np.random.randint(lines),
                               self.values[np.random.randint(len(self.values))]])
        self.mapped = False
            

    def print(self):
        """ print the individual"""
        for j in range(self.cols):
            expr = "col "+str(j)+": "
            for i in range(self.lines):
                expr += self.nodes[i][j].get_node()+"\t"
            print(expr)
            
    def print_active(self):
        """ print the individual"""
        for j in range(self.cols):
            flag = False
            expr = "col "+str(j)+": "
            for i in range(self.lines):
                if self.nodes[i][j].active:
                    expr += self.nodes[i][j].get_node()+"\t"
                    flag = True
                else:
                    expr += ' - '+"\t"
            if flag:
                print(expr)
            
    def print_outputs(self):
        """ print the outputs of the nodes"""
        for j in range(self.cols):
            expr = "col "+str(j)+": "
            for i in range(self.lines):
                expr += str(self.nodes[i][j].output)+"\t"
            print(expr)

    def set_all_inactive(self):
        """ set all nodes inactive"""
        for j in self.nodes:
            [i.set_inactive() for i in j]
        self.mapped = False

    def copy(self):
        """ make a copy of itself"""
        new = individual(self.inputs, self.outputs, self.lines, self.cols, self.levels_back, self.n_gates)
        new.nodes = []
        for i in range(self.lines):
            new.nodes.append([j.copy() for j in self.nodes[i]])
        
        new.o_add = [j.copy() for j in self.o_add]
        return new

    def eval(self, line_input):
        """ Evaluate an truth table input"""
        for j in range(self.cols):
            for i in range(self.lines):
                if self.nodes[i][j].i_add[0][1]<0:
                    i_a = line_input[abs(self.nodes[i][j].i_add[0][1])-1]
                else:
                    i_a = self.nodes[self.nodes[i][j].i_add[0][0]][self.nodes[i][j].i_add[0][1]].output
                if self.nodes[i][j].i_add[1][1]<0:
                    i_b = line_input[abs(self.nodes[i][j].i_add[1][1])-1]
                else:
                    i_b = self.nodes[self.nodes[i][j].i_add[1][0]][self.nodes[i][j].i_add[1][1]].output
                if i_a not in [0,1] or i_b not in [0,1]:
                    print("Something wrong is not right")
                self.nodes[i][j].eval(i_a,i_b)
        line_output = []
        for i in self.o_add:
            if i[1] < 0:
                line_output.append(line_input[abs(i[1])-1])
            else:
                line_output.append(self.nodes[i[0]][i[1]].output)
            
        #print(line_output)
        return np.array(line_output)
        
    def map_active(self):
        """ map active nodes"""
        to_visit = []
        for i in self.o_add:
            to_visit.append(i)
        while len(to_visit)>0:
            if to_visit[0][1] < 0:
                to_visit.remove(to_visit[0])
            else:
                if self.nodes[to_visit[0][0]][to_visit[0][1]].active:
                    to_visit.remove(to_visit[0])
                else:
                    self.nodes[to_visit[0][0]][to_visit[0][1]].active = True
                    to_visit.append(
                        self.nodes[to_visit[0][0]][to_visit[0][1]].i_add[0]
                        )
                    to_visit.append(
                        self.nodes[to_visit[0][0]][to_visit[0][1]].i_add[1]
                        )
                    to_visit.remove(to_visit[0])
        self.mapped = True

    def mutate_output(self):
        """ mutate one output"""
        target = np.random.randint(self.o_add)
        self.o_add[target] = [np.random.randint(lines),
                              self.values[np.random.randint(len(self.values))]]
        
    def mutate_sam(self):
        """ mutate nodes once an active node or output is mutated"""
        if not self.mapped:
            self.map_active()
        target = np.random.randint(
            len(self.o_add)+self.lines*self.cols)

        if target < len(self.o_add):
            self.mutate_output()
        else:
            active_mut = False
            while not active_mut:
                i = np.random.randint(self.lines)
                j = np.random.randint(self.cols)
                active_mut = self.nodes[i][j].active
                self.nodes[i][j].mutate()
            print(i,j)
        self.set_all_inactive()
                
                

                    
                    
                
            
        
            
        
    

        
        
                       
    
