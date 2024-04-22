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

## ASR transformation
Before we start the lexical analysis of the AD diagnosis, we should use the ASR to transform the audio datasets into text files so we can use NLP to analyze the lexical features. The ASR model we use is Whisper, developed by OpenAI. We can use the following code to transform the audio data:
```bush
!pip install whisper
!pip install git+https://github.com/openai/whisper.git
```
## Lexical Analysis
After receiving the text file from ASR processing, you can extract the lexical analysis function by function using the following engines:
### 1. Stanford CoreNLP (using the parser tree package from the server):

Start the local server by keying following code in your CMD:
```bush
$cd "C:\stanford-corenlp-4.5.5\stanford-corenlp-4.5.5"
$java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000 -annotators tokenize,ssplit,pos,lemma,ner,parse,dcoref
```
If you want to run Stanford coreNLP server on Colab, you need to implement the following code:
```bush
# Install stanza; note that the prefix "!" is not needed if you are running in a terminal
!pip install stanza
# Import stanza
import stanza
# Download the Stanford CoreNLP package with Stanza's installation command
# This'll take several minutes, depending on the network speed
corenlp_dir = './corenlp'
stanza.install_corenlp(dir=corenlp_dir)
# Set the CORENLP_HOME environment variable to point to the installation location
import os
os.environ["CORENLP_HOME"] = corenlp_dir
# Examine the CoreNLP installation folder to make sure the installation is successful
!ls $CORENLP_HOME
# Import client module
from stanza.server import CoreNLPClient
# Construct a CoreNLPClient with some basic annotators, a memory allocation of 4GB, and port number 9001
client = CoreNLPClient(
    annotators=['tokenize', 'ssplit', 'pos', 'lemma'],
    memory='1000T',
    timeout=1e32,
    endpoint='http://localhost:4015',
    max_char_length=1e24,
    thread=100,
    be_quiet=True)
print(client)
# Start the background server and wait for some time
# Note that in practice this is totally optional, as by default the server will be started when the first annotation is performed
client.start()
import time; time.sleep(10)
# Print background processes and look for java
# You should be able to see a StanfordCoreNLPServer java process running in the background
!ps -o pid,cmd | grep java
```
End the server with the following code:
```bush
client.stop()
time.sleep(10)
!ps -o pid,cmd | grep java
```
### 2.Stanza: 

If you want to use the optimal version of StanfordNLP -- stanza
```bush
!pip install stanza
stanza.download('en')
# Loading pipline from stanza 
nlp = stanza.Pipeline('en', processors='tokenize,mwt,pos,lemma,depparse')
```
### 3.NLTK:

If you want to use NLTK:
```bush
!pip install nltk
import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag
```
### 4.SpaCy:

If you want to use SpaCy:
```bush
!pip install spacy
!python -m spacy download en_core_web_sm
!pip install scispacy
!pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.3/en_core_sci_sm-0.5.3.tar.gz
!pip install textacy
!pip install negspacy
!python -m spacy validate
!python -m spacy download en_core_web_sm
```
If you want to silence splitting:
```bush
!pip install pydub
from pydub import AudioSegment
from pydub.silence import split_on_silence
```
We can use these engines to extract following features:

1.POS tagging

2.Syntactic complexity(Including basic and advanced part)

3.Vocabulary richness

4.Negation analysis

5.Name entity recognized

6.Emoji analysis

7.Psycholinguistics

8.Repetitiveness

9.Silence splitting

## Prediction Model Using MFCC and NLP Features

### Overview
This comprehensive guide covers three Alzheimer's Disease (AD) prediction models, focusing on machine learning techniques, MFCC data extraction, and a combination of MFCC and NLP features. These models aim to predict AD using various classifiers and data sources, including patient and normal datasets.

### Requirements
- Python 3.x
- Libraries: pandas, numpy, sklearn, matplotlib, csv
- Google Colab for drive mounting and processing

### Installation
1. Install Python 3 and required libraries using pip.
2. Use Google Colab for executing scripts and accessing Google Drive.

### Usage
#### Common Steps for All Models
- **Connect to Google Drive**: Use Google Colab to mount your Google Drive for data access.
- **Import Required Packages**: Import Python packages like pandas, numpy, sklearn, os, etc.

#### Model-Specific Steps
##### 1. Machine Learning Model for AD Prediction
- **Data Preparation**: Load the dataset from Google Drive and split it into training and test sets.
- **Feature Selection using Lasso**: Perform feature selection using Lasso regression.
- **Model Training and Evaluation**: Train models like KNN, SVM, Decision Tree, etc., and evaluate using metrics like accuracy, MCC, and F1-score.
- **Results Visualization**: Visualize model performance.

##### 2. MFCC Data Extraction Model
- **Data Processing**: Initialize a data processing class for extracting MFCC features.
- **MFCC Feature Extraction**: Process patient datasets to extract MFCC features such as mean, standard deviation, etc.

##### 3. Combined MFCC and NLP Features Model
- **Data Preparation**: Load the dataset from Google Drive and split it into training and test sets.
- **Merge MFCC and Text Data**: Combine MFCC data with NLP textual data and assign AD diagnosis labels.
- **Normalize the Final Dataset**: Merge datasets and normalize by dropping non-normalized features.

#### Final Dataset Creation and Saving
- **Create DataFrames and Merge Data**: For all models, create separate DataFrames for different features and merge them.
- **Save Processed Data to CSV**: Export the processed data to CSV files for further analysis.

### Data
- Ensure data files like patient datasets, MFCC feature files, and NLP textual data files are correctly placed in Google Drive.
- Follow specific file paths mentioned in the models' scripts.

### Note
- These models are developed for educational and research purposes.
- The performance of the models can vary based on dataset quality and size.


## Linebot Interface
#### Introduction  

This Brench is created for linebot implementation  
Mainly in file "Linebot", Which includes:  
1. Linebot interface_  
2. Data preprocess maintained as a class_  
3. Model training process maintained as a class_  
4. Side materials for testing_

####  Build Setup  

1. Replit 
2. Google Run 

#### .env Setting  

1. OpenAI token  
2. LineBot LINE_CHANNEL_ACCESS_TOKEN 
3. LineBot LINE_CHANNEL_SECRET  

#### User Manual  
1. Adding AD diagnoser as your friend  
2. Sending an audio message of a 30sec~1min speech to AD diagnoser(could  be either a description of a picture, or any monologue in English  
3. Waiting for response

![image](https://i.imgur.com/Br1cRps.png)
![image](https://i.imgur.com/M08Eg7T.png)
![image](https://i.imgur.com/C5Onfz2.png)
#### Demo video
https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/104049394/0abc9976-7245-4fc7-9743-a16e3f877b35


