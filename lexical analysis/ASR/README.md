## ASR segment of the project
`Whisper.ipynb`
### Overview
The file is composed of the calling of the wav file in the drive-way, then transformed by the sequence-to-sequence module developed by Open-AI. We only take the text segments of the transformation result and save it as a txt file.
### Github page of Whisper
[Whisper](https://github.com/openai/whisper)
### Introduction to Whisper
#### Approach
![image](https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/106430645/55a60af3-146c-4e29-814c-94237eba2d62)
A Transformer sequence-to-sequence model is trained on various speech processing tasks, including multilingual speech recognition, speech translation, spoken language identification, and voice activity detection. These tasks are jointly represented as a sequence of tokens to be predicted by the decoder, allowing a single model to replace many stages of a traditional speech-processing pipeline. The multitask training format uses a set of special tokens that serve as task specifiers or classification targets.
### Accuracy
