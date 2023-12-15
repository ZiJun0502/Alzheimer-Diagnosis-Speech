import numpy as np
import csv
from scipy.io import wavfile
from scipy.fftpack import dct
import os
import pandas as pd

### Messages for Daphne:
### 1. All file handlers are named as "file_handler", change it according to the feed from the audio messages generated from line.
###

class mfcc_features():
    def __init__(self, file_handler):
        self.fs, self.wavdata = wavfile.read(file_handler)
        self.num_ceps = 12
        self.frame_len = 25
        self.frame_shift = 10                   # frame shift length (ms)
        self.pre_emphasis_coeff = 0.97          # Pre-emphasis coefficient
        self.K = 512                            # length of DFT
        self.low_frequency = 20                 # We don't use start from 0 Hz because human ear is not able to perceive low frequency signal.
        self.n_filt = 40                        # number of mel-filters (usually between 22-40)
        self.mfcc = 0

    def mfcc_feature_calculation(self):
        frame_len_samples = self.frame_len * self.fs // 1000
        frame_shift_samples = self.frame_shift * self.fs // 1000
        total_frames = int(np.ceil((len(self.wavdata) - frame_len_samples) / float(frame_shift_samples)) + 1)   # total frames will get
        padding_length = int((total_frames - 1) * frame_shift_samples + frame_len_samples - len(self.wavdata))  # how many samples last frame need to pad
        frame_data = np.zeros((total_frames, frame_len_samples))                                                # where we save the frame results
        window_func = np.hamming(frame_len_samples)                                                             # hamming window
        pad_data = np.pad(self.wavdata, (0, padding_length), mode='constant')                                   # pad last frame with zeros
        pad_data = np.append(pad_data[0], pad_data[1:] - self.pre_emphasis_coeff * pad_data[:-1])               # Pre-emphasis
        self.log_fbank = 0

        for i in range(total_frames):
            single_frame = pad_data[i * frame_shift_samples : 
                                    i * frame_shift_samples + frame_len_samples]              # original frame data
            single_frame = single_frame * window_func                                         # add window function
            frame_data[i,:] = single_frame

        freq_domain_data = np.fft.rfft(frame_data, self.K)                                    # DFT
        power_spec = np.absolute(freq_domain_data) ** 2 * (1 / self.K)                        # power spectrum
        high_frequency = self.fs // 2                                                         # if the speech is sampled at f Hz then our upper frequency is limited to 2/f Hz.
        low_frequency_mel = 2595 * np.log10(1 + self.low_frequency / 700)                     # M(f) = 2595*log10(1+f/700)
        high_frequency_mel = 2595 * np.log10(1 + high_frequency / 700)
        mel_points = np.linspace(low_frequency_mel, high_frequency_mel, self.n_filt + 2)      # Make the Mel scale spacing equal.
        hz_points = (700 * (10**(mel_points / 2595) - 1))                                     # convert back to Hz scale.
        bins = np.floor((self.K + 1) * hz_points / self.fs)                                   # round those frequencies to the nearest FFT bin.

        fbank = np.zeros((self.n_filt, int(np.floor(self.K / 2 + 1))))
        for m in range(1, self.n_filt + 1):
            f_m_minus = int(bins[m - 1])   # left point
            f_m = int(bins[m])             # peak point
            f_m_plus = int(bins[m + 1])    # right point
            for k in range(f_m_minus, f_m):
                fbank[m - 1, k] = (k - bins[m - 1]) / (bins[m] - bins[m - 1])
            for k in range(f_m, f_m_plus):
                fbank[m - 1, k] = (bins[m + 1] - k) / (bins[m + 1] - bins[m])
        filter_bank = np.matmul(power_spec,fbank.T)                                 # This is known as fbank feature.
        filter_bank = np.where(filter_bank == 0,np.finfo(float).eps,filter_bank)    # Repalce 0 to a small constant or it will cause problem to log.
        log_fbank = np.log(filter_bank)                                             # We can also use log_fbank = 20*np.log10(filter_bank) to get dB energies.
        self.mfcc = dct(log_fbank, type=2, axis=1, norm="ortho")[:, 1 : (self.num_ceps + 1)] 

    def mfcc_output(self, idx_wav):
        file_handler = f'./{idx_wav}.csv'
        with open(file_handler, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            # Write data to the CSV file
            for row in self.mfcc:
                csv_writer.writerow(row)

if __name__ == "__main__":
    # Input audio file
    MFCC = mfcc_features("/Users/raychang/Desktop/NTHU Courses/Machine Learning/final_project/Alzheimer-Diagnosis-Speech/linebot/Baycrest2103.wav")
    # Calculate the audio's mfcc features
    MFCC.mfcc_feature_calculation()
    # output datafile
    MFCC.mfcc_output("testdoc")


    