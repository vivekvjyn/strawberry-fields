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

    index = 15
    for frame_index in range(len(spectrogram)):
        smoothed_spectrum = savgol_filter(spectrogram[frame_index], window_length=15, polyorder=5)
        
        current_peak_frequencyBin = 0
        current_peak_magnitude = 0
        
        
        while index < len(smoothed_spectrum) - 1:                    
            if smoothed_spectrum[index] < -25: 
                index += 1
                continue

            if smoothed_spectrum[index - 1] < smoothed_spectrum[index] and smoothed_spectrum[index] > smoothed_spectrum[index + 1]:
                segment = np.zeros(len(smoothed_spectrum)) - 100
                segment[index:index + 15] = smoothed_spectrum[index:index + 15]
                
                current_peak_frequencyBin = np.argmax(segment)
                current_peak_magnitude = smoothed_spectrum[np.argmax(segment)]
                
                index = current_peak_frequencyBin - 10

                break
                
            else:
                index += 1

        peak_frequencyBins.append(current_peak_frequencyBin)
        peak_magnitudes.append(current_peak_magnitude)

    return np.array(peak_frequencyBins), np.array(peak_magnitudes)

def detectRealpeaks(spectrogram, peak_frequencyBins, peak_magnitudes):
    for i in range(len(peak_frequencyBins)):
        p = peak_frequencyBins[i]
            
        for k in range(p-2, p+2):
            if spectrogram[i][k] > peak_magnitudes[i]:
                peak_magnitudes[i] = spectrogram[i][k]
                peak_frequencyBins[i] = k
    
    return peak_frequencyBins, peak_magnitudes

def peakInterpolation(spectrogram, peak_frequencyBins, peak_magnitudes):
    for i in range(len(peak_frequencyBins)):
        val = spectrogram[i][peak_frequencyBins[i]]
        lval = spectrogram[i][peak_frequencyBins[i] - 1]
        rval = spectrogram[i][peak_frequencyBins[i] + 1]
        
        currentPeakBin = peak_frequencyBins[i] + 0.5 * (lval - rval) / (lval - 2 * val + rval)
        currentPeakMagnitude = val - 0.25 * (lval - rval) * (currentPeakBin - peak_frequencyBins[i])
        
        peak_magnitudes[i] = currentPeakMagnitude
        peak_frequencyBins[i] = currentPeakBin

    return peak_frequencyBins, peak_magnitudes
