import CFlow,time,threading,logging,math

logging.basicConfig(filename='C:\\Users\\rumarc\\Desktop\\Results\\CFlow_execution.log', level=logging.INFO,filemode='w',format='%(asctime)s %(message)s',datefmt='%Y-%m-%d %H:%M')
operate_arduino_object=CFlow.operate_arduino()

day=1#starting day
hour=11#starting hour
minute=16#starting minute
frequency_sampling=10#frequency of cytometer measurements, in minutes
samples=48#number of cytometer measurements in total
frequency_light=3600#frequency of led changes, in seconds
start_sample_well=0

reference=[]
for i in range(samples+1):				##Check that everything works goo if
  reference.append(math.sin(i*0.52)*0.1+0.5)		##Define radian change every 10 minutes; define offset; define proportionality constant


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
  operate_arduino_object.push_to_cytometer(0.9)##Critical time step. 2
  operate_arduino_object.push_to_cytometer(0)##0.3
  operate_arduino_object.cytometer_to_waste(7)#7
  operate_arduino_object.push_to_cytometer(1)##How much sample to introduce into cytometer. 1
  operate_arduino_object.air_to_cytometer(1.5)#2.5
  operate_arduino_object.cytometer_to_sample(3.5)#4.7
  operate_arduino_object.turn_off_valve('valve1')
  operate_arduino_object.turn_off_valve('valve2')
  return

def pumping_operation(day,hour,minute,frequency,num_samples,operate_arduino_object,ref,starting_well=0):
  click_object=CFlow.click(sample_counter=starting_well)
  click_object.set_measuring_times(day,hour,minute,frequency,num_samples)		#Set input correctly. day,hour,minute,frequency,num_samples
  read_fcs_object=CFlow.read_fcs('C:\\Users\\rumarc\\Desktop\\Results','ecoli')
  operate_arduino_object.operate_led(1,256)####
  operate_arduino_object.operate_led(2,0*256)####
  ##Feedback constants
  I=0
  P=0
  kp=0.8
  ki=0.08
  num_cycles=0
  
  ##
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
    ##PERFORM FEEDBACK
    YFP_mean=read_fcs_object.get_last_data(click_object)
    logging.info('YFP mean is: %f',YFP_mean)
    logging.info('reference is: %f',ref[num_cycles])
    print(YFP_mean)
    I=ki*(ref[num_cycles]-YFP_mean)+I
    print(I)
    logging.info('Integral parameter value is: %f',I)
    P=kp*(ref[num_cycles]-YFP_mean)
    print(P)
    logging.info('Proportional parameter value is: %f',P)
    LED_signal=P+I
    if LED_signal<0:
        LED_signal=0
    elif LED_signal>1:
        LED_signal=1
    logging.info('LED signal is: %f',LED_signal)
    print(LED_signal)
    LED_signal=LED_signal*256
    operate_arduino_object.operate_led(2,LED_signal)
	##
    click_object.backflush()
    operate_arduino_object.cytometer_to_waste(8)
    num_cycles+=1
  return

def led_operation(day,hour,minute,frequency,operate_arduino_object):#frequency is in seconds
  led=CFlow.led(operate_arduino_object)
  led.read_intensity_file(folder_path='C:\\Users\\rumarc\\Desktop\\Results',file_name='intensities.csv')			##ADD FOLDER
  led.scale_intensities()
  led.set_change_times(day,hour,minute,frequency)
  led.led_guide()
  return




thread1=threading.Thread(target=pumping_operation, args = (day,hour,minute,frequency_sampling,samples,operate_arduino_object,reference,start_sample_well))
thread1.start()

#thread2=threading.Thread(target=led_operation, args = (day,hour,minute,frequency_light,operate_arduino_object))
#thread2.start()
