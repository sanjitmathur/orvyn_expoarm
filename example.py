#.\.venv\Scripts\Activate.ps1
#python example.py

import numpy as np
from scipy.signal import butter, filtfilt
from scipy.io import loadmat
import matplotlib.pyplot as plt

def apply_bandpass_filter(signal_data, low_cutoff, high_cutoff, sample_rate, filter_order=4):
    nyquist_frequency = 0.5 * sample_rate
    normalized_low = low_cutoff / nyquist_frequency
    normalized_high = high_cutoff / nyquist_frequency
    filter_b, filter_a = butter(filter_order, [normalized_low, normalized_high], btype='band')
    filtered_data = filtfilt(filter_b, filter_a, signal_data)
    return filtered_data

def calculate_rms_envelope(signal_data, window_size_samples):
    squared_signal = np.power(signal_data, 2)
    averaging_window = np.ones(window_size_samples) / float(window_size_samples)
    valid_rms_envelope = np.sqrt(np.convolve(squared_signal, averaging_window, 'valid'))
    
    padding_amount = (len(signal_data) - len(valid_rms_envelope)) // 2
    full_rms_envelope = np.pad(valid_rms_envelope, (padding_amount, len(signal_data) - len(valid_rms_envelope) - padding_amount), 'edge')
    
    return full_rms_envelope

MATLAB_FILE_PATH = r"C:\Users\bhawn\Downloads\semg+for+basic+hand+movements\Database 1\female_1.mat"
SAMPLE_RATE_HZ = 500
FILTER_LOW_CUTOFF_HZ = 20.0
FILTER_HIGH_CUTOFF_HZ = 240.0
RMS_WINDOW_MILLISECONDS = 50
rms_window_sample_count = int((RMS_WINDOW_MILLISECONDS / 1000) * SAMPLE_RATE_HZ)

matlab_data = loadmat(MATLAB_FILE_PATH)

all_grasp_trials = matlab_data['cyl_ch1']
raw_signal_trial_1 = all_grasp_trials[0, :]

time_axis_seconds = np.linspace(0, len(raw_signal_trial_1) / SAMPLE_RATE_HZ, len(raw_signal_trial_1))

filtered_signal = apply_bandpass_filter(raw_signal_trial_1,  low_cutoff=FILTER_LOW_CUTOFF_HZ, high_cutoff=FILTER_HIGH_CUTOFF_HZ,
sample_rate=SAMPLE_RATE_HZ)

rectified_signal = np.abs(filtered_signal)

rms_flex_envelope = calculate_rms_envelope(rectified_signal, rms_window_sample_count)

figure, (plot1, plot2, plot3) = plt.subplots(3, 1, sharex=True, figsize=(12, 8))
figure.suptitle("sEMG Signal Processing (Dataset ID 313)", fontsize=16)

plot1.plot(time_axis_seconds, raw_signal_trial_1)
plot1.set_title("1. Raw sEMG Signal (male_1.mat, cyl_ch1, Trial 1)")
plot1.set_ylabel("Amplitude (V)")

plot2.plot(time_axis_seconds, rectified_signal)
plot2.set_title("2. Filtered (20-240 Hz) and Rectified Signal")
plot2.set_ylabel("Amplitude (V)")

plot3.plot(time_axis_seconds, rms_flex_envelope, 'r', linewidth=2)
plot3.set_title("3. RMS Envelope")
plot3.set_ylabel("Flex Level (RMS)")
plot3.set_xlabel("Time (s)")

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()