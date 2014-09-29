## import the arduino Proto Api library
from Arduino import Arduino
import time,logging #import the time library
## open the serial port that your arduino is connected to.
class operate_arduino(Arduino):
	def __init__(self,valve1=2,valve2=4,pump1D=8,pump1S=9,pump2D=12,pump2S=11,led1=5,led2=10,sensor='A05'):#the defaults are the pins that I assume will be connected to the valves
		try:
			Arduino.__init__(self) #connect to arduino REMOVE THE PORT!!
		except ValueError:
			logging.warning('Error! Arduino was not found')
			return
		self.valve1=valve1
		self.valve2=valve2
		#self.valve3=valve3
		self.pump1D=pump1D
		self.pump1S=pump1S
		self.pump2D=pump2D
		self.pump2S=pump2S
		self.led1=led1
		self.led2=led2
		self.pinMode(self.valve1,'Output')
		self.digitalWrite(self.valve1,'HIGH')
		self.pinMode(self.valve2,'Output')
		self.digitalWrite(self.valve2,'HIGH')
		#self.pinMode(self.valve3,'Output')
		#self.digitalWrite(self.valve3,'HIGH')
		self.pinMode(self.pump1D,'Output')
		self.pinMode(self.pump1S,'Output')
		self.pinMode(self.pump2D,'Output')
		self.pinMode(self.pump2S,'Output')
		self.pinMode(self.led1,'Output')
		self.pinMode(self.led2,'Output')
		self.sensor=sensor

	def turn_on_valve(self, element): #set the pin to ON. The pin can either be called by its name (valve1, etc.) or by its number
		if element=='valve1' or element==self.valve1:
			temp=self.valve1
		elif element=='valve2' or element==self.valve2:
			temp=self.valve2
		elif element=='valve3' or element==self.valve3:
			temp=self.valve3
		else:
			return 'wrong element name'
		self.digitalWrite(temp,'LOW')
	def turn_off_valve(self, element): #set the pin to OFF. The pin can either be called by its name (valve1, etc.) or by its number
		if element=='valve1' or element==self.valve1:
			temp=self.valve1
		elif element=='valve2' or element==self.valve2:
			temp=self.valve2
		elif element=='valve3' or element==self.valve3:
			temp=self.valve3
		else:
			return 'wrong element name'
		self.digitalWrite(temp,'HIGH')

	def operate_pump(self,element,direction='right',speed=0): #set the pin to OFF. The pin can either be called by its name (valve1, etc.) or by its number
		if direction=='right':
			temp3='LOW'
		elif direction=='left':
			temp3='HIGH'
		else:
			return 'wrong direction name'
		
		if element=='pump1' or element==1:
			temp1=self.pump1D
			temp2=self.pump1S
			
		elif element=='pump2' or element==2:
			temp1=self.pump2D
			temp2=self.pump2S
		else:
			return 'wrong element name'
		self.digitalWrite(temp1,temp3)
		self.analogWrite(temp2,speed)
	def air_to_cytometer(self,seconds,speed=128):
		self.turn_on_valve('valve2')
		self.turn_off_valve('valve1')
		self.operate_pump('pump1','left',speed)
		time.sleep(seconds)
		self.operate_pump('pump1','right',0)
	def sample_to_cytometer(self,seconds,speed=128):
		self.turn_on_valve('valve1')
		self.operate_pump('pump1','left',speed)
		time.sleep(seconds)
		self.operate_pump('pump1','right',0)
	def cytometer_to_waste(self,seconds,speed=128):
		self.operate_pump('pump2','left',speed)
		time.sleep(seconds)
		self.operate_pump('pump2','left',0)
	def push_to_cytometer(self,seconds,speed=128):
		self.turn_off_valve('valve2')
		self.turn_off_valve('valve1')
		self.operate_pump('pump1','left',speed)
		time.sleep(seconds)	
		self.operate_pump('pump1','right',0)
	def cytometer_to_sample(self,seconds,speed=85):
		self.turn_on_valve('valve1') # Cytometer to Sample
		self.operate_pump('pump1','right',speed)
		time.sleep(seconds)
		self.operate_pump('pump1','left',0)
	def operate_led(self,led,frequency):
		if led=='led1' or led==1:
			pin=self.led1
		elif led=='led2' or led==2:
			pin=self.led2
		else:
			return 'wrong led name'
		self.analogWrite(pin,frequency)
	def read_sensor(self,N=250):
		value=0.
		for i in range(N):
			value=value+self.analogRead(self.sensor)/float(N)
		return value/1024.*1100

class multiOperate_arduino(Arduino):
	def __init__(self,valveP=6,valveS1=2,valveS2=3,valveS3=4,valveS4=5,pump1D=8,pump1S=9,pump2D=12,pump2S=11):#the defaults are the pins that I assume will be connected to the valves
		try:
			Arduino.__init__(self) #connect to arduino REMOVE THE PORT!!
		except ValueError:
			logging.warning('Error! Arduino was not found')
			return
		self.valveP=valveP
		self.valveS1=valveS1
		self.valveS2=valveS2
		self.valveS3=valveS3
		self.valveS4=valveS4#
		self.valveList=[self.valveP,self.valveS1,self.valveS2,self.valveS3,self.valveS4]
		self.pump1D=pump1D#
		self.pump1S=pump1S
		self.pump2D=pump2D
		self.pump2S=pump2S
		self.pinMode(self.valveP,'Output')#
		self.digitalWrite(self.valveP,'HIGH')
		self.pinMode(self.valveS1,'Output')
		self.digitalWrite(self.valveS1,'HIGH')
		self.pinMode(self.valveS2,'Output')
		self.digitalWrite(self.valveS2,'HIGH')
		self.pinMode(self.valveS3,'Output')
		self.digitalWrite(self.valveS3,'HIGH')
		self.pinMode(self.valveS4,'Output')
		self.digitalWrite(self.valveS4,'HIGH')
		self.pinMode(self.pump1D,'Output')#
		self.pinMode(self.pump1S,'Output')
		self.pinMode(self.pump2D,'Output')
		self.pinMode(self.pump2S,'Output')
	def operate_valve(self,element,state): #set the pin to ON. The pin can either be called by its name (valve1, etc.) or by its number
		if element=='valveP' or element==self.valveP:
			temp=self.valveP
		elif element=='valveS1' or element==self.valveS1:
			temp=self.valveS1
		elif element=='valveS2' or element==self.valveS2:
			temp=self.valveS2
		elif element=='valveS3' or element==self.valveS3:
			temp=self.valveS3
		elif element=='valveS4' or element==self.valveS4:
			temp=self.valveS4
		else:
			logging.warning('Error! wrong element name on operate_valve call')
			return
		if state=='HIGH' or state=='OFF':#Means no current to valve.
			state='HIGH'
		elif state=='LOW' or state=='ON':#Means current to valve.
			state='LOW'
		else:
			logging.warning('Error! wrong state name on operate_valve call')
			return
		self.digitalWrite(temp,state)
	def turn_off_valves(self):#Turns off all valves
		self.digitalWrite(self.valveP,'HIGH')
		self.digitalWrite(self.valveS1,'HIGH')
		self.digitalWrite(self.valveS2,'HIGH')
		self.digitalWrite(self.valveS3,'HIGH')
		self.digitalWrite(self.valveS4,'HIGH')
	def operate_pump(self,element,direction='right',speed=0): #set the pin to OFF. The pin can either be called by its name (valve1, etc.) or by its number
		if direction=='right':
			temp3='LOW'
		elif direction=='left':
			temp3='HIGH'
		else:
			return 'wrong direction name'
		
		if element=='pump1' or element==1:
			temp1=self.pump1D
			temp2=self.pump1S
			
		elif element=='pump2' or element==2:
			temp1=self.pump2D
			temp2=self.pump2S
		else:
			return 'wrong element name'
		self.digitalWrite(temp1,temp3)
		self.analogWrite(temp2,speed)
	def air_to_cytometer(self,seconds,speed=128):
		self.operate_valve(self.valveP,'ON')
		self.operate_valve(self.valveS1,'OFF')
		self.operate_valve(self.valveS2,'OFF')
		self.operate_valve(self.valveS3,'OFF')
		self.operate_valve(self.valveS4,'OFF')
		self.operate_pump('pump1','left',speed)
		time.sleep(seconds)
		self.operate_pump('pump1','right',0)
	def sample_to_cytometer(self,sample,seconds,speed=128):
		self.operate_valve(self.valveP,'OFF')
		for i in range(4):
			if i+1==sample:
				self.operate_valve(self.valveList[i+1],'ON')
			else:
				self.operate_valve(self.valveList[i+1],'OFF')
		self.operate_pump('pump1','left',speed)
		time.sleep(seconds)
		self.operate_pump('pump1','right',0)
	def cytometer_to_waste(self,seconds,speed=128):
		self.operate_pump('pump2','left',speed)
		time.sleep(seconds)
		self.operate_pump('pump2','left',0)
	def push_to_cytometer(self,seconds,speed=128):
		self.operate_valve(self.valveP,'OFF')
		self.operate_valve(self.valveS1,'OFF')
		self.operate_valve(self.valveS2,'OFF')
		self.operate_valve(self.valveS3,'OFF')
		self.operate_valve(self.valveS4,'OFF')
		self.operate_pump('pump1','left',speed)
		time.sleep(seconds)	
		self.operate_pump('pump1','right',0)
	def cytometer_to_sample(self,sample,seconds,speed=85):
		self.operate_valve(self.valveP,'OFF')
		for i in range(4):
			if i+1==sample:
				self.operate_valve(self.valveList[i+1],'ON')
			else:
				self.operate_valve(self.valveList[i+1],'OFF')
		self.operate_pump('pump1','right',speed)
		time.sleep(seconds)
		self.operate_pump('pump1','left',0)

		


