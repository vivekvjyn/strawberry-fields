import numpy as np
import librosa

def dtw(collection, X, window_size, hop_length):
    """
    Dynamic Time Warping (DTW) on a pymongo.collection.Collection.

    """
    distances = [np.inf, np.inf, np.inf, np.inf]
    results = [None, None, None, None]

    for document in collection.find():
        vector = np.array(document["vector"])
        cost = np.inf

        for l in range(0, len(vector) - window_size, hop_length):
            Y = vector[l: l + window_size]
            Y = Y - np.mean(Y)

            D = librosa.sequence.dtw(X, Y, subseq=True, global_constraints=True, band_rad=0.1, backtrack=False)
            cost = min(D[-1, -1], cost)

        for i in range(len(distances)):
            if cost < distances[i]:
                distances.insert(i, cost)
                distances = distances[: 4]

                results.insert(i, document)
                results = results[: 4]
                break
        
    return results

def hz_to_midi(frequencies):
    """
    Frequencies to MIDI note numbers.

    """
    note_nums = librosa.hz_to_midi(frequencies)
    note_nums = note_nums - np.mean(note_nums)

    return note_nums

def parse_request(request):
    """
    Parses a request form.

    """

    y = np.array([float(x) for x in request.form['signal'].split(',')])
    y = y / np.max(abs(y))
    sr = int(request.form['sample-rate'])

    return y, sr

def pyin(y, sr):
    """
    F0 estimation using Probabilistic YIN (PYIN) algorithm
    """
    f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin=librosa.note_to_hz('E2'), fmax=librosa.note_to_hz('C5'), sr=sr)
    f0 = f0[~np.isnan(f0)]
    f0 = f0[0::4]

    return f0