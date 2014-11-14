import random,math
import numpy as np
from scipy import linalg

class particleFilter:
    """ """
    def __init__(self,frequency,numParticles,numSamples):
        """ """
        self.A_cont=np.matrix('-0.1333,0,0;0.0333,-0.0333,0;0,0.0217,-0.0217')
        self.B_cont=np.matrix('0.1333,0.1348;0,0;0,0')
        self.A=linalg.expm(self.A_cont*frequency)
        self.B=linalg.inv(self.A_cont)*((self.A-np.asmatrix(np.identity(len(self.A)))))*(self.B_cont)
        self.C=np.matrix('0,0,1')
        
        self.numSamples=numSamples
        
        self.inputsApplied=[]
        self.measurements=[]
        self.sigmaMeasurements=0.05#measurement noise
        self.sigmaProcess=0.1#process noise
        
        self.frequency=frequency
        self.numParticles=numParticles
        self.parameters=np.matrix('-0.0956;-0.0214;0.0116;0.0965')
        self.parameterVariance=np.divide(abs(self.parameters),np.matrix('3;3;3;3'))
        self.relativeParameterVariance=0.5
        self.particles=[np.asmatrix(np.ones((7,self.numParticles))) for i in range(self.numSamples)]
        self.particles[0][3:7,:]=(np.asmatrix(np.tile(self.parameters,(1,self.numParticles))).T+np.random.random((self.numParticles,4))*np.asmatrix(np.identity(4)*np.asarray(self.parameterVariance))).T
        self.MPChorizon=3
        self.bnds = ((0, 4.4385),)*self.MPChorizon
        self.initialOptimizedInput=2*np.array([1.,1.,1.,1.,1.])   
    def cost(self,X0,P0,u,Yset):        
        Yset = np.ones((self.numParticles,1))*Yset      
        xpred = self.predictiveDistribution(u,X0,P0);
        ypred=np.asmatrix(np.zeros(Yset.shape))
        for i in range(self.numParticles):
            ypred[i,:] = xpred[i][2,:]
        error=Yset-ypred#Get difference between prediction and reference
        np.multiply(error,error)#square such difference
        S=np.multiply(b,b).sum(axis=1)#sum up the difference across the whole trajectory, for each particle.
        s10 = np.percentile(S,10)
        s90 = np.percentile(S,90)
        S=S[np.nonzero(S-s10)]
        S=S[np.nonzero(s90-S)]
        return np.mean(S)
    def predictiveDistribution(self,u,X0,P0):
        horizon=len(u)+1        
        pars_cont = P0;
        xpred=[np.asmatrix(np.zeros((3,horizon))) for i in range(self.numParticles)]
        xpred[0] = X0[0:3,:]####Look at its dimensions
        for p in range(self.numParticles):
            xpred_p = np.asmatrix(np.zeros((3,horizon)))
            xpred_p[:,1] = X0[0:3,p]####Look at its dimensions
            A_cont=np.matrix([[pars_cont[0,p],0,0],[-pars_cont[1,p]+pars_cont[2,p],pars_cont[1,p]-pars_cont[2,p],0],[0,-pars_cont[1,p],pars_cont[1,p]]])
            A=linalg.expm(A_cont*self.frequency)
            B_cont=np.matrix([[-pars_cont[0,p],pars_cont[3,p]],[0,0],[0,0]])
            B=linalg.inv(A_cont)*((A-np.asmatrix(np.identity(len(A)))))*(B_cont)
            for h in range(1,1+len(u)):
                xpred_p[:,h]=A*np.asmatrix(xpred_p[:,h-1])+B*np.matrix([[1],[u[h-1]]])
            xpred[p]= xpred_p
        return xpred
    def optimizationLoop(self):
        optimalInput=minimize(self.cost,self.initialOptimizedInput,args=(reference,),method='SLSQP',bounds=self.bnds).x
        self.initialOptimizedInput=optimalInput
        self.inputsApplied.append(optimalInput[0])#####    
    def bootstrapFilter(self):
        x=[0]*self.numSamples#particles
        w=np.zeros((self.numSamples,self.numParticles))#incremental weights. ITS FIRST ROW IS ALL ZEROES!
        W=np.zeros((self.numSamples,self.numParticles))#normalized weights. ITS FIRST ROW IS ALL ZEROES!
        x[0]=self.particles[0]
        
        for i in range(1,self.numSamples):######
            pars_cont = x[i-1][3:7,:]
            xcurr=x[i-1][0:3,:]
            xnext=np.zeros(xcurr.shape)
            for p in range(self.numParticles):
                A_cont=np.matrix([[pars_cont[0,p],0,0],[-pars_cont[1,p]+pars_cont[2,p],pars_cont[1,p]-pars_cont[2,p],0],[0,-pars_cont[1,p],pars_cont[1,p]]])
                A=linalg.expm(A_cont*self.frequency)
                B_cont=np.matrix([[-pars_cont[0,p],pars_cont[3,p]],[0,0],[0,0]])
                B=linalg.inv(A_cont)*((A-np.asmatrix(np.identity(len(A)))))*(B_cont)
                xnext[:,h]=A*xcurr[:,p]+B*np.matrix([[1],[u[h-1]]])+np.asmatrix(self.sigmaProcess*np.random.randn(3)).T
            x[i][0:3,:]=xnext
            ypred=self.C*x[i][0:3,:]
            w[i]=self.normpdf(Ymeas(i),ypred,sigma_meas)
            W[i]=w[i]/np.sum(w[i])
            
            resamplingWeights=np.cumsum(W[i])
            resamplingIndex=[]
            for j in range(self.numParticles):
                rnd=np.random.rand(1)
                if resamplingWeights[j]-rnd>0:
                    resamplingIndex.append(j)
            x[n]=x[n][:,resamplingIndex]
            x[n][3:5]=-abs(x[n-1][3:7,:]+self.relativeParameterVariance*np.asmatrix(np.identity(4)*np.asarray(self.parameterVariance))*np.asmatrix(np.random.randn(4,self.numParticles)))##sign
            x[n][5:7]=abs(x[n-1][3:7,:]+self.relativeParameterVariance*np.asmatrix(np.identity(4)*np.asarray(self.parameterVariance))*np.asmatrix(np.random.randn(4,self.numParticles)))##sign
        Xest=x[self.numSamples][0:3,]
        Parest=x[self.numSamples-1][3:7,]
        Parnext=x[self.numSamples][3:7,]
            
    def normpdf(self,x, mean, sd):
        '''test speed of this'''
        return 1/(sd*(2*math.pi)**0.5)*np.exp(-(np.asarray(x)-np.asarray(mean))**2/(2*sd**2))
        
 
            
        #self.particles[i][0:3,:]##BOOTSTRAP
        #self.particles[i][3:7,:]##BOOTSTRAP
        #self.particles[i-1][3:7,:]##BOOTSTRAP