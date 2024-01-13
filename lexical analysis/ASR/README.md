## ASR segment of the project: The bridge from audio to lexical analysis
### There are three parts of the ASR process

1.`Whisper.ipynb`
### Overview
The file is composed of the calling of the wav file in the drive-way, then transformed by the sequence-to-sequence module developed by Open-AI. We only take the text segments of the transformation result and save it as a txt file.
### page of Whisper
[Whisper github page](https://github.com/openai/whisper)
[Whisper website](https://openai.com/research/whisper)
### Approach
![image](https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/106430645/55a60af3-146c-4e29-814c-94237eba2d62)
In Open-AI github have a detail description, but we will give brief introduction about it, we will intrduct it by the picture in above.

#### (1) training datasets:
The left-right side is the multilingual and multitask supervised data collected from the web. dataset to train the ASR model; the total time length of it is about 680k hours. The reason why it is called a multi-taking dataset is that it includes English audio, another language different from English translated into English, another language translated into the original language, and non-vocal audio in four parts, as shown below. 
![image](https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/106430645/be6433c0-84f0-43f8-9309-db6c4848db09)

The developed group has done specific optimal processing on the non-English translation by supervised SOTA on CoVoST2.
#### (2) training:
![image](https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/106430645/69648582-6180-49a2-9456-8f4c289e006f)

Its training process is on the right, mainly sequence-to-sequence learning. The sequence-to-sequence model is a general term for a type of technology that converts sequences into sequences. Regarding sequence-to-sequence, it is mainly composed of two RNNs: encoder and decoder. You can imagine that encoding is equivalent to processing input data. We feed it data and denoise it through feature engineering (or attention, or image compression processing, etc.), and then output through the decoder.

We can simply think that the sentence transformation depends on the previous words in the text, so if we have the sequence node to transform the sentence by the position it is in, we can perfectly solve the problem. Below is a RNN module built into a sequence transform:

![image](https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/106430645/d620fd13-145e-4666-b50b-e0a4766b2654)


But there is a problem that occurs with the RNN sequence module: if we want to transform the sentence into more words than input, we need to build another RNN sequence module to transform the output into a longer sentence. The first module will be named encoder; it encodes the sentence into the feature vector, and another RNN module reconstructs the feature vector by decoding. The module is as below:

![image](https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/106430645/2198e01e-2d2f-4215-9e4f-02dc658a16ba)


We can think of the process as the PCA process we did in Project 4. First,  we reduced the dimension into a dimension input and used the dimension extract to reconstruct the original data.

![image](https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/106430645/12511923-2cd9-4638-ab8a-16a51e0bc156)


### Language Module 
There are five model sizes, four with English-only versions, offering speed and accuracy tradeoffs.
<img width="608" alt="image" src="https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/106430645/ab9b853c-6d6d-4d2b-a29b-854bc6cf6681">

We chose the base module in this case because a smaller module will cause translation errors, a bigger module will cause huge running time, and we don't need so much multilanguage.
### Accuracy
The fallowing is the accuracy in different language

![image](https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/106430645/4f081855-480f-4263-8532-cb81ee2947a8)

![image](https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/106430645/c1f6ad52-39ae-418e-b928-19c6b6883c5d)

In the implementation of ASR transformation, English transform is well transformed, but Chinese has almost the wrong answer as we hear.We have done the research on Chinese ASR; the Central Research Academy in Taiwan has some research on it; and NTHU in China as well, but their method only has about 70% accuracy in the transform result.
So, I think if we want to do research on Chinese audio classification, the text part will be stuck on the ASR part.
### Why we choose Whisper
(1) Reliability
(2) Easy to use in their function call
(3) Multilanguage support
(4) Open-source
### The disadvantage of Whisper
Because Whisper is a sequence-to-sequence module, the average running time will be huge.
On the other hand, Whisper is only supported in CPU computation and programming in the Python language, both of which slow the processing time while you execute it. Therefore, the version proposed to speed up processing starts appearing.
### Faster version of Whisper
[High-performance GPGPU inference of OpenAI's Whisper automatic speech recognition (ASR) model](https://github.com/Const-me/Whisper)

Using cpython instead of python can run on a Nvidia GPU; the faster modification version to use Whisper.
### The method we used in our Line bot
Because linebots can use GPUs,  we can't use the modified version of whisper. It will be extremely slow for us to run a minute of audio to have the classify result, so we directly call the API from Open-AI.
### The blurry words in patient data
The first question we will ask is whether all of the blurry words spoken by the patient will be translated; if the words are being translated to a proper word, then we can't recognize the blurry words in the natural language process.
The answer is that Whisper will translate the blurry word into a comma, or emm, but there isn't a constant form for these blurry words, so it's the barrier to recognizing the specific term for punction in nature language processing.

2.`ASR result`:
The text result will be store in this folder, we can take a simple look about transform, we can simply see that Chinese ASR text file has several mistakes, English ASR transform result has some utf-8 code(maybe blurry words), will cause error on NLP.

3.`missing_asr.ipynb`:
Because some of the entries have poor performance on the NLP (ex: empty, extremely high value), we'll specifically pick out the entries and rerun the ASR for them.
The fallowing figure is the extremely high value in the dataset, we'll need to double check tje accuracy of the ASR result.

![螢幕擷取畫面 2024-01-12 112617](https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/106430645/44d9afc0-b3dd-452b-a32b-82b21a5eb568)


