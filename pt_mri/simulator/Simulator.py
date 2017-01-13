'''
Created on 13 dec. 2016

@author: shenrot
'''
import numpy as np
import math
from pt_mri.simulator.Flip import Flip
from pt_mri.simulator.FreePrecess import FreePrecess

class Simulator(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.sequence=[]
    
    def addSequenceItem(self,sequence_item):
        self.sequence.append(sequence_item)
    
    def removeSequenceItem(self,sequence_item):
        self.sequence.remove(sequence_item)
    
    def run(self, magnetisation):
        result=[]
        result.append(magnetisation)
        for sequence_item in self.sequence:
            magnetisation=sequence_item.run(magnetisation)
            result.append(magnetisation)
        
        return np.asarray(result)

if __name__ == '__main__':
    simulator=Simulator()
    simulator.addSequenceItem(Flip(math.pi/3,"Y"))
    simulator.addSequenceItem(FreePrecess(500, 600, 100, 0))
    simulator.addSequenceItem(Flip(math.pi/3,"Y"))
    simulator.addSequenceItem(FreePrecess(1, 600, 100, 0))
    print(simulator.run(np.array([0,0,1])))