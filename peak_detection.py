import numpy as np
from scipy.signal import savgol_filter

def estimate_peaks(spectrogram):
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

    peak_frequencyBins = []
    peak_magnitudes = []

    for frame_index in range(len(spectrogram)):
        smoothed_spectrum = savgol_filter(spectrogram[frame_index], window_length=15, polyorder=5)
        
        current_peak_frequencyBins = []
        current_peak_magnitudes = []
        
        index = 15
        while index < len(smoothed_spectrum) - 1:
            if len(current_peak_frequencyBins) == 4:
                break
                    
            if smoothed_spectrum[index] < -25: 
                index += 1
                continue

            if smoothed_spectrum[index - 1] < smoothed_spectrum[index] and smoothed_spectrum[index] > smoothed_spectrum[index + 1]:
                segment = np.zeros(len(smoothed_spectrum)) - 100
                segment[index:index + 15] = smoothed_spectrum[index:index + 15]
                
                current_peak_frequencyBins.append(np.argmax(segment))
                current_peak_magnitudes.append(smoothed_spectrum[np.argmax(segment)])
                
                index = np.argmax(segment) + 10
                
            else:
                index += 1

        peak_frequencyBins.append(current_peak_frequencyBins)
        peak_magnitudes.append(current_peak_magnitudes)

    return np.array(peak_frequencyBins), np.array(peak_magnitudes)

def detectRealpeaks(spectrogram, peak_frequencyBins, peak_magnitudes):
    for i in range(len(peak_frequencyBins)):
        for j in range(len(peak_frequencyBins[i])):
            p = peak_frequencyBins[i][j]
            
            for k in range(p-4, p+4):
                if spectrogram[i][k] > peak_magnitudes[i][j]:
                    peak_magnitudes[i][j] = spectrogram[i][k]
                    peak_frequencyBins[i][j] = k
    
    return peak_frequencyBins, peak_magnitudes

def peakInterpolation(spectrogram, peak_frequencyBins, peak_magnitudes):
    for i in range(len(peak_frequencyBins)):
        for j in range(len(peak_frequencyBins[i])):
            val = spectrogram[i][peak_frequencyBins[i][j]]
            lval = spectrogram[i][peak_frequencyBins[i][j] - 1]
            rval = spectrogram[i][peak_frequencyBins[i][j] + 1]
            
            currentPeakBin = peak_frequencyBins[i][j] + 0.5 * (lval - rval) / (lval - 2 * val + rval)
            currentPeakMagnitude = val - 0.25 * (lval - rval) * (currentPeakBin - peak_frequencyBins[i][j])
            
            peak_magnitudes[i][j] = currentPeakMagnitude
            peak_frequencyBins[i][j] = currentPeakBin

    return peak_frequencyBins, peak_magnitudes
