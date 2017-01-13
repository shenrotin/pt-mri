'''
Created on 14 dec. 2016

@author: shenrot
'''
from pt_mri.simulator.MatrixGenerator import MatrixGenerator
import math
import numpy as np
import numpy.linalg as la
import cmath

class SteadyState(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.matrix_generator=MatrixGenerator()
        
    #Steady state for a simple excitation (angle is a parameter). Result: M at echo time    
    def sssignal(self,flip_angle,T1,T2,TE,TR,df):
        [Ate,Bte]=self.matrix_generator.getFreePrecessMatrix(TE,T1,T2,df)
        [Atr,Btr]=self.matrix_generator.getFreePrecessMatrix(TR-TE,T1,T2,df)
        R=self.matrix_generator.getYRotationMatrix(flip_angle)
        I=np.eye(3,3)
        Mss=la.inv(I-Ate.dot(R.dot(Atr))).dot(Ate.dot(R.dot(Btr))+Bte)
        return [Mss,Mss[0]+1j*Mss[1]]

    #Steady state for a simple excitation (angle is a parameter), (transverse component after TR neglected). Result: M at echo time
    def srsignal(self,flip_angle,T1,T2,TE,TR,df):
        [Ate,Bte]=self.matrix_generator.getFreePrecessMatrix(TE,T1,T2,df)
        [Atr,Btr]=self.matrix_generator.getFreePrecessMatrix(TR-TE,T1,T2,df)
        
        #Here is the trick. We multiply Atr to get completely rid of the transverse component after relaxation
        Atr=np.array([[0,0,0],[0,0,0],[0,0,1]]).dot(Atr)
        
        R=self.matrix_generator.getYRotationMatrix(flip_angle)
        I=np.eye(3,3)
        Mss=la.inv(I-Ate.dot(R.dot(Atr))).dot(Ate.dot(R.dot(Btr))+Bte)
        return [Mss,Mss[0]+1j*Mss[1]]

    #Steady state for a simple spin echo (transverse component after TR neglected). Result: M at echo time
    def sesignal(self,T1,T2,TE,TR,df):
        [Ate2,Bte2]=self.matrix_generator.getFreePrecessMatrix(TE/2,T1,T2,df)
        [Atr,Btr]=self.matrix_generator.getFreePrecessMatrix(TR-TE,T1,T2,df)
        
        #Here is the trick. We multiply Atr to get completely rid of the transverse component after relaxation
        Atr=np.array([[0,0,0],[0,0,0],[0,0,1]]).dot(Atr)
        
        R90=self.matrix_generator.getYRotationMatrix(math.pi/2)
        R180=self.matrix_generator.getXRotationMatrix(math.pi)
        
        I=np.eye(3,3)
        Mss=la.inv(I-Ate2.dot(R180.dot(Ate2.dot(R90.dot(Atr))))).dot(Bte2+Ate2.dot(R180.dot(Bte2))+Ate2.dot(R180.dot(Ate2.dot(R90.dot(Btr)))))
        return [Mss,Mss[0]+1j*Mss[1]]
    
    #Steady state for a Fast Spin Echo or Turbo Spin Echo(transverse component after TR neglected). ETL is the number of 180 echos.
    #Result: The steady state just after the excitation + M at each echo time
    def fsesignal(self,T1,T2,TE,TR,ETL,df):
        [Ate2,Bte2]=self.matrix_generator.getFreePrecessMatrix(TE/2,T1,T2,df)
        [Atr,Btr]=self.matrix_generator.getFreePrecessMatrix(TR-ETL*TE,T1,T2,df)
        
        #Here is the trick. We multiply Atr to get completely rid of the transverse component after relaxation
        Atr=np.array([[0,0,0],[0,0,0],[0,0,1]]).dot(Atr)
        
        R90=self.matrix_generator.getYRotationMatrix(math.pi/2)
        R180=self.matrix_generator.getXRotationMatrix(math.pi)
        
        #Recurrence formula to determine Aetl et Betl
        A=np.eye(3)
        B=np.array([0,0,0])
        for i in range(ETL):
            A=Ate2.dot(R180.dot(Ate2.dot(A)))
            B=Ate2.dot(R180.dot(Bte2))+Bte2+Ate2.dot(R180.dot(Ate2.dot(B)))
        
        I=np.eye(3,3)
        M=la.inv(I-R90.dot(Atr.dot(A))).dot(R90.dot(Atr.dot(B))+R90.dot(Btr))
        result=[M]
        
        #We start from the steady state and calculate M for each echo
        for i in range(ETL):
            M=Ate2.dot(R180.dot(Ate2.dot(M)+Bte2))+Bte2
            result.append(M)
        
        return np.asarray(result)
    
    def gssignal(self,flip_angle,T1,T2,TE,TR,df, phi):
        [Ate,Bte]=self.matrix_generator.getFreePrecessMatrix(TE,T1,T2,df)
        [Atr,Btr]=self.matrix_generator.getFreePrecessMatrix(TR-TE,T1,T2,df)
        
        #Here is the difference, we rotate around z with and angle phi at the end of the relaxation
        Atr=self.matrix_generator.getZRotationMatrix(phi).dot(Atr)
        
        R=self.matrix_generator.getYRotationMatrix(flip_angle)
        I=np.eye(3,3)
        Mss=la.inv(I-Ate.dot(R.dot(Atr))).dot(Ate.dot(R.dot(Btr))+Bte)
        return [Mss,Mss[0]+1j*Mss[1]]
    
    # B-3-b. We use a different phi for 100 different magnetisations + average
    def gresignal(self,flip,T1,T2,TE,TR,dfreq=0):
        result=np.zeros(3)
        phis=np.arange(1,101,1)
        phis=(phis/100-0.5)*4*math.pi
        for phi in phis:
            [M,Mtranverse]=self.gssignal(flip,T1,T2,TE,TR,dfreq,phi)
            result=result+M
        
        result=result/100
        return [result,result[0]+1j*result[1]]

    def spgrsignal(self,flip,T1,T2,TE,TR,df=0,nb_excitations=100,inc=117.0/180.0*math.pi):
        nb_magnetisations=100
        increment=inc
    
        phi=0 #Angle of the axis for the excitation
        spoil_angles=np.arange(1,nb_magnetisations+1,1)/nb_magnetisations*2*math.pi
    
        M=np.zeros((nb_magnetisations,3))
        M[:,0]=1
        
        [Ate,Bte]=self.matrix_generator.getFreePrecessMatrix(TE,T1,T2,df)
        [Atr,Btr]=self.matrix_generator.getFreePrecessMatrix(TR-TE,T1,T2,df)
    
        #We have a list of magnetisation vector. Each vector will be rotated by a certain angle spoil_angle after each cycle.
    
        for i in range(nb_excitations):
            #RF excitation
            Rflip=MatrixGenerator().getThetaRotationMatrix(flip,phi)
            A=Ate.dot(Rflip)
    
            #We wait until echo time
            for j in range(nb_magnetisations):
                M[j]=A.dot(M[j])+Bte
    
            Maverage=np.zeros(3)
            for j in range(nb_magnetisations):
                Maverage=Maverage+M[j]
    
            Maverage=Maverage/nb_magnetisations
    
            last_magnetisation=Maverage
            last_signal=(Maverage[0]+1j*Maverage[1])*np.exp(-(1j*phi))
    
            #Relaxation until new excitation
            for j in range(nb_magnetisations):
                M[j]=Atr.dot(M[j])+Btr
    
            #Spoil effect
            for j in range(nb_magnetisations):
                M[j]=MatrixGenerator().getZRotationMatrix(spoil_angles[j]).dot(M[j])
    
            phi=phi+increment
            increment=increment+inc
    
        return [last_magnetisation,last_signal]
    
    #This function consider a simple SSFP (Gradient echo without gradient-spoil neither rf-spoil). To show the impact of error in the df, we simulate 500 spins at different 
    #frequencies chose in a uniform distribution centered on "frequency"+/- deltaf. The sum of the transverse signal is made.
    def ssfpavsignal(self,flip,T1,T2,TE,TR,frequency,deltaf):
        n=500
        dfs=np.random.uniform(frequency-deltaf,frequency+deltaf, size=n)
        M_sum=0
        M_sig_sum=0        
        for i in range(len(dfs)):
            [M,M_sig]=self.sssignal(flip,T1,T2,TE,TR,dfs[i])
            M_sig_sum=M_sig_sum+M_sig
            M_sum=M_sum+M
        
        M_sig_sum=M_sig_sum/n
        M_sum=M_sum/n
        return [M_sum,M_sig_sum]