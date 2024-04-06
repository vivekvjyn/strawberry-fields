import math
import numpy as np
import scipy.fft
import scipy.signal
import librosa

import matplotlib.pyplot as plt

def dtw(collection, x, frame_length, hop_length):

    min_costs = [np.inf, np.inf, np.inf, np.inf]
    results = [None, None, None, None]

    for document in collection.find():
        y = np.array(document["melody"])

        cost = np.inf
        l = 0
        while l < len(y) - frame_length:
            y_sub = y[l: l + frame_length]
            y_sub = y_sub - np.mean(y_sub)

            D, wp = librosa.sequence.dtw(x, y_sub, subseq=True, global_constraints=True, band_rad=0.1)
            cost = min(D[-1, -1], cost)

            l += hop_length

        for i in range(len(min_costs)):
            if cost < min_costs[i]:
                min_costs.insert(i, cost)
                min_costs = min_costs[:4]

                results.insert(i, document)
                results = results[:4]
                break
        
    return results

def hz_to_midi(frequencies):

    note_nums = librosa.hz_to_midi(frequencies)
    note_nums = note_nums - np.mean(note_nums)

    return note_nums

def parse_req(request):

    y = np.array([float(x) for x in request.form['signal'].split(',')])
    y = y / np.max(abs(y))
    sr = int(request.form['sample-rate'])

    return y, sr

def peak_eval(S, onsets, sr, fft_size):

    frame_length = 15
    thresh = -25

    kmin = int(librosa.note_to_hz('E2') / (sr / fft_size))

    peaks = []
    for x in S:
        y = scipy.signal.savgol_filter(x, window_length=15, polyorder=5)
        
        k = kmin
        while k < len(x) - frame_length:
            if y[k] < thresh: k += 1; continue

            if y[k - 1] < y[k] and y[k] > y[k + 1]:
                roi = np.zeros(len(x)) - np.inf
                roi[k: k + frame_length] = x[k: k + frame_length]
                peaks.append(np.argmax(roi) * (sr / fft_size))

                if k >= int(librosa.note_to_hz('F4') / (sr / frame_length)) or k in onsets:
                    kmin = int(librosa.note_to_hz('E2') / (sr / frame_length))
                else:
                    kmin = np.max(peaks[-1] - 10, int(librosa.note_to_hz('E2') / (sr / frame_length)))

                break

            else: k += 1

    return np.array(peaks)

def stft(x, sr):

    fft_size = 8192
    win_length = 8191
    hop_length = 2048
    thresh = 0.01

    window  = scipy.signal.get_window('hamming', Nx=win_length)
    window = window / sum(window)

    S = []
    onsets = []
    
    l = 0
    while l < len(x) - win_length:
        y = x[l: l + win_length]

        if np.sqrt(np.dot(y, y) / win_length) > thresh:
            y = y * window

            fft_buffer = np.zeros(fft_size)
            fft_buffer[: int(math.floor((win_length + 1) / 2))] = y[int(math.floor(win_length / 2)):] 
            fft_buffer[fft_size - int(math.floor(win_length / 2)):] = y[: int(math.floor(win_length / 2))]

            X = scipy.fft.fft(fft_buffer)
            X = abs(X)[: int(librosa.note_to_hz('C5') / (sr / fft_size))]
            X[X < np.finfo(float).eps] = np.finfo(float).eps
            X_db = 10 * np.log10(X)

            S.append(X_db)
        else:
            try:
                onsets.append(len(S))
            except:
                pass

        l += hop_length

    return np.array(S), np.array(onsets), fft_size