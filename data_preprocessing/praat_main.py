import pandas as pd
import parselmouth
import csv
import os

from feature import *  

directory = 'Ted_left_output'
wav_files = [file for file in os.listdir(directory) if file.endswith('.wav')]

for idx,file_name in enumerate(wav_files):
    print(f'wav_idx={idx},file_name={file_name}')
    file_path = os.path.join(directory, file_name) 
    sound = parselmouth.Sound(file_path)

    # Extract attributes
    intensity_attributes = get_intensity_attributes(sound)[0]
    pitch_attributes = get_pitch_attributes(sound)[0]
    hnr_attributes = get_harmonics_to_noise_ratio_attributes(sound)[0]
    gne_attributes = get_glottal_to_noise_ratio_attributes(sound)[0]
    local_jitter = get_local_jitter(sound)
    local_shimmer = get_local_shimmer(sound)
    spectrum_attributes = get_spectrum_attributes(sound)[0]
    formant_attributes = get_formant_attributes(sound)[0]

    # Organize attributes into a DataFrame
    attributes = {
        **intensity_attributes,
        **pitch_attributes,
        **hnr_attributes,
        **gne_attributes,
        'local_jitter': local_jitter,
        'local_shimmer': local_shimmer,
        **spectrum_attributes,
        **formant_attributes,
        # 'sound_filepath': file_path
    }
    df = pd.DataFrame(attributes, index=[0])

    # Create a CSV file for each WAV file
    base_name = os.path.splitext(file_name)[0]
    output_file = f'{base_name}.csv'
    df.to_csv(output_file, index=False)
