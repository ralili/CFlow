import os,re,csv
os.chdir('C:/Users/rumarc/Desktop')		#Folder where log file is located
csvfile=open('results.csv','w')			#Name of output file
csvwriter = csv.writer(csvfile, dialect='excel')
res1=open('CFlow_execution.log','r')	#Name of log file
res1lines=res1.readlines()

##Stuff that you want to get from the log file
YFP=['YFP']+[m.group(1) for line in res1lines for m in [re.search('YFP mean is: ([0-9.-]+)',line)] if m]
reference=['Reference']+[m.group(1) for line in res1lines for m in [re.search('reference is: ([0-9.-]+)',line)] if m]
Integral=['Integral']+[m.group(1) for line in res1lines for m in [re.search('Integral parameter value is: ([0-9.-]+)',line)] if m]
Proportional=['Proportional']+[m.group(1) for line in res1lines for m in [re.search('Proportional parameter value is: ([0-9.-]+)',line)] if m]
LED=['LED']+[m.group(1) for line in res1lines for m in [re.search('LED signal is: ([0-9.-]+)',line)] if m]
Time=['Time']+[(i)*10 for i in range(len(YFP)-1)]

##Write information extracted from the log file into a csv file. Csv file is created in the folder where the log file is located.
csvwriter.writerow(Time)
csvwriter.writerow(YFP)
csvwriter.writerow(reference)
csvwriter.writerow(Integral)
csvwriter.writerow(Proportional)
csvwriter.writerow(LED)

csvfile.close()