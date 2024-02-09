import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, ifft
from scipy.signal import get_window
from scipy.io import wavfile
from scipy.signal import savgol_filter
import json

filenames = ['c-major-scale.wav', 'cinematic1.wav', 'cinematic2.wav', 'cinematic3.wav', 'indian1.wav', 'indian2.wav', 'milan.wav', 'mohabatein.wav', 'mruthubhaave.wav', 'piano-A4.wav', 'processed.wav', 'sawtooth.wav', 'talasaki.wav', 'tu-jesty.wav']

data = {
    "dfts": [],
    "peakFreqs": []
}

M=4095
N=4096
H= 1024

hM1 = int(math.floor((M + 1) / 2))
hM2 = int(math.floor(M / 2))
eps = np.finfo(float).eps

w  = get_window('blackman', M)
w = w / sum(w)

dfts = []
peakFreqs = []

curr = 0
for file in filenames:
    print('file: {}'.format(curr))
    fs, x = wavfile.read("samples/" + file)
    x = x / np.max(abs(x))

    print('number of samples: {}'.format(len(x) / H))

    l = 44100
    while l + M < len(x):
        y = x[l: l+M]

        
        rmsframe = np.sqrt(np.dot(y, y) / M)    
        print(rmsframe)
        
        if rmsframe < 0.0001:
            continue

        y = y / np.max(abs(y))  

        fftBuffer = np.zeros(N)
        fftBuffer[: hM1] = y[hM2:] 
        fftBuffer[N - hM2:] = y[: hM2]

        X = fft(fftBuffer)
        absX = abs(X)
        absX[absX < np.finfo(float).eps] = np.finfo(float).eps
        mX = 10 * np.log10(absX)[:int(2500 * N / fs)]
        mX = savgol_filter(mX, 12, 5)

        plt.plot(mX)
        plt.show()

        peaks = []
        for i in range(4):
            peaks.append(float(input()))

        l += 10 * H

    curr += 1

data['dfts'] = dfts
data['peakFreqs'] = peakFreqs

with open("data.json", "w") as fp:
    json.dump(data, fp, indent=4)