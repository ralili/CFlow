import datetime,time
class led:
	def __init__(self,operate_arduino_object):
		self.intensity=[]
		self.counter=0
		self.operate_arduino_object=operate_arduino_object
	def read_intensity_file(self,file='intensities.csv'):
		file=open('file_name.csv')
		test=csv.reader(file,delimiter=',')
		for line in test:
			self.intensity.append(line)
		number_rows=len(self.intensity)
		number_columns=len(self.intensity[0])
		if number_rows!=2:
			print('Led intensities file does not have correct format. Unequal number of rows')
			return
		if len(self.intensity[0])!=len(self.intensity[1]:
			print('Led intensities file does not have correct format. Unequal number of columns')
				return
	def scale_intensities(self):
		for j in range(number_rows):
			for i range(number_columns):
				self.intensity[0][i]=self.intensity[0][i]*255
	def set_change_times(self,day,hour,minute,frequency):		#Step size is in seconds
		time_today=datetime.datetime.now()
		starting_time=datetime.datetime(time_today.year,time_today.month,day,hour,minute,second=0) #User input is only day,hour,minute,second
		self.intensity_change_times=[]
		for i in range(number_rows):
			self.intensity_change_times.append(starting_time+datetime.timedelta(seconds=frequency*i))
	def led_guide(self):				#Tells led's when to change intensity
		while len(self.intensity_change_times)>self.counter:
			waiting_time=(self.intensity_change_times[self.counter]-datetime.datetime.now()).total_seconds()
			if waiting_time<0:
				print('timepoint %s already passed. Waiting for the next one'%(str(self.intensity_change_times[self.counter]))) #If timepoint has passed, wait for the next one (or should we just measure right away?)
				self.counter=self.counter+1
			else:
				self.operate_arduino_object.operate_led('led1',self.intensity[0][self.counter])
				self.operate_arduino_object.operate_led('led2',self.intensity[1][self.counter])
				time.sleep(waiting_time)						#time to sleep to next change
				self.counter=self.counter+1
		print('Experiment is done!!')
		return												#This indicates that experiment IS done. Close everything.