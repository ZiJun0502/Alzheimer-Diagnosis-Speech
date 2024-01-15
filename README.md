# Alzheimer-Diagnosis-Speech
## Data resource
### [DementiaBank](https://dementia.talkbank.org/access/)
We use the dataset used in the competition and the tags on it to classify the MCI and AD classes in all of the patients.
### [TED-LIUM release1](https://huggingface.co/datasets/LIUM/tedlium)
We use the dataset composed of Ted Talks in 2012. The reason we chose it is because of the fluency of the speaker's speech and the length of the speech, which is suitable for the patient dataset.

## LineBot interface

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

## User Manual  
_1. Adding AD diagnoser as your friend_  
_2. Sending an audio message of a 30sec~1min speech to AD diagnoser(could  be either a description of a picture, or any monologue in English_  
_3. Waiting for response_

![image](https://i.imgur.com/Br1cRps.png)
![image](https://i.imgur.com/M08Eg7T.png)
![image](https://i.imgur.com/C5Onfz2.png)
