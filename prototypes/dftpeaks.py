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
H= 4410

hM1 = int(math.floor((M + 1) / 2))
hM2 = int(math.floor(M / 2))
eps = np.finfo(float).eps
cf = int(2500 * N / 44100)

w  = get_window('blackman', M)
w = w / sum(w)

dfts = []
peakFreqs = []

count = 0
for file in filenames:
    if count >= 50: break
    fs, x = wavfile.read("samples/" + file)
    x = x / np.max(abs(x))
    #plt.plot(x)
    #plt.show()
    l = 0
    while l + M < len(x):
        if count >= 50: break
        print(50 - count)
        y = x[l: l + M] * w

        rmsframe = np.sqrt(np.dot(y, y) / M)
        if rmsframe > 2e-5:    

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
                count+=1
                dfts.append(mX.tolist())
                peakFreqs.append(sorted(peaks))

        l += H

data['dfts'] = dfts
data['peakFreqs'] = peakFreqs

#plt.plot(rms)
#plt.show()
print(len(data['dfts']))

with open('data.json', 'w') as fp:
    json.dump(data, fp, indent=4)

'''            if len(peaks) < 8:
                k = 1
                while k < len(mX) - 1:
                    if len(peaks) == 8:
                        break
                    if mX[k] > -45 or mX[k] < -55: 
                        k += 1
                        continue

                    if mX[k-1] < mX[k] and mX[k] > mX[k+1]:
                        tmp = np.zeros(len(mX)) - 100
                        tmp[k:k+10] = mX[k:k+10]
                        peaks.append(np.argmax(tmp))
                        mags.append(max(mX[k:k+10]))
                        k += 10
                    else:
                        k += 1
'''