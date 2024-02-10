import math
import numpy as np
from scipy.signal import get_window
from scipy.fft import fft

def compute_spectrogram(signal, sample_rate, window_size=8191, fft_buffer_size=8192, hop_length=2048):
    """
    Compute the spectrogram of an audio signal.

    Parameters:
    signal (array_like): The input signal.
    sample_rate (int): The sampling rate of the input signal.
    window_size (int, optional): The size of the analysis window.
    fft_buffer_size (int, optional): The size of the FFT buffer.
    hop_length (int, optional): The hop length between consecutive frames.

    Returns:
    spectrogram (array_like): Spectrogram of the input signal.
    """

    # Compute relevant parameters
    half_window_plus_one = (window_size + 1) // 2
    half_window = window_size // 2

    # Generate a Hamming window for windowing the signal
    window = get_window('hamming', window_size)
    window /= sum(window)

    # Define upper bound for relevant frequencies
    cutoff_frequency = int(1000 * fft_buffer_size / sample_rate)

    # Initialize an empty array for the spectrogram
    spectrogram = []
    
    # Initialize frame index
    frame_index = 0

    # Iterate through each frame
    while frame_index < len(signal) - window_size:
        # Extract the current frame from the audio
        frame = signal[frame_index: frame_index + window_size]
        
        # Compute the root mean square (RMS) value of the current frame
        rms_value = np.sqrt(np.dot(frame, frame) / window_size)
        
        # Discard frames with very low RMS for the spectrogram
        if rms_value > 0.1:
            # Normalize the frame
            frame = frame / np.max(abs(frame))
            frame = frame * window

            # Apply zero-phase windowing to the frame
            fft_buffer = np.zeros(fft_buffer_size)
            fft_buffer[:half_window_plus_one] = frame[half_window:] 
            fft_buffer[fft_buffer_size - half_window:] = frame[:half_window]

            # Compute the log magnitude spectrum of the current frame
            spectrum = fft(fft_buffer)
            magnitude_spectrum = abs(spectrum)
            magnitude_spectrum[magnitude_spectrum < np.finfo(float).eps] = np.finfo(float).eps
            log_magnitude_spectrum = 10 * np.log10(magnitude_spectrum)

            # Append the log magnitude spectrum to the spectrogram
            spectrogram.append(log_magnitude_spectrum[:cutoff_frequency])

        # Move to the next frame
        frame_index += hop_length

    return np.array(spectrogram)