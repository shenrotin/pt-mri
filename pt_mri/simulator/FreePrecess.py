'''
Created on 13 dec. 2016

@author: shenrot
'''
from pt_mri.simulator.SequenceItem import SequenceItem
from pt_mri.simulator.MatrixGenerator import MatrixGenerator

class FreePrecess(SequenceItem):
    '''
    classdocs
    '''

    def __init__(self,relaxation_time, T1, T2, df):
        '''
        Constructor
        '''
        [self.matrix_A, self.matrix_B]=MatrixGenerator().getFreePrecessMatrix(relaxation_time, T1, T2, df)
    
    def run(self,magnetisation):    
        super()
        return self.matrix_A.dot(magnetisation)+self.matrix_B
    