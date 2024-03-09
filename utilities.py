import numpy as np
from scipy.fft import fft
from scipy.signal import get_window

def peak_interpolation(spectrogram, peaks):
    """
    Perform peak interpolation on a spectrogram.

    This function interpolates the peak frequencies of a spectrogram using quadratic interpolation.

    Parameters:
        spectrogram (numpy.ndarray): The spectrogram.
        peaks (numpy.ndarray): The peaks to be interpolated.

    Returns:
        numpy.ndarray: An array containing the interpolated peak frequencies.
    """
    # Obtain magnitudes of peaks and adjacent bins
    magnitudes = spectrogram[np.arange(peaks.size), peaks]
    l_magnitudes = spectrogram[np.arange(peaks.size), peaks - 1]
    r_magnitudes = spectrogram[np.arange(peaks.size), peaks + 1]
    
    # Perform peak interpolation using quadratic interpolation formula
    interpolated_peaks = peaks + 0.5 * (l_magnitudes - r_magnitudes) / (l_magnitudes - 2 * magnitudes + r_magnitudes)
    
    return interpolated_peaks


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
    valid_frames = frames[rms_values > 0.1]

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