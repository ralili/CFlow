import os,re,csv
os.chdir('C:/Users/rumarc/Desktop/LBperturbation25032014')
csvfile=open('res.csv','w')
csvwriter = csv.writer(csvfile, dialect='excel')
res1=open('CFlow_execution25032014(1).log','r')
res1lines=res1.readlines()

YFP=['YFP']+[m.group(1) for line in res1lines for m in [re.search('YFP mean is: ([0-9.-]+)',line)] if m]
Integral=['Integral']+[m.group(1) for line in res1lines for m in [re.search('Integral parameter value is: ([0-9.-]+)',line)] if m]
Proportional=['Proportional']+[m.group(1) for line in res1lines for m in [re.search('Proportional parameter value is: ([0-9.-]+)',line)] if m]
LED=['LED']+[m.group(1) for line in res1lines for m in [re.search('LED signal is: ([0-9.-]+)',line)] if m]

res2=open('CFlow_execution25032014(2).log','r')
res2lines=res2.readlines()

YFP=YFP+[m.group(1) for line in res2lines for m in [re.search('YFP mean is: ([0-9.-]+)',line)] if m]
Integral=Integral+[m.group(1) for line in res2lines for m in [re.search('Integral parameter value is: ([0-9.-]+)',line)] if m]
Proportional=Proportional+[m.group(1) for line in res2lines for m in [re.search('Proportional parameter value is: ([0-9.-]+)',line)] if m]
LED=LED+[m.group(1) for line in res2lines for m in [re.search('LED signal is: ([0-9.-]+)',line)] if m]
Time=['Time']+[(i+2)*10 for i in range(len(LED)-1)]

csvwriter.writerow(Time)
csvwriter.writerow(YFP)
csvwriter.writerow(Integral)
csvwriter.writerow(Proportional)
csvwriter.writerow(LED)

csvfile.close()