import numpy as np
from scipy.fft import fft
from scipy.signal import get_window
from scipy.signal import savgol_filter

def extract_melody(spectrogram, model, window_size=20, step_size=15):
    """
    Extracts melody from a spectrogram using a machine learning model.

    Parameters:
        spectrogram (numpy.ndarray): The input spectrogram.
        model (object): The machine learning model to predict peaks.
        window_size (int, optional): The size of the window for analyzing the spectrogram.
        step_size (int, optional): The step size for moving the analysis window.

    Returns:
        peaks (numpy.ndarray): Array of extracted melody peaks.
    """
    peaks = []

    start_index = 15

    for frame_index in range(len(spectrogram)):
        smoothed_spectrum = savgol_filter(spectrogram[frame_index], window_length=15, polyorder=5)
        
        interpolated_peak = 0
        
        index = start_index
        while index < len(smoothed_spectrum) - 1:  
            if smoothed_spectrum[index] < -25: 
                index += 1
                continue

            if smoothed_spectrum[index - 1] < smoothed_spectrum[index] and smoothed_spectrum[index] > smoothed_spectrum[index + 1]:
                segment = np.zeros(len(smoothed_spectrum)) - 100
                segment[index:index + 15] = spectrogram[frame_index][index:index + 15]
                
                current_peak = np.argmax(segment)

                start_index = current_peak - 5

                #peak_value = spectrogram[frame_index][current_peak]
                #left_value = spectrogram[frame_index][current_peak - 1]
                #right_value = spectrogram[frame_index][current_peak + 1]
                interpolated_peak = current_peak# + 0.5 * (left_value - right_value) / (left_value - 2 * peak_value + right_value)

                break                
            else:
                index += 1

        peaks.append(interpolated_peak)

    return np.array(peaks)

def detectRealpeaks(spectrogram, peak_frequencyBins, peak_magnitudes):
    for i in range(len(peak_frequencyBins)):
        for j in range(len(peak_frequencyBins[i])):
            p = peak_frequencyBins[i][j]
            
            for k in range(p-4, p+4):
                if spectrogram[i][k] > peak_magnitudes[i][j]:
                    peak_magnitudes[i][j] = spectrogram[i][k]
                    peak_frequencyBins[i][j] = k
    
    return peak_frequencyBins, peak_magnitudes

def extract_melody_nn(spectrogram, model, window_size=20, step_size=15):
    """
    Extracts melody from a spectrogram using a machine learning model.

    Parameters:
        spectrogram (numpy.ndarray): The input spectrogram.
        model (object): The machine learning model to predict peaks.
        window_size (int, optional): The size of the window for analyzing the spectrogram.
        step_size (int, optional): The step size for moving the analysis window.

    Returns:
        peaks (numpy.ndarray): Array of extracted melody peaks.
    """
    peaks = np.array([])  # Initialize array to store extracted melody peaks
    for frame_index in range(len(spectrogram)):
        # Smooth the spectrum for the current frame
        smoothed_spectrum = savgol_filter(spectrogram[frame_index], window_length=12, polyorder=5)
        
        index = 10  # Start index for analyzing the spectrum
        while index < len(smoothed_spectrum) - window_size:
            # Extract the segment of interest from the spectrum
            segment = smoothed_spectrum[index: index + window_size]
            segment = np.array([segment])[..., np.newaxis]  # Normalize and reshape segment
            
            # Evaluate the segment using the model
            prediction = model.predict(segment)
            
            # Check if it's a peak
            if np.round(prediction):
                # Get the frequency bin of the peak
                peak_index = index + np.argmax(segment)
                peak_index = peak_index - 5 + np.argmax(spectrogram[frame_index][peak_index - 5: peak_index + 5])
                
                # Interpolate the peak
                peak_value = spectrogram[frame_index][peak_index]
                left_value = spectrogram[frame_index][peak_index - 1]
                right_value = spectrogram[frame_index][peak_index + 1]
                interpolated_peak = peak_index + 0.5 * (left_value - right_value) / (left_value - 2 * peak_value + right_value)
                
                # Append interpolated peak to array and break out of the loop after finding the peak
                peaks = np.append(peaks, interpolated_peak)  
                break
            
            # Move the analysis window
            index += step_size 
        
    return peaks



def stft(signal, sample_rate, window_size=8191, fft_buffer_size=8192, hop_length=2048):
    """
    Compute the spectrogram of an audio signal.

    Parameters:
        signal (numpy.ndarray): The input signal.
        sample_rate (int): The sampling rate of the input signal.
        window_size (int, optional): The size of the analysis window.
        fft_buffer_size (int, optional): The size of the FFT buffer.
        hop_length (int, optional): The hop length between consecutive frames.

    Returns:
        log_magnitude_spectrogram (array_like): Log magnitude spectrogram of the input signal.
    """

    # Generate a Hamming window for windowing the signal
    window = get_window('hamming', window_size)
    window /= np.sum(window)

    # Define the number of frequency bins
    num_frequency_bins = int(1000 * fft_buffer_size / sample_rate)

    # Compute the number of frames
    num_frames = (len(signal) - window_size) // hop_length + 1

    # Extract frames from the signal
    frames = np.lib.stride_tricks.as_strided(signal, shape=(num_frames, window_size), strides=(signal.itemsize * hop_length, signal.itemsize))

    # Compute RMS values
    rms_values = np.sqrt(np.sum(frames**2, axis=1) / window_size)

    # Filter frames based on RMS threshold
    valid_frames = frames[rms_values > 0.002]

    # Normalize valid frames
    max_abs_amplitude = np.max(np.abs(valid_frames))
    normalized_valid_frames = valid_frames / max_abs_amplitude

    # Apply window to all valid frames
    windowed_frames = normalized_valid_frames * window

    # Apply zero-phase windowing to the frames
    fft_buffer = np.zeros((len(windowed_frames), fft_buffer_size),   dtype=signal.dtype)
    fft_buffer[:, :window_size // 2 + 1] = windowed_frames[:, window_size // 2:]
    fft_buffer[:, fft_buffer_size - window_size // 2:] = windowed_frames[:, :window_size // 2]

    # Compute the spectrogram for all frames
    spectrogram = fft(fft_buffer, axis=1)

    # Slice up to 1 kHz (up to num_frequency_bins)
    spectrogram = spectrogram[:, :num_frequency_bins]

    # Compute magnitude spectrum
    magnitude_spectrogram = np.abs(spectrogram)

    # Apply log to the magnitude spectrum
    magnitude_spectrogram[magnitude_spectrogram < np.finfo(float).eps] = np.finfo(float).eps
    log_magnitude_spectrogram = 10 * np.log10(magnitude_spectrogram)

    return log_magnitude_spectrogram