import CFlow,time,threading,logging

logging.basicConfig(filename='C:\\Users\\rumarc\\Desktop\\Results\\CFlow_execution.log', level=logging.INFO,filemode='w',format='%(asctime)s %(message)s',datefmt='%Y-%m-%d %H:%M')
operate_arduino_object=CFlow.operate_arduino()

day=28#starting day
hour=17#starting hour
minute=37#starting minute
frequency_sampling=10#frequency of cytometer measurements, in minutes
samples=21#number of cytometer measurements in total
frequency_light=3600#frequency of led changes, in seconds
start_sample_well=0

#CFLOW STARTUP
#PUMP CALIBRATION
#PUMP STARTUP
def bring_sample(operate_arduino_object):
  operate_arduino_object.sample_to_cytometer(1.25)##How much sample to take. 1.2
  operate_arduino_object.air_to_cytometer(1)#2
  operate_arduino_object.cytometer_to_waste(3)#3
  operate_arduino_object.push_to_cytometer(2.5)#2
  operate_arduino_object.cytometer_to_waste(3)#3
  operate_arduino_object.push_to_cytometer(2.5)#2
  operate_arduino_object.cytometer_to_waste(3)#3
  operate_arduino_object.push_to_cytometer(2)#2
  operate_arduino_object.cytometer_to_waste(3)#3
  operate_arduino_object.push_to_cytometer(0.4)##Critical time step. 2
  operate_arduino_object.push_to_cytometer(0)##0.3
  operate_arduino_object.cytometer_to_waste(7)#7
  operate_arduino_object.push_to_cytometer(1)##How much sample to introduce into cytometer. 1
  operate_arduino_object.air_to_cytometer(1.5)#2.5
  operate_arduino_object.cytometer_to_sample(3.5)#4.7
  operate_arduino_object.turn_off_valve('valve1')
  operate_arduino_object.turn_off_valve('valve2')
  return

def pumping_operation(day,hour,minute,frequency,num_samples,operate_arduino_object,starting_well=0):
  click_object=CFlow.click(sample_counter=starting_well)
  click_object.set_measuring_times(day,hour,minute,frequency,num_samples)		#Set input correctly. day,hour,minute,frequency,num_samples
  read_fcs_object=CFlow.read_fcs('C:\\Users\\rumarc\\Desktop\\Results','ecoli')
  operate_arduino_object.operate_led(1,256)####
  operate_arduino_object.operate_led(2,0*256)####
  ##controller setup
  controller=CFlow.MPC()
  reference=[0.66]*(num_samples+2)
  LED_signal=0
  ##
  cycle=0
  while click_object.set_waiting_time()==0:
    time.sleep(click_object.waiting_time)
    logging.info('waiting time until next measurement is: %f',click_object.waiting_time)
    bring_sample(operate_arduino_object)
    click_object.sample()
    click_object.run()
    click_object.export()
    time.sleep(1)
    click_object.moveFiles('C:\\Users\\rumarc\\Desktop','C:\\Users\\rumarc\\Desktop\\Results')###THIS CHANGES FROM COMPUTER TO COMPUTER. THE OUTPUT FOLDER MUST BE CREATED BEFOREHAND
    time.sleep(1)
    ##PERFORM CONTTROL
    GFP_mean=read_fcs_object.get_last_data(click_object)
    logging.info('GFP mean is: %f',GFP_mean)
    print(GFP_mean)
    controller.kalmanFilter(LED_signal,GFP_mean)
    LED_signal=controller.prediction(reference[cycle])####!!!!
    logging.info('LED signal is: %f',LED_signal)
    logging.info('reference is: %f',reference[cycle])
    print(LED_signal)
    operate_arduino_object.operate_led(2,LED_signal*256)
	##
    click_object.backflush()
    operate_arduino_object.cytometer_to_waste(8)
    cycle+=1
  return

def led_operation(day,hour,minute,frequency,operate_arduino_object):#frequency is in seconds
  led=CFlow.led(operate_arduino_object)
  led.read_intensity_file(folder_path='C:\\Users\\rumarc\\Desktop\\Results',file_name='intensities.csv')			##ADD FOLDER
  led.scale_intensities()
  led.set_change_times(day,hour,minute,frequency)
  led.led_guide()
  return




thread1=threading.Thread(target=pumping_operation, args = (day,hour,minute,frequency_sampling,samples,operate_arduino_object,start_sample_well))
thread1.start()

#thread2=threading.Thread(target=led_operation, args = (day,hour,minute,frequency_light,operate_arduino_object))
#thread2.start()
