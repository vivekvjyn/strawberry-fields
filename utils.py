import math
import numpy as np
from scipy.fft import fft
from scipy.signal import get_window
from scipy.signal import savgol_filter
import librosa
from fastdtw import fastdtw

def parse(form):
    signal = np.array([float(x) for x in form['signal'].split(',')])
    signal = signal / np.max(abs(signal))
    sr = int(form['sample-rate'])

    return signal, sr

def local_max(stft, t_onset, sr, n_fft, window_length=15):
    f0 = []
    k = 15

    for frame_index in range(len(stft)):
        dft = stft[frame_index]
        dft_savgol = savgol_filter(dft, window_length=15, polyorder=5)
        
        bin = k
        while bin < len(dft) - window_length: 
            if dft_savgol[bin] < -21: 
                bin += 1
                continue

            if dft_savgol[bin - 1] < dft_savgol[bin] and dft_savgol[bin] > dft_savgol[bin + 1]:
                window = np.zeros(len(dft_savgol)) - 100
                window[bin: bin + window_length] = dft[bin: bin + window_length]
                
                peak = np.argmax(window) 

                if frame_index > 59 or frame_index in t_onset:
                    k = 15
                else:
                    k = max(peak - 10, 15)

                f0.append(peak * sr / n_fft)

                break                
            else:
                bin += 1
        

    return np.array(f0)

def midi(f0):
    midi_sequence = 69 + 12 * np.log2((f0 + 0.0001) / 440)
    midi_sequence = midi_sequence - np.mean(midi_sequence)

    return midi_sequence

def stft(x, sr, n_fft=8192, win_length=8191, hop_length=2048, fmax=523):
    stft = []
    t_onset = []
    window  = get_window('hamming', win_length)
    window = window / sum(window)
    
    frame_index = 0
    while frame_index < len(x) - win_length:
        frame = x[frame_index: frame_index + win_length]
        
        rms = np.sqrt(np.dot(frame, frame) / win_length)    
        
        if rms > 0.01:
            frame = frame / np.max(abs(frame))
            frame = frame * window

            fft_buffer = np.zeros(n_fft)
            fft_buffer[: int(math.floor((win_length + 1) / 2))] = frame[int(math.floor(win_length / 2)):] 
            fft_buffer[n_fft - int(math.floor(win_length / 2)):] = frame[: int(math.floor(win_length / 2))]

            dft = fft(fft_buffer)
            dtf = abs(dft)[: int(fmax * n_fft / sr)]
            dtf[dtf < np.finfo(float).eps] = np.finfo(float).eps
            dft = 10 * np.log10(dtf)

            stft.append(dft)
        else:
            try:
                t_onset.append(len(stft))
            except:
                pass

        frame_index += hop_length

    return np.array(stft), t_onset, n_fft

def pyin(x, sr, frame_length=4096, win_length = 1024, hop_length=2048, fmin=82, fmax=523):
    f0 = librosa.pyin(x, sr=sr, frame_length=frame_length, win_length=win_length, hop_length=hop_length, fmin=fmin, fmax=fmax)[0]
    f0 = f0[~np.isnan(f0)]

    return f0

def dtw(collection, x, win_length, hop_length):
    min_distances = [np.inf, np.inf]
    meta = [None, None]

    for document in collection.find():
        y = np.array(document["melody"])

        window_index = 0
        distance = np.inf

        while window_index < len(y) - win_length:
            window = y[window_index: window_index + win_length]
            window = window - np.mean(window)

            distance = min(fastdtw(x, window)[0], distance)

            window_index += hop_length

        if distance < min_distances[0]:
            min_distances[1] = min_distances[0]
            min_distances[0] = distance

            meta[1] = meta[0]
            meta[0] = {"title": document["title"], "album": document["album"], "singer": document["singer"], "composer": document["composer"], "lyricist": document["lyricist"], "link": document["link"]}

        elif distance < min_distances[1]:
            min_distances[1] = distance

            meta[1] = {"title": document["title"], "album": document["album"], "singer": document["singer"], "composer": document["composer"], "lyricist": document["lyricist"], "link": document["link"]}
        
    return meta