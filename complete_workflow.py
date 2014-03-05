import CFlow,time,threading
a=CFlow.operate_arduino()
b=CFlow.click()
c=CFlow.click()

#CFLOW STARTUP
#PUMP CALIBRATION
#PUMP STARTUP
def bring_sample(operate_arduino_object):			#a is a CFlow.operate_arduino() object
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

def pumping_operation(day,hour,minute,frequency,num_samples,operate_arduino_object,click_object):
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

def led_operation(operate_arduino_object)
  operate_arduino_object.operate_led('led1',256)
  time.sleep(2000)
  operate_arduino_object.operate_led('led1',0)
  operate_arduino_object.operate_led('led2',256)
  time.sleep(2000)
  operate_arduino_object.operate_led('led2',0)
  return

thread1=threading.Thread(target=pumping_operation, args = (day,hour,minute,frequency,num_samples,a,b))
thread2=threading.Thread(target=ked_operation, args = (a))
thread1.start()
thread2.start()

pumping_operation(day,hour,minute,frequency,num_samples,a,b)
