import CFlow,time,logging,matlab_wrapper
import numpy as np

logging.basicConfig(filename='C:\\Users\\rumarc\\Desktop\\Results\\CFlow_execution.log', level=logging.INFO,filemode='w',format='%(asctime)s %(message)s',datefmt='%Y-%m-%d %H:%M')
operate_arduino_object=CFlow.operate_arduino()

day=12#starting day
hour=11#starting hour
minute=37#starting minute
frequency_sampling=10#frequency of cytometer measurements, in minutes
samples=31#number of cytometer measurements in total
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
  ##Initial light conditions
  LED_signal=0#initial green light
  LED_signalTransformed=0
  operate_arduino_object.operate_led(1,256)
  operate_arduino_object.operate_led(2,LED_signal*256)
  ##Start up Matlab
  matlab = matlab_wrapper.MatlabSession()
  matlab.eval("parpool")
  matlab.eval("cd('C:\\Users\\localadmin\\Desktop\\Particle Filter')")
  ##Controller setup
  P=1000#number of particles
  MPChorizon=3#number of steps that the MPC looks ahead for the optimization
  reference=[3,]*(num_samples+MPChorizon)
  GFP_measurements=[]
  ##Dose-response Sigmoidal
  a=5.828
  b=3.353
  c=-0.05946
  d=-1.3388
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
    if cycle==0:
      initialGFPreading=GFP_mean
    GFP_measurements.append(GFP_mean/initialGFPreading)
    matlabCommand="LED=MPC_loop(%i,%i,%i,%i,%s,%s)"%(cycle+2,P,frequency,MPChorizon,str(GFP_measurements),str(reference))#!!!
    matlab.eval(matlabCommand)
    LED_signalTransformed=matlab.get('LED')
    LED_signal=np.log(a/(b*(LEDintensity-d))-1/b)/(c*100)
    if LED_signal>1:
        LED_signal=1
    elif LED_signal<0:
        LED_signal=0
    logging.info('LED signal is: %f',LED_signal)
    logging.info('reference is: %f',reference[0][cycle])
    print(LED_signal)
    operate_arduino_object.operate_led(2,LED_signal*256)
	##
    click_object.backflush()
    operate_arduino_object.cytometer_to_waste(8)
    cycle+=1
  return

pumping_operation(day,hour,minute,frequency_sampling,samples,operate_arduino_object,start_sample_well)
