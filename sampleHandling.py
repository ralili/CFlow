import yaml,time,os
class sampleHandling:
	'''class that contains all functions related to bringing the sample from the cell culture to the cytometer. Finds the timings specified by the user and operates the arduino accordingly'''
	def __init__(self,directory='C:\\Users\\localadmin\\Desktop'):
		self.directory=directory
		self.setTimes(self.directory)
	def setTimes(self,directory):
		with open(os.path.join(directory,'setTiming.yaml'), 'r') as f:
			doc = yaml.load(f)
		self.airTimes1=[]
		self.sampleTimes=[]
		self.pbsTimes1=[]
		self.pbsTimes2=[]
		self.airTimes2=[]
		self.backSampleTimes=[]
		for i in range(len(doc)):
			for key in doc[i].keys():
				self.airTimes1.append(doc[i][key]['air1'])
				self.sampleTimes.append(doc[i][key]['sample'])
				self.pbsTimes1.append(doc[i][key]['pbs1'])
				self.pbsTimes2.append(doc[i][key]['pbs2'])
				self.airTimes2.append(doc[i][key]['air2'])
				self.backSampleTimes.append(doc[i][key]['back sample'])
		return
	def bring_sample(self,operate_arduino_object,sample):
		sample=sample-1
		operate_arduino_object.operate_pump('pump2','left',speed)
		operate_arduino_object.air_to_cytometer(self.airTimes1[sample])
		operate_arduino_object.sample_to_cytometer(sample+1,self.sampleTimes[sample])
		operate_arduino_object.push_to_cytometer(self.pbsTimes1[sample])
		time.sleep(2)
		operate_arduino_object.operate_pump('pump2','left',0)
		operate_arduino_object.push_to_cytometer(self.pbsTimes2[sample])
		operate_arduino_object.air_to_cytometer(self.airTimes2[sample])
		operate_arduino_object.cytometer_to_sample(sample+1,self.backSampleTimes[sample])
		operate_arduino_object.turn_off_valves()
		return