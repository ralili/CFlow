import numpy as np
from scipy.optimize import minimize
from scipy import linalg
import logging

class newMPC:
    """ """
    def __init__(self,frequency):
        """ """
        self.A_cont=np.matrix('-0.1333,0,0;0.0333,-0.0333,0;0,0.0217,-0.0217')
        self.B_cont=np.matrix('0.1333,0.1348;0,0;0,0')
        self.A=linalg.expm(self.A_cont*frequency)
        self.B=linalg.inv(self.A_cont)*((self.A-np.asmatrix(np.identity(len(self.A)))))*(self.B_cont)
        self.C=np.matrix('0,0,1')
        self.R=1.#######
        self.Q=np.asmatrix(np.identity(len(self.A)))*10##########
        self.P=np.asmatrix(np.empty(shape=(len(self.A),len(self.A))))
        self.y=0.
        self.x=np.matrix('1;1;1')
        self.u=0.
        self.bnds = ((0, 4.57), (0, 4.57), (0, 4.57), (0, 4.57), (0, 4.57))#Change to incorporate number of steps
        self.sigmoidal=[6.4307,2.6491,-0.0509,-1.7622]
        self.initialGFPreading=0
    def kalmanFilter(self,u,y0):
        """ """
        xm=self.A*self.x+self.B*np.matrix([[1],[u]])
        Pm=(self.A*self.P*self.A.T+self.Q)
        ym=y0-self.C*xm
        L=Pm*self.C.T/(self.C*Pm*self.C.T+self.R)
        self.x=xm+L*ym;
        self.y=self.C*self.x;
        self.P=(np.asmatrix(np.identity(len(self.x)))-L*self.C)*Pm
        loggingState=''
        for i in range(len(self.x)):
            loggingState+=str(self.x[i])+','
        logging.info('SS hidden states are: %s',loggingState)
    def cost(self,input,reference,weights=np.array([1.,1.,1.,1.,1.])):#introduce number of steps
        predicted_output=np.array([0.]*len(weights))
        hiddenStates=self.x
        for i in range(len(weights)):
            predicted_output[i]=self.C*(self.A*hiddenStates+self.B*np.matrix([[1],[input[i]]]))
            hiddenStates=self.A*hiddenStates+self.B*np.matrix([[1],[input[i]]])
        return sum(abs((predicted_output-reference)*weights))
    def multiPrediction(self,reference):
        optimalInput=minimize(self.cost,np.array([1.,1.,1.,1.,1.]),args=(reference,),method='SLSQP',bounds=self.bnds).x[0]#introduce number of steps
        return optimalInput
    def ledOutputTransformation(self,LEDintensity):
        a=self.sigmoidal[0]
        b=self.sigmoidal[1]
        c=self.sigmoidal[2]
        d=self.sigmoidal[3]
        return np.log(a/(b*(LEDintensity-d))-1/b)/(c*100)
    def getFoldChange(self,GFPreading):
        return GFPreading/self.initialGFPreading

class MPC:
    """ """
    def __init__(self):
        """ """
        self.A=np.matrix('0.1028,-0.3208,-0.1697;0.6076,0.7442,-0.1385;0.06197,0.1414,0.9919')
        self.B=np.matrix('1.215;0.9915;0.05822')
        self.C=np.matrix('0,0,0.2151')
        self.R=1.
        self.Q=np.asmatrix(np.identity(len(self.A)))*100
        self.P=np.asmatrix(np.empty(shape=(len(self.A),len(self.A))))
        self.y=0.
        self.x=np.matrix('0;0;0')
        self.u=0.
        self.bnds = ((0, 1), (0, 1), (0, 1), (0, 1), (0, 1))#Change to incorporate number of steps
    def kalmanFilter(self,u,y0):
        """ """
        xm=(self.A*self.x+self.B*u)
        Pm=(self.A*self.P*self.A.T+self.Q)
        ym=y0-self.C*xm
        L=Pm*self.C.T/(self.C*Pm*self.C.T+self.R)
        self.x=xm+L*ym;
        self.y=self.C*self.x;
        self.P=(np.asmatrix(np.identity(len(self.x)))-L*self.C)*Pm
        loggingState=''
        for i in range(len(self.x)):
          loggingState+=str(self.x[i])+','
        logging.info('SS hidden states are: %s',loggingState)
    def prediction(self,reference):
        """ """
        u=1/float(self.C*self.B)*float(reference-self.C*self.A*self.x)
        if u<0:
            u=0
        elif u>1:
            u=1
        return u
    def cost(self,input,reference,weights=np.array([1.,1.,1.,1.,1.])):#introduce number of steps
        predicted_output=np.array([0.]*len(weights))
        hiddenStates=self.x
        for i in range(len(weights)):
            predicted_output[i]=self.C*(self.B*input[i]+self.A*hiddenStates)
            hiddenStates=self.B*input[i]+self.A*hiddenStates
        return sum(abs((predicted_output-reference)*weights))
    def multiPrediction(self,reference):
        return minimize(self.cost,np.array([1.,1.,1.,1.,1.]),args=(reference,),method='SLSQP',bounds=self.bnds).x[0]#introduce number of steps
