This file will extract the audio clip where only patients are speaking and use the function from **noisereduce** to reduce the background noise of these clips.

It also use the patient information from chat file to produce label (0 as MCI, 1 as AD)

The input files should be put inside folder *./data* relative to this notebook.

The generated output files will be put in ./Audio_Output

* Input files : audio files, corresponding chat files
* Output files : segmentized audio files, one csv file contains patient information and AD, MCI labels
