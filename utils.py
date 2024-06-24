import numpy as np
import librosa
from tslearn.neighbors import KNeighborsTimeSeries

model = KNeighborsTimeSeries.from_json("model.json")

def dtw(candidates, X, window_size, hop_length):
    """
    Perform Dynamic Time Warping (DTW) on the candidates to find the closest match.

    """
    min_cost = np.inf
    result = None

    for document in candidates:
        vector = np.array(document["vector"])
        cost = np.inf

        for l in range(0, len(vector) - window_size, hop_length):
            Y = vector[l: l + window_size]
            Y = Y - np.mean(Y)

            D = librosa.sequence.dtw(X, Y, subseq=True, global_constraints=True, band_rad=0.1, backtrack=False)
            cost = min(D[-1, -1], cost)

        if cost < min_cost:
            min_cost = cost

            result = document
        
    return result

def hz_to_midi(frequencies):
    """
    Convert frequencies to mean centered MIDI note numbers.

    """
    note_nums = librosa.hz_to_midi(frequencies)
    note_nums = note_nums - np.mean(note_nums)

    return note_nums

def knn(collection, X):
    """
    Select top candidates from the database.

    """
    idx = set(model.kneighbors(X=[X.tolist()], n_neighbors=20, return_distance=False)[0])
    
    candidates = []
    for document in collection.find():
        if not idx.isdisjoint(set(document["hashes"])):
            candidates.append(document)

    return candidates

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

    y = np.isnan(f0)
    for i in range(1, len(f0)):
        if y[i]:
            f0[i] = f0[i - 1]

    f0 = f0[~np.isnan(f0)]
    f0 = f0[0::4]

    return f0