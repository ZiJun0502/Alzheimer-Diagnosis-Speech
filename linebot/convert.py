import mfcc_obj
import NLP_obj
from datetime import datetime, timezone, timedelta
from pydub import AudioSegment

file_name = "/Users/raychang/Desktop/NTHU Courses/Machine Learning/final_project/Alzheimer-Diagnosis-Speech/linebot/_65421407.m4a"
wav_filename = 'output.wav'
sound = AudioSegment.from_file(file_name, format='m4a')
sound.export(wav_filename, format='wav')

MFCC = mfcc_obj.mfcc_features(wav_filename)
MFCC.mfcc_feature_calculation()
MFCC.mfcc_output("testdoc")