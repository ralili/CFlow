##FILE TO GET THE TIMING FOR THE MULTISAMPLING CORRECT
import CFlow,yaml,os
os.chdir("C:\\Users\\rumarc\\Desktop\\Results")#CHANGE
arduinoObject=CFlow.multiOperate_arduino()

with open('setTiming.yaml', 'r') as f:
  doc = yaml.load(f)


airTimes1=[]
sampleTimes=[]
pbsTimes1=[]
pbsTimes2=[]
airTimes2=[]
backSampleTimes=[]

for i in range(len(doc)):
  for key in doc[i].keys():
    airTimes1.append(doc[i][key]['air1'])
    sampleTimes.append(doc[i][key]['sample'])
    pbsTimes1.append(doc[i][key]['pbs1'])
    pbsTimes2.append(doc[i][key]['pbs2'])
    airTimes2.append(doc[i][key]['air2'])
    backSampleTimes.append(doc[i][key]['back sample'])

def bring_sample(operate_arduino_object,sample,airTimes1,sampleTimes,pbsTimes2,airTimes2,backSampleTimes):
  sample=sample-1
  operate_arduino_object.air_to_cytometer(airTimes1[sample])
  raw_input()
  operate_arduino_object.sample_to_cytometer(sample+1,sampleTimes[sample])
  raw_input()
  operate_arduino_object.push_to_cytometer(pbsTimes1[sample])
  raw_input()
  operate_arduino_object.push_to_cytometer(pbsTimes2[sample])
  raw_input()
  operate_arduino_object.air_to_cytometer(airTimes2[sample])
  raw_input()
  operate_arduino_object.cytometer_to_sample(sample+1,backSampleTimes[sample])
  operate_arduino_object.turn_off_valves()
  return

bring_sample(arduinoObject,1,airTimes1,sampleTimes,pbsTimes2,airTimes2,backSampleTimes)