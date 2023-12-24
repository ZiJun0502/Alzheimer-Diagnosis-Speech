## Audio Collecting and Processing Notebook
`collect_data.ipynb`
### Overview
This notebook is specifically crafted for the extraction of audio clips featuring only patients' speech. It leverages the noisereduce library to efficiently diminish background noise in these clips.

Furthermore, the notebook integrates patient information sourced from chat files to generate labels, with 0 denoting Mild Cognitive Impairment (MCI) and 1 representing Alzheimer's Disease (AD).

### Usage
1. **Input Files Placement:**
Ensure that the input files, encompassing audio files and their corresponding chat files, are positioned inside the *./data* directory relative to this notebook.

2. **Output Files Location:**
The resulting output files will be saved in the ./Audio_Output directory.

### File Details
#### Input Files:
* Audio files
* Corresponding chat files
#### Output Files:

* Segmentized audio files
* A single CSV file containing patient information and labels (AD, MCI)

### Other Preprocessing Details
1. Channel Averaging:
If the audio file consists of more than one channel, the preprocessing script takes the average of all channels and combines them into a single channel. This ensures uniformity in audio processing.

2. Normalization to -20 dBFS:
To address variations in volume levels, particularly in cases where audio from the dementia bank might be very low in volume, all audio files undergo normalization. The normalization process sets the audio to a standard level of -20 dBFS, ensuring consistent and optimal audio quality.
