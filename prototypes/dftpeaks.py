import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, ifft
from scipy.signal import get_window
from scipy.io import wavfile
import IPython
import json

filenames = ['bro1.wav', 'bro2.wav', 'bro3.wav', 'c-major-scale.wav', 'cinematic1.wav', 'cinematic2.wav', 'cinematic3.wav', 'indian1.wav', 'indian2.wav', 'milan.wav', 'mohabatein.wav', 'mruthubhaave.wav', 'piano-A4.wav', 'processed.wav', 'sawtooth.wav', 'talasaki.wav', 'tu-jesty.wav']

data = {
    "dfts": [],
    "peakBins": []
}

M=8001
N=8192
H=256

hM1 = int(math.floor((M + 1) / 2))
hM2 = int(math.floor(M / 2))
eps = np.finfo(float).eps
cf = int(2500 * N / 44100)

w  = get_window('blackman', M)
w = w / sum(w)


fs, x = wavfile.read("samples/" + filenames[0])
x = x / np.max(abs(x))
#plt.plot(x)
#plt.show()
x = x[int(1e5): int(1.5e5)]

dfts = []

l = 0
while l < 10000:
    y = x[l: l + M] * w

    fftBuffer = np.zeros(N)
    fftBuffer[: hM1] = y[hM2:] 
    fftBuffer[N - hM2:] = y[: hM2]

    X = fft(fftBuffer)
    absX = abs(X[: cf])
    absX[absX < np.finfo(float).eps] = np.finfo(float).eps
    mX = 20 * np.log10(absX)
    dfts.append(mX.tolist())

    l += H

data['dfts'] = dfts

print(data)