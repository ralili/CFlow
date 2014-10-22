from fcm import loadFCS
import numpy as np
import os,csv,time,logging

class read_fcs:
	def __init__(self,folder,cell_type=None):
		self.folder=folder
		self.cell_type=cell_type
		self.extract_error=0
	def extract_data(self,file_name):
	#extract data from the specified file and save it into memory
		try:
			self.data=loadFCS(os.path.join(self.folder,file_name))
		except IOError:		#If the file is not found, try again in 2 seconds (wait for the cytometer software to export the file) and if the files are still not found, give up.
			if self.extract_error!=1:
				self.extract_error=1
				time.sleep(2)
				self.extract_data(file_name)
				return
			else:
				logging.warning('fcs file named %s was not found in folder %s',file_name,self.folder)
				self.extract_error=0
				return
		self.extract_error=0
		self.FSC_H=[self.data[:,index] for index in range(len(self.data.channels)) if self.data.channels[index]=='FSC-H'][0]#extracts data of desired channel.
		self.SSC_H=[self.data[:,index] for index in range(len(self.data.channels)) if self.data.channels[index]=='SSC-H'][0]#extracts data of desired channel.
		self.FSC_A=[self.data[:,index] for index in range(len(self.data.channels)) if self.data.channels[index]=='FSC-A'][0]#extracts data of desired channel.
		self.SSC_A=[self.data[:,index] for index in range(len(self.data.channels)) if self.data.channels[index]=='SSC-A'][0]#extracts data of desired channel.
		self.GFP=[self.data[:,index] for index in range(len(self.data.channels)) if self.data.channels[index]=='FL1-A'][0]#extracts data of desired channel.	
	def gate(self):
	#gate data in memory
		if self.cell_type=='yeast' or self.cell_type==2:
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
			self.GFP=self.data[ingate,2]##FL1_A
		elif self.cell_type=='ecoli' or self.cell_type==1:
			center = np.array([4.3,3.3])
			ingate = (3*(np.log10(self.FSC_A)-center[0])**2+0.5*(np.log10(self.SSC_A)-center[1]))**2<0.1
			ingate = ingate*(self.GFP>800)
			self.FSC_H=self.data[ingate,6]
			self.FSC_A=self.data[ingate,0]
			self.SSC_A=self.data[ingate,1]
			self.GFP= self.data[ingate,2]##FL1_A
	def normalize(self):
	#Normalize data in memory
		self.GFPnorm_fsc= self.GFP.astype(float)/self.FSC_H.astype(float);
		#self.GFPnorm_ssc= self.GFP.astype(float)/self.SSC_A.astype(float);
		self.mean_all_fsc= np.mean(self.GFPnorm_fsc);
		#self.mean_all_ssc = np.mean(GFPnorm_ssc);
		self.median_all_fsc= np.median(self.GFPnorm_fsc);
		#self.median_all_ssc= np.median(GFPnorm_ssc);
		self.var_all_fsc= np.var(self.GFPnorm_fsc);
		#self.var_all_ssc= np.var(GFPnorm_ssc);
		self.mean_all = np.mean(self.GFP);
	def print_results(self):
	#generate a csv file with the normalized mean of all .fcs files in the folder
		files = [ f for f in os.listdir(self.folder) if (os.path.isfile(os.path.join(self.folder,f)) and f[-4:]=='.fcs')]
		self.means=[]
		self.var=[]
		for f in files:
			self.extract_data(f)
			self.gate()
			self.normalize()
			self.means.append(self.mean_all_fsc)
			self.var.append(self.var_all_fsc)
		csvfile=open(os.path.join(self.folder,'results.csv'),'w+')
		csvwriter = csv.writer(csvfile, dialect='excel')
		csvwriter.writerow(files)
		csvwriter.writerow(self.means)
		csvwriter.writerow(self.var)
		csvfile.close()
	def get_last_data(self,click_object,output='mean'):
	#Get normalized mean from last sample taken
		last_sample=click_object.sample_counter-1
		letter_list=['A','B','C','D','E','F','G','H']
		letter=letter_list[(last_sample/12)]
		number=last_sample%12+1
		well_name=('%s%02d'%(letter,number))
		file_name = [ f for f in os.listdir(self.folder) if (os.path.isfile(os.path.join(self.folder,f)) and f[0:3]==well_name)]
		self.extract_data(file_name[0])
		self.gate()
		self.normalize()
		if output=='variance':
			lowerSize=np.percentile(self.GFPnorm_fsc,5)
			upperSize=np.percentile(self.GFPnorm_fsc,95)
			crib1=self.GFPnorm_fsc[self.GFPnorm_fsc>lowerSize]
			crib2=crib1[crib1<upperSize]
			return np.var(crib2)
		elif output=='mean':
			return self.mean_all_fsc
	def sampleToCSV(self,file_name):
	#Generate csv file with normalized GFP fluorescence of current data in memory
		self.extract_data(file_name)
		self.gate()
		self.normalize()
		csvfile=open(os.path.join(self.folder,file_name[:-3]+'csv'),'w+')
		csvwriter = csv.writer(csvfile, dialect='excel')
		csvwriter.writerow(self.GFPnorm_fsc)
		csvfile.close()

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