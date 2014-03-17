from fcm import loadFCS
import numpy as np
import os
import csv

class read_fcs:
	def __init__(self,folder,cell_type=None):
		self.folder=folder
		self.cell_type=cell_type
	def extract_data(self,file_name):
		self.data=loadFCS(os.path.join(self.folder,file_name))
		self.FSC_H=[self.data[:,index] for index in range(len(self.data.channels)) if self.data.channels[index]=='FSC-H'][0]#extracts data of desired channel.
		self.SSC_H=[self.data[:,index] for index in range(len(self.data.channels)) if self.data.channels[index]=='SSC-H'][0]#extracts data of desired channel.
		self.FSC_A=[self.data[:,index] for index in range(len(self.data.channels)) if self.data.channels[index]=='FSC-A'][0]#extracts data of desired channel.
		self.SSC_A=[self.data[:,index] for index in range(len(self.data.channels)) if self.data.channels[index]=='SSC-A'][0]#extracts data of desired channel.
		self.YFP=[self.data[:,index] for index in range(len(self.data.channels)) if self.data.channels[index]=='FL1-A'][0]#extracts data of desired channel.
	def gate(self):
		if self.cell_type=='yeast' or self.cell_type=='2':
			M=np.matrix('6.3913 5.3564')
			C = np.matrix('0.0392,0.0354;0.0354,0.0708')
			C_inv=np.linalg.inv(C)
			a=zip(np.log10(self.FSC_H)-M[0,0],np.log10(self.SSC_H)-M[0,1])
			b=np.matrix(a)
			d=b*C_inv
			e=np.multiply(d,b)
			ingate=(e[:,0]+e[:,1])<1

			self.FSC_H=self.data[ingate,6]
			self.SSC_H=self.data[ingate,7]
			self.FSC_A=self.data[ingate,0]
			self.SSC_A=self.data[ingate,1]
			self.YFP=self.data[ingate,2]##FL1_A
		elif self.cell_type=='ecoli' or self.cell_type=='1':
			center = np.array([4.3,3.3])
			ingate = (3*(np.log10(self.FSC_A)-center[0])**2+0.5*(np.log10(self.SSC_A)-center[1]))**2<0.1
			ingate = ingate*(self.YFP>300)
			self.FSC_H=self.data[ingate,6]
			self.FSC_A=self.data[ingate,0]
			self.SSC_A=self.data[ingate,1]
			self.YFP= self.data[ingate,2]##FL1_A
	def normalize(self):
		self.YFPnorm_fsc= self.YFP.astype(float)/self.FSC_H.astype(float);
		#self.YFPnorm_ssc= self.YFP.astype(float)/self.SSC_A.astype(float);
		self.mean_all_fsc= np.mean(self.YFPnorm_fsc);
		#self.mean_all_ssc = np.mean(YFPnorm_ssc);
		self.median_all_fsc= np.median(self.YFPnorm_fsc);
		#self.median_all_ssc= np.median(YFPnorm_ssc);
		self.var_all_fsc= np.var(self.YFPnorm_fsc);
		#self.var_all_ssc= np.var(YFPnorm_ssc);
		self.mean_all = np.mean(self.YFP);
	def print_results(self):
		files = [ f for f in os.listdir(self.folder) if (os.path.isfile(os.path.join(self.folder,f)) and f[-4:]=='.fcs')]
		self.means=[]
		self.medians=[]
		for f in files:
			self.extract_data(f)
			self.gate()
			self.normalize()
			self.means.append(self.mean_all_fsc)
			self.medians.append(self.median_all_fsc)
		csvfile=open(os.path.join(self.folder,'results.csv'),'w+')
		csvwriter = csv.writer(csvfile, dialect='excel')
		csvwriter.writerow(files)
		csvwriter.writerow(self.means)
		csvwriter.writerow(self.medians)
		csvfile.close()
	def get_last_data(self,click_object):
		last_sample=click_object.sample_counter-1
		letter_list=['A','B','C','D','E','F','G','H']
		letter=letter_list[(last_sample/12)]
		number=last_sample%12+1
		well_name=('%s%02d'%(letter,number))
		file_name = [ f for f in os.listdir(self.folder) if (os.path.isfile(os.path.join(self.folder,f)) and f[0:3]==well_name)]
		self.extract_data(file_name[0])
		self.gate()
		self.normalize()
		return self.mean_all_fsc


#available channels: ['FSC-A', 'SSC-A', 'FL1-A', 'FL2-A', 'FL3-A', 'FL4-A', 'FSC-H', 'SSC-H', 'FL1-H', 'FL2-H', 'FL3-H', 'FL4-H', 'Width', 'Time']

#####Gate
#####Get FL1-A/FSC-H
#####Get median of resulting vector


##if yeast
#mean_seq_norm = np.mean(YFP.astype(float)/FSC_A.astype(float));
#var_seq_norm = np.mean((YFP.astype(float)/FSC_A.astype(float))**2)- np.mean(YFP.astype(float)/FSC_A.astype(float))**2;
##else
#mean_seq_norm = np.mean(YFP.astype(float)/FSC.astype(float));

##mean_seq = np.mean(YFP);
##var_seq = np.mean(YFP**2)-np.mean(YFP)**2;