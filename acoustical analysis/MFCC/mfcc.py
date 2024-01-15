# 1. Frame the signal into short frames.
import numpy as np
import csv
from scipy.io import wavfile
import os

# Define the directory containing your WAV files
directory = './wav'

# Get a list of all WAV files in the directory
wav_files = [file for file in os.listdir(directory) if file.endswith('.wav')]


# Process each WAV file
for idx_wav, file_name in enumerate(wav_files, start=1):
    #fs:refers to the number of samples of audio carried per second, measured in Hertz (Hz). It indicates how frequently the audio signal is sampled or measured per unit of time. For instance, a sampling rate of 44100 Hz means that 44100 samples of audio are taken every second to represent the continuous audio signal digitally.
    #wavdata:contains the amplitude values of the audio signal sampled at the specified sampling rate (in Hz).
    fs, wavdata = wavfile.read(os.path.join(directory, file_name))  # Read the WAV file

    frame_len = 25 # each frame length (ms)
    frame_shift = 10 # frame shift length (ms)
    frame_len_samples = frame_len*fs//1000 # each frame length (samples)
    frame_shift_samples = frame_shift*fs//1000 # frame shifte length (samples)
    total_frames = int(np.ceil((len(wavdata) - frame_len_samples)/float(frame_shift_samples)) + 1) # total frames will get
    padding_length = int((total_frames-1)*frame_shift_samples + frame_len_samples - len(wavdata)) # how many samples last frame need to pad

    pad_data = np.pad(wavdata,(0,padding_length),mode='constant') # pad last frame with zeros
    """ when we frame the signal, usually we do Pre-emphasis first to amplify high frequency signals.
        Pre-emphasis function:
            y(n) = x(x)-a*x(x-1)  
        The reason why we do Pre-emphasis please watch reference: https://zhuanlan.zhihu.com/p/34798429
        Also, we often add a window function to the frame to reduce signal discontinuity at the beginning and end of the frame.
        There are many window functions, we use hamming window here as an example.
    """
    frame_data = np.zeros((total_frames,frame_len_samples)) # where we save the frame results
    pre_emphasis_coeff = 0.97 # Pre-emphasis coefficient
    window_func = np.hamming(frame_len_samples) # hamming window
    pad_data = np.append(pad_data[0],pad_data[1:]-pre_emphasis_coeff*pad_data[:-1]) # Pre-emphasis

    for i in range(total_frames):
        single_frame = pad_data[i*frame_shift_samples:i*frame_shift_samples+frame_len_samples] # original frame data
        single_frame = single_frame * window_func # add window function
        frame_data[i,:] = single_frame

    """ 2. For each frame calculate the periodogram estimate of the power spectrum.
        To transform the frame data from time-domain to frequency-domain we take the Discrete Fourier Transform (DFT) of the frame, 
        by perform the following function:
    """
    from IPython.display import Image
    # Image("./img/DFT.png")

    """ where si(n) is the frame data and h(n) is the window function, K is the length of DFT (usually 256 or 512).
        The periodogram-based power spectral estimate for the speech frame si(n) is given by:
    """
    # Image("./img/power.png")

    K = 512 # length of DFT
    freq_domain_data = np.fft.rfft(frame_data,K) # DFT
    power_spec = np.absolute(freq_domain_data) ** 2 * (1/K) # power spectrum

    """ 3. Apply the mel filterbank to the power spectrum, sum the energy in each filter.
        The Mel scale relates perceived frequency, or pitch, of a pure tone to its actual measured frequency. 
        Humans are much better at discerning small changes in pitch at low frequencies than they are at high frequencies. 
        Incorporating this scale makes our features match more closely what humans hear.
        The formula for converting from frequency to Mel scale is:
            M(f) = 2595*log10(1+f/700)
        And formula for converting from Mel scale to frequency is:
            F(m) = 700*(10**(m/2595)-1)
    """
    low_frequency = 20 # We don't use start from 0 Hz because human ear is not able to perceive low frequency signal.
    high_frequency = fs//2 # if the speech is sampled at f Hz then our upper frequency is limited to 2/f Hz.
    low_frequency_mel = 2595 * np.log10(1 + low_frequency / 700)
    high_frequency_mel = 2595 * np.log10(1 + high_frequency / 700)
    n_filt = 40 # number of mel-filters (usually between 22-40)
    mel_points = np.linspace(low_frequency_mel, high_frequency_mel, n_filt + 2) # Make the Mel scale spacing equal.
    hz_points = (700 * (10**(mel_points / 2595) - 1)) # convert back to Hz scale.
    bins = np.floor((K + 1) * hz_points / fs) # round those frequencies to the nearest FFT bin.

    """Now we create our filterbanks. 
        The first filterbank will start at the first point, reach its peak at the second point, then return to zero at the 3rd point. 
        The second filterbank will start at the 2nd point, reach its max at the 3rd, then be zero at the 4th etc. 
        A formula for calculating these is as follows:
    """
    # Image("./img/fbank.png")

    """The filterbanks are triangle filters, they should look like above figure:
    """
    # Image("./img/mel_tri.png")

    fbank = np.zeros((n_filt, int(np.floor(K / 2 + 1))))
    for m in range(1, n_filt + 1):
        f_m_minus = int(bins[m - 1])   # left point
        f_m = int(bins[m])             # peak point
        f_m_plus = int(bins[m + 1])    # right point

        for k in range(f_m_minus, f_m):
            fbank[m - 1, k] = (k - bins[m - 1]) / (bins[m] - bins[m - 1])
        for k in range(f_m, f_m_plus):
            fbank[m - 1, k] = (bins[m + 1] - k) / (bins[m + 1] - bins[m])
    filter_bank = np.matmul(power_spec,fbank.T) # This is known as fbank feature.
    filter_bank = np.where(filter_bank == 0,np.finfo(float).eps,filter_bank) # Repalce 0 to a small constant or it will cause problem to log.
    """4. Take the logarithm of all filterbank energies.
    """
    log_fbank = np.log(filter_bank) # We can also use log_fbank = 20*np.log10(filter_bank) to get dB energies.

    """ 5. Take the DCT of the log filterbank energies.
        6. Keep DCT coefficients 2-13, discard the rest.
    """
    from scipy.fftpack import dct
    num_ceps = 12 # MFCC feature dims, usually between 2-13.
    # feature from other dims are dropped beacuse they represent rapid changes in filter bank coefficients and they are not helpful for speech models.
    mfcc = dct(log_fbank, type=2, axis=1, norm="ortho")[:, 1 : (num_ceps + 1)] 

    # Create a CSV file with all flattened MFCCs
    base_name = os.path.splitext(file_name)[0]  # Extracting the base name of the WAV file
    output_file = f'{base_name}.csv'  # Using the base name for the CSV file
    with open(output_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(mfcc)

