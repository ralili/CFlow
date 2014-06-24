import numpy as np
from scipy.optimize import leastsq

class MPC:
    """ """
    def __init__(self):
        """ """
        self.A=np.matrix('0.9643 -0.00631; 6.947 0.4472')
        self.B=np.matrix('9.874;39.31')
        self.C=np.matrix('-0.006362 0.001674')
        self.R=1.
        self.Q=np.asmatrix(np.identity(len(self.A)))*100
        self.P=np.asmatrix(np.empty(shape=(len(self.A),len(self.A))))
        self.y=0.
        self.x=np.matrix('0;0')
        self.u=0.
    def kalmanFilter(self,u,y0):
        """ """
        xm=(self.A*self.x+self.B*u)
        Pm=(self.A*self.P*self.A.T+self.Q)
        ym=y0-self.C*xm
        L=Pm*self.C.T/(self.C*Pm*self.C.T+self.R)
        self.x=xm+L*ym;
        self.y=self.C*self.x;
        self.P=(np.asmatrix(np.identity(len(self.x)))-L*self.C)*Pm
    def prediction(self,reference):
        """ """
        u=1/float(self.C*self.B)*float(reference-self.C*self.A*self.x)
        if u<0:
            u=0
        elif u>1:
            u=1
        return u
    def cost(self,input,reference,weights=np.array([1.,1.,1.])):
        predicted_output=np.array([0.]*len(weights))
        hiddenStates=self.x
        for i in range(len(weights)):
            predicted_output[i]=self.C*(self.B*input[i]+self.A*hiddenStates)
            hiddenStates=self.B*input[i]+self.A*hiddenStates
#        if any(abs(input)>1):
#            return 1e10
#        else:
        return abs((predicted_output-reference)*weights)
    def multiPrediction(self,reference):
        return leastsq(self.cost,np.array([0.,0.,0.]),(reference))[0]

