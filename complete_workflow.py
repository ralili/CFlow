import CFlow,time,threading

#CFLOW STARTUP
#PUMP CALIBRATION
#PUMP STARTUP
def bring_sample(operate_arduino_object):
  operate_arduino_object.sample_to_cytometer(1.4)##How much sample to take
  operate_arduino_object.air_to_cytometer(2)
  operate_arduino_object.cytometer_to_waste(3)
  operate_arduino_object.push_to_cytometer(2)
  operate_arduino_object.cytometer_to_waste(3)
  operate_arduino_object.push_to_cytometer(2)
  operate_arduino_object.cytometer_to_waste(3)
  operate_arduino_object.push_to_cytometer(2)
  operate_arduino_object.cytometer_to_waste(3)
  operate_arduino_object.push_to_cytometer(2)##Critical time step
  operate_arduino_object.push_to_cytometer(1)##
  operate_arduino_object.cytometer_to_waste(7)
  operate_arduino_object.push_to_cytometer(1)##How much sample to introduce into cytometer
  operate_arduino_object.air_to_cytometer(2.5)
  operate_arduino_object.cytometer_to_sample(5)
  operate_arduino_object.turn_off_valve('valve1')
  operate_arduino_object.turn_off_valve('valve2')
  return

def pumping_operation(day,hour,minute,frequency,num_samples,operate_arduino_object):
  click_object=CFlow.click()
  click_object.set_measuring_times(day,hour,minute,frequency,num_samples)		#Set input correctly. day,hour,minute,frequency,num_samples
  while click_object.set_waiting_time()==0:
    time.sleep(click_object.waiting_time)
    print(click_object.waiting_time)
    bring_sample(operate_arduino_object)
    click_object.sample()
    click_object.run()
    click_object.export()
    click_object.moveFiles('C:\\Users\\rumarc\\Desktop','C:\\Users\\rumarc\\Desktop\\Results')###THIS CHANGES FROM COMPUTER TO COMPUTER. THE OUTPUT FOLDER MUST BE CREATED BEFOREHAND
    ##PERFORM FEEDBACK
    click_object.backflush()
    operate_arduino_object.cytometer_to_waste(7)
  return

def led_operation(day,hour,minute,frequency,operate_arduino_object)
  led=CFlow.led(operate_arduino_object)
  led.read_intensity_file()
  led.scale_intensities()
  led.set_change_times(day,hour,minute,frequency)
  led.guide()
  return

operate_arduino_object=CFlow.operate_arduino()
click_object=CFlow.click()
day=
hour=
minute=
frequency_sampling=
samples=
frequency_light=
  

thread1=threading.Thread(target=pumping_operation, args = (day,hour,minute,frequency_sampling,num_samples,operate_arduino_object,click_object))
thread2=threading.Thread(target=led_operation, args = (day,hour,minute,frequency_light,operate_arduino_object))
thread1.start()
thread2.start()
