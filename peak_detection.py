import numpy as np
from scipy.signal import savgol_filter

def detect_peaks(spectrogram, sampling_rate, fft_size=8192):
    """
    Detect peaks in the spectrogram.

    Parameters:
    spectrogram (array_like): Spectrogram of the audio signal.
    sampling_rate (int): Sampling frequency of the audio signal.
    fft_size (int): Size of the FFT.
    cutoff_frequency (int): Cutoff frequency.

    Returns:
    peak_frequencies (list): List of peak frequencies.
    peak_magnitudes (list): List of peak magnitudes.
    """

    peak_frequencies = []
    peak_magnitudes = []

    for frame_index in range(len(spectrogram)):
        smoothed_spectrum = savgol_filter(spectrogram[frame_index], window_length=15, polyorder=5)
        
        current_peak_frequencies = []
        current_peak_magnitudes = []
        
        index = 15
        while index < len(smoothed_spectrum) - 1:
            if len(current_peak_frequencies) == 4:
                break
                    
            if smoothed_spectrum[index] < -25: 
                index += 1
                continue

            if smoothed_spectrum[index - 1] < smoothed_spectrum[index] and smoothed_spectrum[index] > smoothed_spectrum[index + 1]:
                segment = np.zeros(len(smoothed_spectrum)) - 100
                segment[index:index + 15] = smoothed_spectrum[index:index + 15]
                
                current_peak_frequencies.append(np.argmax(segment) * sampling_rate / fft_size)
                current_peak_magnitudes.append(smoothed_spectrum[np.argmax(segment)])
                
                index = np.argmax(segment) + 10
                
            else:
                index += 1

        peak_frequencies.append(current_peak_frequencies)
        peak_magnitudes.append(current_peak_magnitudes)

    return peak_frequencies, peak_magnitudes
