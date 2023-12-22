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
    "peakFreqs": []
}

M=4095
N=4096
H= 440

hM1 = int(math.floor((M + 1) / 2))
hM2 = int(math.floor(M / 2))
eps = np.finfo(float).eps
cf = int(2500 * N / 44100)

w  = get_window('blackman', M)
w = w / sum(w)

dfts = []
peakFreqs = []

count = 0
fi = 0
nf = 0
for file in filenames:
    print('file: {}'.format(nf))
    fs, x = wavfile.read("samples/" + file)
    x = x / np.max(abs(x))

    l = 0
    while l + M < len(x):
        print('frame: {}'.format(count))
        y = x[l: l + M] * w

        rmsframe = np.sqrt(np.dot(y, y) / M)
        if rmsframe > 2e-5:

            y = y / np.max(abs(y))  

            fftBuffer = np.zeros(N)
            fftBuffer[: hM1] = y[hM2:] 
            fftBuffer[N - hM2:] = y[: hM2]

            X = fft(fftBuffer)
            absX = abs(X[: cf])
            absX[absX < np.finfo(float).eps] = np.finfo(float).eps
            mX = 10 * np.log10(absX)
            

            peaks = []
            mags = []
            k = 1
            while k < len(mX) - 1:
                if len(peaks) == 8:
                    break
                if mX[k] < -25: 
                    k += 1
                    continue

                if mX[k-1] < mX[k] and mX[k] > mX[k+1]:
                    tmp = np.zeros(len(mX)) - 100
                    tmp[k:k+15] = mX[k:k+15]
                    peaks.append(np.argmax(tmp))
                    mags.append(mX[np.argmax(tmp)])
                    k = np.argmax(tmp) + 10
                else: k += 1

            plt.plot(mX)
            plt.scatter(peaks, mags, c='r')
            plt.show()

            peaks = (np.array(peaks) * fs / N).tolist()

            proceed = input()
            if proceed == 'y':
                dfts.append(mX.tolist())
                peakFreqs.append(sorted(peaks))

            if count % 5 == 0:
                data['dfts'] = dfts
                data['peakFreqs'] = peakFreqs
                dfts = []
                peakFreqs = []
                with open('dataset/data' + str(fi) + '.json', 'w') as fp:
                    json.dump(data, fp, indent=4)
                fi += 1
        
        count+=1
        l += H
    nf+=1
