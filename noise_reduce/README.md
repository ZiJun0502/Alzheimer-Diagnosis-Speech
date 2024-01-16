## Denoise: preprocess through the accoustic features
We take f03.wav patient audio as an example and implement different denoise methods on the audio. Because we can't assure which method is better in MFCC, Pratt extracts features, so we choose the NR library in general.
We measure the noise using the signal-to-noise ratio (SNR), and the formula is as follows:

<img width="178" alt="image" src="https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/106430645/4cf061ee-b60b-44ad-8f70-3da7f82a2693">

![image](https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/106430645/6c8f902d-03eb-4f0d-b990-d7caf3687214)

![image](https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/106430645/c79e8220-cf8f-4bb1-9271-2e04df60c748)

![image](https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/106430645/ac4ec29b-1716-46b5-a4a5-2c5e1d9a7bae)

![image](https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/106430645/dd5369ed-28be-44b2-8434-38851aa7ca88)

![image](https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/106430645/5cd05d59-ba2f-44d9-b5d5-4ef057c72f43)

![image](https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/106430645/dd3d3258-5623-44be-baaf-4c4c1a10fd21)

![image](https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/106430645/870fe710-afda-4d8b-a9d7-bdbfe9ffd02b)

![image](https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/106430645/bfad46b9-cbee-4af1-81be-cd128c8f687e)

![image](https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/106430645/146d9e09-4dbb-4ead-8cb0-87ba74f65d9d)

![image](https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/106430645/82200d0d-0ded-427d-a2b9-6dbfd63cf787)

![image](https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/106430645/3db9ebfe-ce25-484d-8d80-494ab93ca5d8)

![image](https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/106430645/d39548d3-0e8e-426e-9203-f6b97c3ca213)

![image](https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/106430645/28d4efa2-6847-4679-88c5-e24ebe2e190d)

![image](https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/106430645/8dbcdb0d-11f6-4edf-9918-3cf703a8a65f)

![image](https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/106430645/9bda9b73-54e1-4c8d-a08f-8335240844af)

![image](https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/106430645/0ac1aa0d-84a3-443b-a7a4-3ea1bf9c2318)

![image](https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/106430645/ce801071-5a52-4540-89e5-7de955a2d037)

The final result will be as graph:

![image](https://github.com/ZiJun0502/Alzheimer-Diagnosis-Speech/assets/106430645/2f1010af-3e04-4a62-a600-fc813a7b7fd4)

