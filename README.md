# Alzheimer-Diagnosis-Speech
## Data Resource
### [DementiaBank](https://dementia.talkbank.org/access/)
We use the dataset used in the competition and the tags on it to classify the MCI and AD classes in all of the patients.
### [TED-LIUM release1](https://huggingface.co/datasets/LIUM/tedlium)
We use the dataset composed of Ted Talks in 2012. The reason we chose it is because of the fluency of the speaker's speech and the length of the speech, which is suitable for the patient dataset.
## Denoise Implementation
```bush
!pip install pydub
!pip install noisereduce
```
We can simply transform the signal file (.wav file) into an AudioSegment object using pydub. Then, we can use the well-tuned noise reduction library NoiseReduce to implement a noise reduction function on the audio. It's crucial for preprocessing in acoustic feature extraction. The more noise-reduction implementations are developed, the more they will be stored in the NR folder.

## Acoustical Analysis
### MFCC
This Python script processes a collection of WAV files in the 'wav' directory to extract Mel Frequency Cepstral Coefficients (MFCCs). The script follows the standard procedure for MFCC extraction:
1. Frame the Signal
2. Calculate Power Spectrum
3. Apply Mel Filterbank
4. Logarithm of Filterbank Energies
5. Discrete Cosine Transform (DCT)
6. Extract MFCCs

#### Usage
1. Place your WAV files in the 'wav' directory.
2. Run the script to extract MFCC features from each WAV file.
3. CSV files with extracted MFCC features will be generated for each corresponding WAV file.

#### Installation
```bash
pip install numpy scipy
```
Feel free to customize the script based on your specific needs. Adjust frame length, frame shift, and other parameters as necessary.

### Praat
This Python script utilizes the Parselmouth library to extract various acoustic features from a collection of WAV files in the 'patient_wav' directory. The extracted features include intensity, pitch, harmonics-to-noise ratio (HNR), glottal-to-noise ratio (GNE), local jitter, local shimmer, spectrum attributes, and formant attributes.

#### Usage
1. Place your WAV files in the 'patient_wav' directory.
2. Run the script to extract acoustic features from each WAV file.
3. CSV files containing the extracted features will be generated for each corresponding WAV file.

#### Installation
```bash
pip install pandas parselmouth
```
#### Output
CSV files with extracted acoustic features will be created for each WAV file in the 'patient_wav' directory.

Feel free to customize the script based on your specific needs and modify the 'directory' variable if your WAV files are located elsewhere.

# Alzheimer's Disease Prediction Model Using MFCC and NLP Features

## Overview
This comprehensive guide covers three Alzheimer's Disease (AD) prediction models, focusing on machine learning techniques, MFCC data extraction, and a combination of MFCC and NLP features. These models aim to predict AD using various classifiers and data sources, including patient and normal datasets.

## Requirements
- Python 3.x
- Libraries: pandas, numpy, sklearn, matplotlib, csv
- Google Colab for drive mounting and processing

## Installation
1. Install Python 3 and required libraries using pip.
2. Use Google Colab for executing scripts and accessing Google Drive.

## Usage
### Common Steps for All Models
- **Connect to Google Drive**: Use Google Colab to mount your Google Drive for data access.
- **Import Required Packages**: Import Python packages like pandas, numpy, sklearn, os, etc.

### Model-Specific Steps
#### 1. Machine Learning Model for AD Prediction
- **Data Preparation**: Load the dataset from Google Drive and split it into training and test sets.
- **Feature Selection using Lasso**: Perform feature selection using Lasso regression.
- **Model Training and Evaluation**: Train models like KNN, SVM, Decision Tree, etc., and evaluate using metrics like accuracy, MCC, and F1-score.
- **Results Visualization**: Visualize model performance.

#### 2. MFCC Data Extraction Model
- **Data Processing**: Initialize a data processing class for extracting MFCC features.
- **MFCC Feature Extraction**: Process patient datasets to extract MFCC features such as mean, standard deviation, etc.

#### 3. Combined MFCC and NLP Features Model
- **Data Preparation**: Load the dataset from Google Drive and split it into training and test sets.
- **Merge MFCC and Text Data**: Combine MFCC data with NLP textual data and assign AD diagnosis labels.
- **Normalize the Final Dataset**: Merge datasets and normalize by dropping non-normalized features.

### Final Dataset Creation and Saving
- **Create DataFrames and Merge Data**: For all models, create separate DataFrames for different features and merge them.
- **Save Processed Data to CSV**: Export the processed data to CSV files for further analysis.

## Data
- Ensure data files like patient datasets, MFCC feature files, and NLP textual data files are correctly placed in Google Drive.
- Follow specific file paths mentioned in the models' scripts.

## Note
- These models are developed for educational and research purposes.
- The performance of the models can vary based on dataset quality and size.


## LineBot interface
### Introduction  

This Brench is created for linebot implementation  
Mainly in file "Linebot", Which includes:  
_1. Linebot interface_  
_2. Data preprocess maintained as a class_  
_3. Model training process maintained as a class_  
_4. Side materials for testing_

###  Build Setup  

_1. Replit_  
_2. Google Run_  

### .env Setting  

_1. OpenAI token_  
_2. LineBot LINE_CHANNEL_ACCESS_TOKEN_ 
_3. LineBot LINE_CHANNEL_SECRET_  

### User Manual  
_1. Adding AD diagnoser as your friend_  
_2. Sending an audio message of a 30sec~1min speech to AD diagnoser(could  be either a description of a picture, or any monologue in English_  
_3. Waiting for response_

![image](https://i.imgur.com/Br1cRps.png)
![image](https://i.imgur.com/M08Eg7T.png)
![image](https://i.imgur.com/C5Onfz2.png)
### Demo video
https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/104049394/0abc9976-7245-4fc7-9743-a16e3f877b35


