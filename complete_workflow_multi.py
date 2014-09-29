import CFlow,time,threading,logging

logging.basicConfig(filename='C:\\Users\\rumarc\\Desktop\\Results\\CFlow_execution.log', level=logging.INFO,filemode='w',format='%(asctime)s %(message)s',datefmt='%Y-%m-%d %H:%M')
arduinoObject=CFlow.multiOperate_arduino()

day=2#starting day
hour=18#starting hour
minute=20#starting minute
frequency_sampling=[5,5,5,5]#frequency of cytometer measurements, in minutes
samples=[21,0,0,0]#number of cytometer measurements in total
start_sample_well=0

def pumping_operation(day,hour,minute,frequency,num_samples,operate_arduino_object,samplingObject,starting_well=0):
  samplingObject=CFlow.sampleHandling()
  samplingObject.setTimes(folder)

  click_object=CFlow.click(sample_counter=starting_well)
  click_object.set_measuring_times(day,hour,minute,frequency,num_samples)		#Set input correctly. day,hour,minute,frequency,num_samples

  read_fcs_object=CFlow.read_fcs('C:\\Users\\rumarc\\Desktop\\Results','ecoli')

  while click_object.set_waiting_time()==0:
    time.sleep(click_object.waiting_time)
    logging.info('waiting time until next measurement is: %f',click_object.waiting_time)
    samplingObject.bring_sample(operate_arduino_object,sample=click_object.measuring_times[click_object.time_counter][1])
    click_object.sample()
    click_object.run()
    click_object.export()
    time.sleep(1)
    click_object.moveFiles('C:\\Users\\rumarc\\Desktop','C:\\Users\\rumarc\\Desktop\\Results')###THIS CHANGES FROM COMPUTER TO COMPUTER. THE OUTPUT FOLDER MUST BE CREATED BEFOREHAND
    time.sleep(1)
    ##PERFORM FEEDBACK
    ##
    click_object.backflush()
    operate_arduino_object.cytometer_to_waste(7)
  return

pumping_operation(day,hour,minute,frequency_sampling,samples,operate_arduino_object,samplingObject,start_sample_well)