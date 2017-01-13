'''
Created on 13 dec. 2016

@author: shenrot
'''
from pt_mri.simulator.SequenceItem import SequenceItem
from pt_mri.simulator.MatrixGenerator import MatrixGenerator

class Flip(SequenceItem):
    '''
    classdocs
    '''
    def __init__(self, flip_angle, axis):
        self.axis=axis
        self.flip_angle=flip_angle

        if (axis=="X"):
            self.matrix=MatrixGenerator().getXRotationMatrix(flip_angle)
        
        if (axis=="Y"):
            self.matrix=MatrixGenerator().getYRotationMatrix(flip_angle)
        
        if (axis=="Z"):
            self.matrix=MatrixGenerator().getZRotationMatrix(flip_angle)
        
    def run(self, magnetisation):
        super()
        return self.matrix.dot(magnetisation)
