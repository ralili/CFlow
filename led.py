import datetime,time,os,csv,logging,serial
class led:
	def __init__(self,operate_arduino_object):
		self.intensity=[]
		self.counter=0
		self.operate_arduino_object=operate_arduino_object
	def read_intensity_file(self,folder_path='C:\\Users\\rumarc\\Desktop\\Results',file_name='intensities.csv'):
		self.intensity=[]
		file_path=os.path.join(folder_path,file_name)
		file=open(file_path)
		test=csv.reader(file,delimiter=',')
		for line in test:
			self.intensity.append(line)
		self.number_rows=len(self.intensity)
		self.number_columns=len(self.intensity[0])
		if self.number_rows!=2:
			logging.warning('Led intensities file does not have correct format. Unequal number of rows')
			return
		if len(self.intensity[0])!=len(self.intensity[1]):
			logging.warning('Led intensities file does not have correct format. Unequal number of columns')
			return
	def scale_intensities(self):
		for j in range(self.number_rows):
			for i in range(self.number_columns):
				self.intensity[j][i]=float(self.intensity[j][i])*255
	def set_change_times(self,day,hour,minute,frequency):		#Step size is in seconds
		self.counter=0
		self.frequency=frequency
		time_today=datetime.datetime.now()
		starting_time=datetime.datetime(time_today.year,time_today.month,day,hour,minute,second=0) #User input is only day,hour,minute,second
		self.intensity_change_times=[]
		for i in range(self.number_columns):
			self.intensity_change_times.append(starting_time+datetime.timedelta(seconds=self.frequency*i))
	def led_guide(self):				#Tells led's when to change intensity
		self.operate_arduino_object.operate_led('led1',0)
		self.operate_arduino_object.operate_led('led2',0)
		while len(self.intensity_change_times)>self.counter:
			waiting_time=(self.intensity_change_times[self.counter]-datetime.datetime.now()).total_seconds()
			if waiting_time<0:
				logging.warning('timepoint %s already passed. Waiting for the next one'%(str(self.intensity_change_times[self.counter]))) #If timepoint has passed, wait for the next one (or should we just measure right away?)
				self.counter=self.counter+1
			else:
				#logging.info('Waiting time for led intensity change is: %d',waiting_time)
				time.sleep(waiting_time)						#time to sleep to next change
				self.operate_arduino_object.operate_led('led1',self.intensity[0][self.counter])
				self.operate_arduino_object.operate_led('led2',self.intensity[1][self.counter])
				self.counter=self.counter+1
		time.sleep(self.frequency)
		self.operate_arduino_object.operate_led('led1',0)
		self.operate_arduino_object.operate_led('led2',0)
		logging.info('all led intensity changes are done!!')
		return												#This indicates that experiment IS done. Close everything.
class led_array:
	'''This class was created to give input to an Arduino, which itself needs to be connected to the micro-controller in charge of
	controlling the array of LEDs. The Arduino also needs to have the correct code uploaded (LEDcontrol.ino)'''
	def __init__(self,port='COM5'):
		self.serial = serial.Serial(port)
	def setIntensities(self,sample1,sample2,sample3,sample4):
		lightSignal=''
		allSamples=([sample1,sample2,sample3,sample4])
		for individualSamples in reversed(allSamples):
			for LEDbrightness in reversed(individualSamples):
				binaryNumber=bin(int(round(LEDbrightness*4095)))[2:]#Get binary number out of light intensity. Should I multiply by another number instead of 4095?
				binaryNumber='0'*(12-len(binaryNumber))+binaryNumber#Convert to 12-bit number
				lightSignal+=binaryNumber
		if self.serial.write(lightSignal)!=144L:
			logging.warning('error on setIntensities. The light signal given does not have the correct dimensions/format')

		