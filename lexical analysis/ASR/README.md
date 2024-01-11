## ASR segment of the project
### The segment is composed of three part of coding
1.`Whisper.ipynb`
### Overview
The file is composed of the calling of the wav file in the drive-way, then transformed by the sequence-to-sequence module developed by Open-AI. We only take the text segments of the transformation result and save it as a txt file.
### Github page of Whisper
[Whisper](https://github.com/openai/whisper)
### Approach
![image](https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/106430645/55a60af3-146c-4e29-814c-94237eba2d62)
A Transformer sequence-to-sequence model is trained on various speech processing tasks, including multilingual speech recognition, speech translation, spoken language identification, and voice activity detection. These tasks are jointly represented as a sequence of tokens to be predicted by the decoder, allowing a single model to replace many stages of a traditional speech-processing pipeline. The multitask training format uses a set of special tokens that serve as task specifiers or classification targets.
### Module 
There are five model sizes, four with English-only versions, offering speed and accuracy tradeoffs.
<img width="608" alt="image" src="https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/106430645/ab9b853c-6d6d-4d2b-a29b-854bc6cf6681">

We'll choose the base module in this case because a smaller module will cause translation errors, a bigger module will cause huge running time, and we don't need so much multilanguage.
### Accuracy
The fallowing is the accuracy in different language
![image](https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/106430645/4f081855-480f-4263-8532-cb81ee2947a8)

In the implementation of ASR transformation, English transform is well transformed, but Chinese has almost the wrong answer as we hear.We have done the research on Chinese ASR; the Central Research Academy in Taiwan has some research on it; and NTHU in China as well, but their method only has about 70% accuracy in the transform result.
So, I think if we want to do research on Chinese audio classification, the text part will be stuck on the ASR part.
### Why we choose Whisper
1. Reliability
2. Easy to use in their API
3. Multilanguage support
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
The text result will be store in this folder, we can take a simple look about transform
3.`missing_asr.ipynb`:
Because some of the entries have poor performance on the NLP (ex: empty, extremely high value), we'll specifically pick out the entries and rerun the ASR for them.

