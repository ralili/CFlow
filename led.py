import datetime,time,os,csv
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
			print('Led intensities file does not have correct format. Unequal number of rows')
			return
		if len(self.intensity[0])!=len(self.intensity[1]):
			print('Led intensities file does not have correct format. Unequal number of columns')
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
				print('timepoint %s already passed. Waiting for the next one'%(str(self.intensity_change_times[self.counter]))) #If timepoint has passed, wait for the next one (or should we just measure right away?)
				self.counter=self.counter+1
			else:
				print(waiting_time)
				time.sleep(waiting_time)						#time to sleep to next change
				self.operate_arduino_object.operate_led('led1',self.intensity[0][self.counter])
				self.operate_arduino_object.operate_led('led2',self.intensity[1][self.counter])
				self.counter=self.counter+1
		time.sleep(self.frequency)
		self.operate_arduino_object.operate_led('led1',0)
		self.operate_arduino_object.operate_led('led2',0)
		print('Experiment is done!!')
		return												#This indicates that experiment IS done. Close everything.