import math
import numpy as np
import scipy.fft
import scipy.signal
import librosa

def dtw(collection, x, frame_length, hop_length):
    """
    Performs Dynamic Time Warping (DTW) matching between a given time series and a collection of time series data.

    Parameters:
        collection (pymongo.collection.Collection): MongoDB collection containing time series data.
        x (numpy.ndarray): Input time series data for matching.
        frame_length (int): Length of the frames (subsequences) for DTW matching.
        hop_length (int): Number of samples between each frame.

    Returns:
        results (list): Top matching documents from the collection based on DTW matching.

    """
    min_costs = [np.inf, np.inf, np.inf, np.inf]
    results = [None, None, None, None]

    for document in collection.find():
        # Extract pitch vector from document
        y = np.array(document["vector"])

        cost = np.inf

        # Iterate over the pitch vector with a sliding window approach
        l = 0
        while l < len(y) - frame_length:
            y_sub = y[l: l + frame_length]
            y_sub = y_sub - np.mean(y_sub)

            # Compute DTW between input and subsequence and update minimum cost
            D, wp = librosa.sequence.dtw(x, y_sub, subseq=True, global_constraints=True, band_rad=0.1)
            cost = min(D[-1, -1], cost)

            l += hop_length

        # Update top matching documents if the current cost is lower than any of the existing minimum costs
        for i in range(len(min_costs)):
            if cost < min_costs[i]:
                min_costs.insert(i, cost)
                min_costs = min_costs[:4]

                results.insert(i, document)
                results = results[:4]
                break
        
    return results

def find_peaks(S, onsets, sr, fft_size):
    """
    Identify peaks in each frame of the Short-Time Fourier Transform (STFT) representation of a signal.

    Parameters:
        S (np.ndarray): Spectrogram represented as a 2D array of complex values.
        onsets (np.ndarray): Indices of frames where onsets are detected due to low root-mean-square (rms) value.
        sr (int): Sample rate of the audio signal.
        fft_size (int): Size of the Fast Fourier Transform (FFT) window.

    Returns:
        peaks (np.ndarray): Peaks identified in each frame of the STFT.

    This function iterates through each frame of the STFT representation of the signal,
    filters it, and identifies the first significant peak. The starting frequency of the
    peak search is initialized based on a specific note (e.g., 'E2'). If the frame index
    corresponds to an onset, the starting frequency resets to 'E2' due to missing frames
    caused by low rms value. The identified peaks are returned as an array.
    """
    # Parameters
    frame_length = 15
    thresh = -25

    # Starting bin index for peak search
    kmin = int(librosa.note_to_hz('E2') / (sr / fft_size))

    # Iterate through each frame of the STFT
    peaks = []
    for l in range(len(S)):
        # Apply Savitzky-Golay filter for smoothing
        y = scipy.signal.savgol_filter(S[l], window_length=15, polyorder=5)
        
        # Iterate through bins of the current frame
        k = kmin
        while k < len(S[l]) - frame_length:
            # If current bin magnitude is below threshold, move to next bin
            if y[k] < thresh: k += 1; continue

            # If current bin is a peak
            if y[k - 1] < y[k] and y[k] > y[k + 1]:
                # Obtain the region of interest (ROI) around the peak
                roi = np.zeros(len(S[l])) - np.inf
                roi[k: k + frame_length] = S[l][k: k + frame_length]

                # Identify the peak within the ROI and convert bin index to frequency
                peaks.append(np.argmax(roi) * (sr / fft_size))

                # Update the starting bin index for the next peak search
                if k >= int(librosa.note_to_hz('F4') / (sr / frame_length)) or l in onsets:
                    kmin = int(librosa.note_to_hz('E2') / (sr / frame_length))
                else:
                    kmin = np.max(peaks[-1] - 10, int(librosa.note_to_hz('E2') / (sr / frame_length)))

                break

            else: k += 1

    peaks = np.array(peaks)

    return peaks

def hz_to_midi(frequencies):
    """
    Convert frequencies to their corresponding MIDI note numbers and center them around the mean.

    Parameters:
        frequencies (numpy.ndarray): frequencies to be converted to MIDI note numbers.

    Returns:
        note_nums (numpy.ndarray): MIDI note numbers with mean-centered values.

    """
    # Convert frequencies to MIDI note numbers
    note_nums = librosa.hz_to_midi(frequencies)
    # Mean-center the MIDI note numbers
    note_nums = note_nums - np.mean(note_nums)

    return note_nums

def parse_req(request):
    """
    Parses a Flask request containing form data to extract signal and sample rate.

    Parameters:
        request (flask.request): Flask request object containing form data.

    Returns:
        y (numpy.ndarray): Signal extracted from the form as a float array.
        sr (int): Sample rate extracted from the form.

    """
    # Extract signal from the form and convert it to a float array
    y = np.array([float(x) for x in request.form['signal'].split(',')])
    # Normalize the signal
    y = y / np.max(abs(y))

    # Extract sample rate from the form
    sr = int(request.form['sample-rate'])

    return y, sr

def stft(x, sr):
    """
    Calculate the Short-Time Fourier Transform (STFT) of an audio signal.

    Parameters:
        x (np.ndarray): Input audio signal.
        sr (int): Sample rate of the audio signal.

    Returns:
        S (np.ndarray): STFT representation of the signal.
        onsets (np.ndarray): Indices of frames with onsets.
        fft_size (int): Size of the FFT used.

    Frames with low root-mean-square (rms) value are identified as onsets and their indices are stored.
    """
    # Parameters
    fft_size = 8192
    win_length = 8191
    hop_length = 2048
    thresh = 0.01

    # Generate Hamming window
    window  = scipy.signal.get_window('hamming', Nx=win_length)
    window = window / sum(window)

    S = []
    onsets = []
    
    # Iterate through the signal in overlapping frames
    l = 0
    while l < len(x) - win_length:
        y = x[l: l + win_length]

        # If root mean square (RMS) exceeds threshold
        if np.sqrt(np.dot(y, y) / win_length) > thresh:
            # Apply windowing
            y = y * window

            # Zero-padding and shifting for FFT
            fft_buffer = np.zeros(fft_size)
            fft_buffer[: int(math.floor((win_length + 1) / 2))] = y[int(math.floor(win_length / 2)):] 
            fft_buffer[fft_size - int(math.floor(win_length / 2)):] = y[: int(math.floor(win_length / 2))]

            # Compute FFT and convert to decibels (dB)
            X = scipy.fft.fft(fft_buffer)
            X = abs(X)[: int(librosa.note_to_hz('C5') / (sr / fft_size))]
            X[X < np.finfo(float).eps] = np.finfo(float).eps
            X_db = 10 * np.log10(X)

            S.append(X_db)
        # If frame has low rms value, mark its index as an onset
        else:
            try:
                onsets.append(len(S))
            except:
                pass

        l += hop_length

    S = np.array(S)
    onsets = np.array(onsets)

    return S, onsets, fft_size