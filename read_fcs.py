from fcm import loadFCS
import numpy as np
import os

class read_fcs():
	def __init__(self,folder):
		

data=loadFCS('A11.fcs')#load fcs data into a list
FSC_H=[data[:,index] for index in range(len(data.channels)) if data.channels[index]=='FSC-H'][0]#extracts data of desired channel.
SSC_H=[data[:,index] for index in range(len(data.channels)) if data.channels[index]=='SSC-H'][0]#extracts data of desired channel.
FSC_A=[data[:,index] for index in range(len(data.channels)) if data.channels[index]=='FSC-A'][0]#extracts data of desired channel.
SSC_A=[data[:,index] for index in range(len(data.channels)) if data.channels[index]=='SSC-A'][0]#extracts data of desired channel.
#available channels: ['FSC-A', 'SSC-A', 'FL1-A', 'FL2-A', 'FL3-A', 'FL4-A', 'FSC-H', 'SSC-H', 'FL1-H', 'FL2-H', 'FL3-H', 'FL4-H', 'Width', 'Time']

#####Gate
#####Get FL1-A/FSC-H
#####Get median of resulting vector

############
M=np.matrix('6.3913 5.3564')
C = np.matrix('0.0392,0.0354;0.0354,0.0708')
C_inv=np.linalg.inv(C)
a=zip(np.log10(FSC_H)-M[0,0],np.log10(SSC_H)-M[0,1])
b=np.matrix(a)
d=b*C_inv
e=np.multiply(d,b)
ingate=(e[:,0]+e[:,1])<1

FSC=data[ingate,6]
SSC=data[ingate,7]
FSC_A=data[ingate,0]
SSC_A=data[ingate,1]
YFP=data[ingate,2]##FL1_A


#Yeast gate:

#M = [6.3913 5.3564];
#C =  [[0.0392    0.0354];[0.0354    0.0708]];
#level = 1;
#FSC_h,SSC_h

#            for cellnum = 1:length(fsc_h)
#               if ([fsc_h(cellnum)-M(1) ssc_h(cellnum)-M(2)])*inv(C)*([fsc_h(cellnum)-M(1);ssc_h(cellnum)-M(2)])<level
#                    ingate = [ingate;cellnum];
###########
center = np.array([4.3,3.3])
ingate = 3*(np.log10(FSC_A)-center[0])**2+0.5*(np.log10(SSC_A)-center[1])**2<0.1
FSC=data[ingate,6]
FSC_A=data[ingate,0]
SSC_A=data[ingate,1]
YFP= data[ingate,2]##FL1_A
###########
#E.Coli gate:

#center = [4.3 3.3];
#log(FSC_a), log(SSC_a); log is in base 10.

#ingate = 3*(logfsc_a-center(1)).^2+0.5*(logssc_a-center(2)).^2<0.1;



YFPnorm_fsc= YFP.astype(float)/FSC.astype(float);
YFPnorm_ssc= YFP.astype(float)/SSC_A.astype(float);
mean_all_fsc= np.mean(YFPnorm_fsc);
mean_all_ssc = np.mean(YFPnorm_ssc);
median_all_fsc= np.median(YFPnorm_fsc);
median_all_ssc= np.median(YFPnorm_ssc);
var_all_fsc= np.var(YFPnorm_fsc);
var_all_ssc= np.var(YFPnorm_ssc);
mean_all = np.mean(YFP);

##if yeast
mean_seq_norm = np.mean(YFP.astype(float)/FSC_A.astype(float));
var_seq_norm = np.mean((YFP.astype(float)/FSC_A.astype(float))**2)- np.mean(YFP.astype(float)/FSC_A.astype(float))**2;
##else
mean_seq_norm = np.mean(YFP.astype(float)/FSC.astype(float));

mean_seq = np.mean(YFP);
var_seq = np.mean(YFP**2)-np.mean(YFP)**2;