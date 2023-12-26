import pydub
import noisereduce
from pydub import AudioSegment
from noisereduce import reduce_noise
import whisper
from scipy.io import wavfile
import csv

filenames = []
f = open('ted_info.txt')
for line in f.readlines():
    filenames.append(line[0:len(line)-1])
f.close
model = whisper.load_model("base")
print(len(filenames))
time_len=[]
for i in range(0,len(filenames)):
    try:
      source_file_path='unnoise_'+filenames[i][0:len(filenames[i])-4]+'.wav'
      samplerate, data = wavfile.read(source_file_path)
      time_len.append(len(data))
    except:
      print("continue")
      print(filenames[i])
      continue
print(len(time_len))
with open('time_result.csv', 'w', newline='') as csvfile:
  writer = csv.writer(csvfile)
  writer.writerow(['name','time_split'])
  for i in range(0,len(filenames)):
        list1=[]
        list1.append(filenames[i])
        list1.append(time_len[i])
        writer.writerow(list1)
                   
      

	
	