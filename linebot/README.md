# LineBot interface

## Introduction  

This Brench is created for linebot implementation  
Mainly in file "Linebot", Which includes:  

_1. Linebot interface_  
_2. Data preprocess maintained as a class_  
_3. Model training process maintained as a class_  
_4. Side materials for testing_

##  Build Setup  

_1. Replit_  
_2. Google Run_  

## .env Setting  
_1. OpenAI token_  
_2. LineBot LINE_CHANNEL_ACCESS_TOKEN_ 
_3. LineBot LINE_CHANNEL_SECRET_  

## Directory Description  
main.py: Linebot interface  
mfcc_obj.py: MFCC data preprocess module  
NLP_obj.py: turn transcript into NLP analyze result  
Mergeinput.py: Merge MFCC, NLP result into single file, data preprocess module  
Other files: testing material  

## User Manual  
_1. Adding AD diagnoser as your friend_  
_2. Sending an audio message of a 30sec~1min speech to AD diagnoser(could  be either a description of a picture, or any monologue in English_  
_3. Waiting for response_

![image](https://i.imgur.com/Br1cRps.png)
![image](https://i.imgur.com/M08Eg7T.png)
![image](https://i.imgur.com/C5Onfz2.png)
