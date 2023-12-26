import csv
import numpy as np
import pandas as pd
filenames = []
funct = pd.read_csv('patient_info.csv')
filenames = list(funct['name'])
with open('Baycrest2103.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    feature_list=next(csv_reader)
    feature_list.insert(0,'name')
data=[]
for i in range(0,len(filenames)):
    with open(filenames[i]+'.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for row in csv_reader:
            data.append(row)
        data[i].insert(0,filenames[i])    
with open('praat_patient_combined.csv', 'w', newline='') as csvfile:
  writer = csv.writer(csvfile)
  writer.writerow(feature_list)
  for i in range(0,len(data)):
     writer.writerow(data[i])