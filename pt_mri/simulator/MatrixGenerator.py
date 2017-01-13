'''
Created on 13 dec. 2016

@author: shenrot
'''
import numpy as np
import math

class MatrixGenerator(object):
    '''
    This class contains several objects used for the simulation of the MR on the magnetization vector of the matter
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
    def getT2Matrix(self, t, T2):
        factorT2=np.exp(-t/T2)
        return np.array([[factorT2, 0, 0], [0, factorT2, 0], [0, 0, 1]])
    
    def getT1Matrix(self,t, T1):
        factorT1=np.exp(-t/T1)
        return [np.array([[1, 0, 0], [0, 1, 0], [0, 0, factorT1]]),np.array([0,0,1-factorT1])]
    
    def getT1T2Matrix(self, t, T1, T2):
        factorT1=np.exp(-t/T1)
        factorT2=np.exp(-t/T2)
        return [np.array([[factorT2, 0, 0],[0, factorT2, 0],[0, 0, factorT1]]),np.array([0,0,(1-factorT1)])]
    
    def getZRotationMatrix(self,phi):
        return np.array([[math.cos(phi), -math.sin(phi), 0],[math.sin(phi), math.cos(phi), 0],[0,0,1]])

    def getXRotationMatrix(self,phi):
        return np.array([[1, 0, 0],[0, math.cos(phi), -math.sin(phi)],[0,math.sin(phi),math.cos(phi)]])

    def getYRotationMatrix(self,phi):
        return np.array([[math.cos(phi), 0, math.sin(phi)],[0, 1, 0],[-math.sin(phi),0,math.cos(phi)]])

    def getThetaRotationMatrix(self,phi, theta):
        return self.getZRotationMatrix(theta).dot(self.getXRotationMatrix(phi).dot(self.getZRotationMatrix(-theta)))
    
    def getFreePrecessMatrix(self,t,T1,T2,df):
        [A,B]=self.getT1T2Matrix(t,T1,T2)
        return [self.getZRotationMatrix(2*math.pi*df*t/1000).dot(A),B]