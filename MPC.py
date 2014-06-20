import numpy as np
from scipy.optimize import leastsq

class MPC:
    """ """
    def __init__(self):
        """ """
        self.A=np.matrix('0.9643 -0.00631; 6.947 0.4472')
        self.B=np.matrix('9.874;39.31')
        self.C=np.matrix('-0.006362 0.001674')
        self.R=1
        self.Q=np.asmatrix(np.identity(len(A)))*100
        self.P=np.asmatrix(np.empty(shape=(len(A),len(A))))
		self.y=0
		self.x=np.matrix('0;0')
		self.u=0

    def kalmanFilter(self,u,y0=self.y,x0=self.x,A=self.A,B=self.B,C=self.C,Q=self.Q,R=self.R,P0=self.P):
        """ """
        xm=(A*x0+B*u)
        Pm=(A*P0*A.T+Q)
        ym=y0-C*xm
        L=Pm*C.T/(C*Pm*C.T+R)
        x=xm+L*ym;
        y=C*x;
        P=(np.asmatrix(np.identity(len(x0)))-L*C)*Pm
        return [x,y,P]

    def prediction(self,reference,x=self.x,A=self.A,B=self.B,C=self.C):
        """ """
        u=1/float(C*B)*float(reference-C*A*x)
        if u<0:
            u=0
        elif u>1:
            u=1
        return u